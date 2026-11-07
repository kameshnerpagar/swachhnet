/**
 * controllers/complaintController.js — Garbage Complaint Management
 * Dual-Database Engine: Supports PostgreSQL (Amazon RDS) & MongoDB Atlas.
 * Integrates Amazon S3 / Cloudinary for photo evidence and Gemini Flash for visual verification.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const db = require('../db');
const User = require('../models/User');
const Complaint = require('../models/Complaint');
const { uploadToS3, getPresignedDownloadUrl } = require('../services/s3Service');
const { enqueueJob } = require('../services/sqsService');
const logger = require('../services/logger');
const axios = require('axios');

const isPostgres = () => Boolean(process.env.DATABASE_URL || process.env.PGHOST);

// Helper to format PostgreSQL complaint record and generate fresh S3 presigned URLs
async function formatPgComplaint(row) {
  if (!row) return null;

  const imageUrl = row.image_url || (await getPresignedDownloadUrl(row.s3_key));
  const afterImageUrl = row.after_image_url || (await getPresignedDownloadUrl(row.after_s3_key));

  return {
    _id: row.id,
    id: row.id,
    imageUrl,
    afterImageUrl,
    s3Key: row.s3_key,
    afterS3Key: row.after_s3_key,
    location: {
      latitude: row.latitude,
      longitude: row.longitude,
      address: row.address || '',
    },
    status: row.status,
    description: row.description || '',
    userId: row.user_id,
    userName: row.user_name || '',
    authorityId: row.authority_id,
    workerId: row.worker_id ? {
      _id: row.worker_id,
      id: row.worker_id,
      workerDetails: {
        truckNumber: row.truck_number || '',
      },
    } : null,
    rating: row.rating,
    ratingComment: row.rating_comment,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

/**
 * Upload helper that uses S3 when configured or falls back to Cloudinary / Mock
 */
async function uploadEvidence(file, folder = 'complaints') {
  if (process.env.S3_BUCKET_NAME) {
    const s3Res = await uploadToS3(file.buffer, file.originalname, file.mimetype, folder);
    return {
      url: s3Res.url,
      publicId: s3Res.s3Key,
      s3Key: s3Res.s3Key,
    };
  }

  // Cloudinary fallback if configured
  if (process.env.CLOUDINARY_CLOUD_NAME && process.env.CLOUDINARY_API_KEY) {
    const cloudinary = require('cloudinary').v2;
    cloudinary.config({
      cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
      api_key: process.env.CLOUDINARY_API_KEY,
      api_secret: process.env.CLOUDINARY_API_SECRET,
    });

    const b64 = Buffer.from(file.buffer).toString('base64');
    const dataURI = `data:${file.mimetype};base64,${b64}`;
    const result = await cloudinary.uploader.upload(dataURI, {
      folder: `smart-garbage/${folder}`,
    });

    return {
      url: result.secure_url,
      publicId: result.public_id,
      s3Key: result.public_id,
    };
  }

  // Local / mock fallback
  const mockKey = `${folder}/${Date.now()}-${file.originalname}`;
  return {
    url: `https://via.placeholder.com/800x600?text=${folder}+Proof`,
    publicId: mockKey,
    s3Key: mockKey,
  };
}

/**
 * POST /api/complaints
 */
const createComplaint = async (req, res) => {
  try {
    const { latitude, longitude, address, description, authorityId } = req.body;

    if (!req.file) {
      return res.status(400).json({ success: false, message: 'Image is required' });
    }

    if (!latitude || !longitude) {
      return res.status(400).json({ success: false, message: 'Location coordinates are required' });
    }

    if (!authorityId) {
      return res.status(400).json({ success: false, message: 'Ward Authority ID is required' });
    }

    const imageBuffer = req.file.buffer;
    const base64Data = imageBuffer.toString('base64');
    const mimeType = req.file.mimetype || 'image/jpeg';

    // --- GEMINI AI IMAGE VALIDATION ---
    if (process.env.G_API && process.env.SKIP_AI_VALIDATION !== 'true') {
      try {
        const genAI = new GoogleGenerativeAI(process.env.G_API.trim());
        const model = genAI.getGenerativeModel({ model: 'gemini-flash-latest' });

        const prompt = 'Analyze this image. Does it show a garbage dump, overflowing trash, waste, or litter that needs cleaning? Reply with only a single word: YES or NO.';
        const imagePart = {
          inlineData: {
            data: base64Data,
            mimeType,
          },
        };

        const result = await model.generateContent([prompt, imagePart]);
        const aiResponse = result.response.text().trim().toLowerCase();
        logger.info(`[AI Validation] Result: ${aiResponse}`);

        if (!aiResponse.includes('yes')) {
          return res.status(400).json({
            success: false,
            message: 'AI Validation Failed: No garbage or waste detected in this image. Please upload a valid photo.',
          });
        }
      } catch (aiError) {
        logger.error(`[AI Validation Warning] ${aiError.message}`);
        if (process.env.STRICT_AI_VALIDATION === 'true') {
          return res.status(503).json({
            success: false,
            message: 'AI Validation service unavailable. Please try again shortly.',
          });
        }
      }
    }

    // Upload image to S3 or Cloudinary
    const evidence = await uploadEvidence(req.file, 'complaints');

    if (isPostgres()) {
      const insertSql = `
        INSERT INTO complaints (
          user_id, user_name, authority_id, s3_key, image_url,
          latitude, longitude, address, description, status
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'open')
        RETURNING *
      `;

      const insertResult = await db.query(insertSql, [
        req.user.id,
        req.user.name,
        authorityId,
        evidence.s3Key,
        evidence.url,
        parseFloat(latitude),
        parseFloat(longitude),
        address || '',
        description || '',
      ]);

      const createdRecord = await formatPgComplaint(insertResult.rows[0]);

      await enqueueJob('COMPLAINT_CREATED', {
        complaintId: createdRecord.id,
        authorityId,
        userId: req.user.id,
      });

      return res.status(201).json({
        success: true,
        message: 'Complaint submitted successfully',
        complaint: createdRecord,
      });
    } else {
      // MongoDB Atlas fallback
      const complaint = await Complaint.create({
        imageUrl: evidence.url,
        imagePublicId: evidence.publicId,
        location: {
          latitude: parseFloat(latitude),
          longitude: parseFloat(longitude),
          address: address || '',
        },
        description: description || '',
        userId: req.user._id,
        userName: req.user.name,
        authorityId,
      });

      await enqueueJob('COMPLAINT_CREATED', {
        complaintId: complaint._id,
        authorityId,
        userId: req.user._id,
      });

      return res.status(201).json({
        success: true,
        message: 'Complaint submitted successfully',
        complaint,
      });
    }
  } catch (err) {
    logger.error(`Create complaint error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * GET /api/complaints/user
 */
const getUserComplaints = async (req, res) => {
  try {
    const { status } = req.query;

    if (isPostgres()) {
      let sql = `
        SELECT c.*, w.truck_number
        FROM complaints c
        LEFT JOIN workers w ON w.user_id = c.worker_id
        WHERE c.user_id = $1
      `;
      const params = [req.user.id];

      if (status && status !== 'all') {
        params.push(status);
        sql += ` AND c.status = $${params.length}`;
      }

      sql += ' ORDER BY c.created_at DESC';

      const result = await db.query(sql, params);
      const complaints = await Promise.all(result.rows.map(formatPgComplaint));

      return res.json({ success: true, count: complaints.length, complaints });
    } else {
      // MongoDB Atlas fallback
      const filter = { userId: req.user._id };
      if (status && status !== 'all') filter.status = status;

      const complaints = await Complaint.find(filter)
        .populate('workerId', 'workerDetails.truckNumber')
        .sort({ createdAt: -1 });

      return res.json({ success: true, count: complaints.length, complaints });
    }
  } catch (err) {
    logger.error(`Get user complaints error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * GET /api/complaints/worker
 */
const getWorkerComplaints = async (req, res) => {
  try {
    if (isPostgres()) {
      const sql = `
        SELECT c.*, u.name AS citizen_name, u.email AS citizen_email
        FROM complaints c
        JOIN users u ON u.id = c.user_id
        WHERE c.worker_id = $1
        ORDER BY c.created_at DESC
      `;

      const result = await db.query(sql, [req.user.id]);
      const complaints = await Promise.all(
        result.rows.map(async (row) => {
          const formatted = await formatPgComplaint(row);
          formatted.userId = {
            _id: row.user_id,
            id: row.user_id,
            name: row.citizen_name,
            email: row.citizen_email,
          };
          return formatted;
        })
      );

      return res.json({ success: true, count: complaints.length, complaints });
    } else {
      // MongoDB Atlas fallback
      const complaints = await Complaint.find({ workerId: req.user._id })
        .populate('userId', 'name email')
        .sort({ createdAt: -1 });

      return res.json({ success: true, count: complaints.length, complaints });
    }
  } catch (err) {
    logger.error(`Get worker complaints error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * GET /api/complaints/all
 */
const getAllComplaints = async (req, res) => {
  try {
    const { status } = req.query;

    if (isPostgres()) {
      let sql = `
        SELECT c.*, u.name AS citizen_name, u.email AS citizen_email, w.truck_number
        FROM complaints c
        JOIN users u ON u.id = c.user_id
        LEFT JOIN workers w ON w.user_id = c.worker_id
      `;
      const params = [];

      if (req.user.role === 'admin') {
        params.push(req.user.id);
        sql += ` WHERE c.authority_id = $${params.length}`;
      }

      if (status && status !== 'all') {
        sql += params.length ? ' AND' : ' WHERE';
        params.push(status);
        sql += ` c.status = $${params.length}`;
      }

      sql += ' ORDER BY c.created_at DESC';

      const result = await db.query(sql, params);
      const complaints = await Promise.all(
        result.rows.map(async (row) => {
          const formatted = await formatPgComplaint(row);
          formatted.userId = {
            _id: row.user_id,
            id: row.user_id,
            name: row.citizen_name,
            email: row.citizen_email,
          };
          return formatted;
        })
      );

      return res.json({ success: true, count: complaints.length, complaints });
    } else {
      // MongoDB Atlas fallback
      const filter = {};
      if (status && status !== 'all') filter.status = status;

      if (req.user.role === 'admin') {
        filter.authorityId = req.user._id;
      }

      const complaints = await Complaint.find(filter)
        .populate('userId', 'name email')
        .populate('workerId', 'workerDetails.truckNumber')
        .sort({ createdAt: -1 });

      return res.json({ success: true, count: complaints.length, complaints });
    }
  } catch (err) {
    logger.error(`Get all complaints error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * POST /api/complaints/:id/assign-truck
 */
const assignTruck = async (req, res) => {
  try {
    const { id } = req.params;

    if (isPostgres()) {
      const complaintRes = await db.query('SELECT * FROM complaints WHERE id = $1', [id]);
      if (complaintRes.rows.length === 0) {
        return res.status(404).json({ success: false, message: 'Complaint not found' });
      }

      const complaint = complaintRes.rows[0];
      if (complaint.authority_id !== req.user.id) {
        return res.status(403).json({ success: false, message: 'Not authorized to assign this complaint' });
      }

      const truckSql = `
        SELECT w.user_id, w.truck_number, w.latitude, w.longitude,
          (6371 * acos(
            LEAST(1.0, GREATEST(-1.0,
              cos(radians($1)) * cos(radians(w.latitude)) * 
              cos(radians(w.longitude) - radians($2)) + 
              sin(radians($1)) * sin(radians(w.latitude))
            ))
          )) AS distance_km
        FROM workers w
        WHERE w.assigned_ward_id = $3 AND w.status = 'idle'
        ORDER BY distance_km ASC
        LIMIT 1
        FOR UPDATE
      `;

      const updatedComplaint = await db.transaction(async (client) => {
        const truckRes = await client.query(truckSql, [
          complaint.latitude,
          complaint.longitude,
          req.user.id,
        ]);

        if (truckRes.rows.length === 0) {
          throw new Error('No idle trucks available in your ward. You can wait or transfer this report.');
        }

        const assignedWorker = truckRes.rows[0];

        const updRes = await client.query(
          `UPDATE complaints 
           SET worker_id = $1, status = 'assigned', updated_at = NOW()
           WHERE id = $2
           RETURNING *`,
          [assignedWorker.user_id, id]
        );

        await client.query(`UPDATE workers SET status = 'busy' WHERE user_id = $1`, [assignedWorker.user_id]);

        return { complaint: updRes.rows[0], worker: assignedWorker };
      });

      const formatted = await formatPgComplaint(updatedComplaint.complaint);
      formatted.workerId = {
        _id: updatedComplaint.worker.user_id,
        id: updatedComplaint.worker.user_id,
        workerDetails: { truckNumber: updatedComplaint.worker.truck_number },
      };

      await enqueueJob('TRUCK_ASSIGNED', {
        complaintId: id,
        truckNumber: updatedComplaint.worker.truck_number,
      });

      return res.json({
        success: true,
        message: `Truck ${updatedComplaint.worker.truck_number} assigned`,
        complaint: formatted,
        worker: { truckNumber: updatedComplaint.worker.truck_number },
      });
    } else {
      // MongoDB Atlas fallback
      const complaint = await Complaint.findById(id);
      if (!complaint) return res.status(404).json({ success: false, message: 'Complaint not found' });

      if (complaint.authorityId.toString() !== req.user._id.toString()) {
        return res.status(403).json({ success: false, message: 'Not authorized to assign this complaint' });
      }

      const nearestWorker = await User.findOne({
        role: 'worker',
        'workerDetails.status': 'idle',
        'workerDetails.assignedWard': req.user._id,
        'workerDetails.location': {
          $near: {
            $geometry: {
              type: 'Point',
              coordinates: [complaint.location.longitude, complaint.location.latitude],
            },
          },
        },
      });

      if (!nearestWorker) {
        return res.status(400).json({
          success: false,
          message: 'No idle trucks available in your ward. You can wait or transfer this report to an adjacent ward.',
        });
      }

      complaint.workerId = nearestWorker._id;
      complaint.status = 'assigned';
      await complaint.save();

      await User.updateOne({ _id: nearestWorker._id }, { $set: { 'workerDetails.status': 'busy' } });

      await enqueueJob('TRUCK_ASSIGNED', {
        complaintId: complaint._id,
        truckNumber: nearestWorker.workerDetails.truckNumber,
      });

      return res.json({
        success: true,
        message: `Truck ${nearestWorker.workerDetails.truckNumber} assigned`,
        complaint,
        worker: nearestWorker.workerDetails,
      });
    }
  } catch (err) {
    logger.error(`Assign truck error: ${err.message}`);
    res.status(400).json({ success: false, message: err.message });
  }
};

/**
 * PATCH /api/complaints/:id/transfer
 */
const transferComplaint = async (req, res) => {
  try {
    const { id } = req.params;
    const { newAuthorityId, newAuthorityName } = req.body;

    if (!newAuthorityId || !newAuthorityName) {
      return res.status(400).json({ success: false, message: 'New authority ID and Name are required' });
    }

    if (isPostgres()) {
      const complaintRes = await db.query('SELECT * FROM complaints WHERE id = $1', [id]);
      if (complaintRes.rows.length === 0) {
        return res.status(404).json({ success: false, message: 'Complaint not found' });
      }

      const complaint = complaintRes.rows[0];
      if (complaint.authority_id !== req.user.id) {
        return res.status(403).json({ success: false, message: 'Not authorized to transfer this complaint' });
      }

      await db.transaction(async (client) => {
        if (complaint.worker_id) {
          await client.query(`UPDATE workers SET status = 'idle' WHERE user_id = $1`, [complaint.worker_id]);
        }

        await client.query(
          `INSERT INTO complaint_transfers (complaint_id, from_authority_name, to_authority_name)
           VALUES ($1, $2, $3)`,
          [id, req.user.authorityDetails?.name || req.user.name, newAuthorityName]
        );

        await client.query(
          `UPDATE complaints 
           SET authority_id = $1, worker_id = NULL, status = 'open', updated_at = NOW()
           WHERE id = $2`,
          [newAuthorityId, id]
        );
      });

      return res.json({ success: true, message: `Successfully transferred to ${newAuthorityName}` });
    } else {
      // MongoDB Atlas fallback
      const complaint = await Complaint.findById(id);
      if (!complaint) return res.status(404).json({ success: false, message: 'Complaint not found' });

      if (complaint.authorityId.toString() !== req.user._id.toString()) {
        return res.status(403).json({ success: false, message: 'Not authorized to transfer this complaint' });
      }

      if (complaint.workerId) {
        await User.updateOne({ _id: complaint.workerId }, { $set: { 'workerDetails.status': 'idle' } });
        complaint.workerId = null;
        complaint.status = 'open';
      }

      complaint.transferHistory.push({
        fromAuthorityName: req.user.authorityDetails?.name || req.user.name,
        toAuthorityName: newAuthorityName,
        timestamp: Date.now(),
      });

      complaint.authorityId = newAuthorityId;
      await complaint.save();

      return res.json({ success: true, message: `Successfully transferred to ${newAuthorityName}`, complaint });
    }
  } catch (err) {
    logger.error(`Transfer error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * POST /api/complaints/:id/worker-submit
 */
const workerSubmit = async (req, res) => {
  try {
    const { id } = req.params;

    if (!req.file) {
      return res.status(400).json({ success: false, message: 'After image proof is required' });
    }

    const afterBuffer = req.file.buffer;
    const afterBase64 = afterBuffer.toString('base64');
    const mimeType = req.file.mimetype || 'image/jpeg';

    if (isPostgres()) {
      const complaintRes = await db.query('SELECT * FROM complaints WHERE id = $1', [id]);
      if (complaintRes.rows.length === 0) {
        return res.status(404).json({ success: false, message: 'Complaint not found' });
      }

      const complaint = complaintRes.rows[0];
      if (complaint.worker_id !== req.user.id) {
        return res.status(403).json({ success: false, message: 'You are not assigned to this complaint' });
      }

      // --- GEMINI AI VERIFICATION ---
      if (process.env.G_API && process.env.SKIP_AI_VALIDATION !== 'true') {
        try {
          const genAI = new GoogleGenerativeAI(process.env.G_API.trim());
          const model = genAI.getGenerativeModel({ model: 'gemini-flash-latest' });

          const prompt = "I am providing two images. The first is a 'Before' photo showing a garbage problem. The second is an 'After' photo uploaded by a sanitation worker. Has the specific garbage from the first photo been successfully cleaned up in the second photo? Reply strictly with a single word: YES or NO.";

          let beforeBase64;
          try {
            const { getObjectBuffer } = require('../services/s3Service');
            const beforeBuffer = await getObjectBuffer(complaint.s3_key);
            beforeBase64 = beforeBuffer.toString('base64');
          } catch {
            const resp = await axios.get(complaint.image_url, { responseType: 'arraybuffer' });
            beforeBase64 = Buffer.from(resp.data, 'binary').toString('base64');
          }

          const result = await model.generateContent([
            prompt,
            { inlineData: { data: beforeBase64, mimeType: 'image/jpeg' } },
            { inlineData: { data: afterBase64, mimeType } },
          ]);

          const aiResponse = result.response.text().trim().toLowerCase();
          logger.info(`[AI Worker Validation] Result: ${aiResponse}`);

          if (!aiResponse.includes('yes')) {
            return res.status(400).json({
              success: false,
              message: 'AI Validation Failed: The area has not been properly cleaned, or the image is invalid.',
            });
          }
        } catch (aiErr) {
          logger.error(`[AI Worker Outage] ${aiErr.message}`);
        }
      }

      const evidence = await uploadEvidence(req.file, 'cleanup');

      const updatedRes = await db.transaction(async (client) => {
        const upd = await client.query(
          `UPDATE complaints
           SET after_s3_key = $1, after_image_url = $2, status = 'pending_verification', updated_at = NOW()
           WHERE id = $3
           RETURNING *`,
          [evidence.s3Key, evidence.url, id]
        );

        await client.query(`UPDATE workers SET status = 'idle' WHERE user_id = $1`, [req.user.id]);
        return upd.rows[0];
      });

      const formatted = await formatPgComplaint(updatedRes);
      return res.json({ success: true, message: 'Proof submitted. Pending verification.', complaint: formatted });
    } else {
      // MongoDB Atlas fallback
      const complaint = await Complaint.findById(id);
      if (!complaint) return res.status(404).json({ success: false, message: 'Complaint not found' });

      if (complaint.workerId?.toString() !== req.user._id.toString()) {
        return res.status(403).json({ success: false, message: 'You are not assigned to this complaint' });
      }

      // --- GEMINI AI VERIFICATION ---
      if (process.env.G_API && process.env.SKIP_AI_VALIDATION !== 'true') {
        try {
          const genAI = new GoogleGenerativeAI(process.env.G_API.trim());
          const model = genAI.getGenerativeModel({ model: 'gemini-flash-latest' });

          const prompt = "I am providing two images. The first is a 'Before' photo showing a garbage problem. The second is an 'After' photo uploaded by a sanitation worker. Has the specific garbage from the first photo been successfully cleaned up in the second photo? Reply strictly with a single word: YES or NO.";

          const beforeResp = await axios.get(complaint.imageUrl, { responseType: 'arraybuffer' });
          const beforeBase64 = Buffer.from(beforeResp.data, 'binary').toString('base64');

          const result = await model.generateContent([
            prompt,
            { inlineData: { data: beforeBase64, mimeType: 'image/jpeg' } },
            { inlineData: { data: afterBase64, mimeType } },
          ]);

          const aiResponse = result.response.text().trim().toLowerCase();
          logger.info(`[AI Worker Validation] Result: ${aiResponse}`);

          if (!aiResponse.includes('yes')) {
            return res.status(400).json({
              success: false,
              message: 'AI Validation Failed: The area has not been properly cleaned, or the image is invalid.',
            });
          }
        } catch (aiErr) {
          logger.error(`[AI Worker Outage] ${aiErr.message}`);
        }
      }

      const evidence = await uploadEvidence(req.file, 'cleanup');

      complaint.afterImageUrl = evidence.url;
      complaint.afterImagePublicId = evidence.publicId;
      complaint.status = 'pending_verification';
      await complaint.save();

      await User.updateOne({ _id: req.user._id }, { $set: { 'workerDetails.status': 'idle' } });

      return res.json({ success: true, message: 'Proof submitted. Pending verification.', complaint });
    }
  } catch (err) {
    logger.error(`Worker submit error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * PATCH /api/complaints/:id/verify
 */
const verifyComplaint = async (req, res) => {
  try {
    const { id } = req.params;

    if (isPostgres()) {
      const complaintRes = await db.query('SELECT * FROM complaints WHERE id = $1', [id]);
      if (complaintRes.rows.length === 0) return res.status(404).json({ success: false, message: 'Complaint not found' });

      const complaint = complaintRes.rows[0];
      if (complaint.authority_id !== req.user.id) return res.status(403).json({ success: false, message: 'Not authorized' });
      if (complaint.status !== 'pending_verification') return res.status(400).json({ success: false, message: 'Complaint not pending verification' });

      const updateRes = await db.query(
        `UPDATE complaints SET status = 'resolved', updated_at = NOW() WHERE id = $1 RETURNING *`,
        [id]
      );

      const formatted = await formatPgComplaint(updateRes.rows[0]);
      await enqueueJob('COMPLAINT_RESOLVED', { complaintId: id });

      return res.json({ success: true, message: 'Complaint resolved', complaint: formatted });
    } else {
      // MongoDB Atlas fallback
      const complaint = await Complaint.findById(id);
      if (!complaint) return res.status(404).json({ success: false, message: 'Complaint not found' });
      if (complaint.authorityId.toString() !== req.user._id.toString()) return res.status(403).json({ success: false, message: 'Not authorized' });
      if (complaint.status !== 'pending_verification') return res.status(400).json({ success: false, message: 'Complaint not pending verification' });

      complaint.status = 'resolved';
      await complaint.save();

      await enqueueJob('COMPLAINT_RESOLVED', { complaintId: complaint._id });

      return res.json({ success: true, message: 'Complaint resolved', complaint });
    }
  } catch (err) {
    logger.error(`Verify complaint error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * PATCH /api/complaints/:id/reject
 */
const rejectComplaint = async (req, res) => {
  try {
    const { id } = req.params;

    if (isPostgres()) {
      const complaintRes = await db.query('SELECT * FROM complaints WHERE id = $1', [id]);
      if (complaintRes.rows.length === 0) return res.status(404).json({ success: false, message: 'Complaint not found' });

      const complaint = complaintRes.rows[0];
      if (complaint.authority_id !== req.user.id) return res.status(403).json({ success: false, message: 'Not authorized' });
      if (complaint.status !== 'open') return res.status(400).json({ success: false, message: 'Only open complaints can be rejected' });

      const updateRes = await db.query(
        `UPDATE complaints SET status = 'rejected', updated_at = NOW() WHERE id = $1 RETURNING *`,
        [id]
      );

      const formatted = await formatPgComplaint(updateRes.rows[0]);
      return res.json({ success: true, message: 'Complaint rejected', complaint: formatted });
    } else {
      // MongoDB Atlas fallback
      const complaint = await Complaint.findById(id);
      if (!complaint) return res.status(404).json({ success: false, message: 'Complaint not found' });
      if (complaint.authorityId.toString() !== req.user._id.toString()) return res.status(403).json({ success: false, message: 'Not authorized' });
      if (complaint.status !== 'open') return res.status(400).json({ success: false, message: 'Only open complaints can be rejected' });

      complaint.status = 'rejected';
      await complaint.save();

      return res.json({ success: true, message: 'Complaint rejected', complaint });
    }
  } catch (err) {
    logger.error(`Reject complaint error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * GET /api/complaints/:id
 */
const getComplaintById = async (req, res) => {
  try {
    if (isPostgres()) {
      const sql = `
        SELECT c.*, u.name AS citizen_name, u.email AS citizen_email, w.truck_number
        FROM complaints c
        JOIN users u ON u.id = c.user_id
        LEFT JOIN workers w ON w.user_id = c.worker_id
        WHERE c.id = $1
      `;
      const result = await db.query(sql, [req.params.id]);
      if (result.rows.length === 0) return res.status(404).json({ success: false, message: 'Complaint not found' });

      const formatted = await formatPgComplaint(result.rows[0]);
      formatted.userId = {
        _id: result.rows[0].user_id,
        id: result.rows[0].user_id,
        name: result.rows[0].citizen_name,
        email: result.rows[0].citizen_email,
      };

      return res.json({ success: true, complaint: formatted });
    } else {
      // MongoDB Atlas fallback
      const complaint = await Complaint.findById(req.params.id).populate('userId', 'name email');
      if (!complaint) return res.status(404).json({ success: false, message: 'Complaint not found' });

      return res.json({ success: true, complaint });
    }
  } catch (err) {
    logger.error(`Get complaint by ID error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

module.exports = {
  createComplaint,
  getUserComplaints,
  getAllComplaints,
  getComplaintById,
  getWorkerComplaints,
  assignTruck,
  transferComplaint,
  workerSubmit,
  verifyComplaint,
  rejectComplaint,
};
