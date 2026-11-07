/**
 * controllers/authorityController.js — Ward Authority Operations
 * Dual-Database Engine: Supports PostgreSQL (Amazon RDS) & MongoDB Atlas.
 */

const db = require('../db');
const User = require('../models/User');
const Complaint = require('../models/Complaint');
const logger = require('../services/logger');

const isPostgres = () => Boolean(process.env.DATABASE_URL || process.env.PGHOST);

/**
 * GET /api/authorities/nearby
 */
const getNearbyAuthorities = async (req, res) => {
  try {
    let { lat, lng, limit } = req.query;

    if (!lat || !lng) {
      return res.status(400).json({ success: false, message: 'Latitude and longitude are required' });
    }

    const latitude = parseFloat(lat);
    const longitude = parseFloat(lng);
    const maxResults = parseInt(limit) || 3;

    if (isPostgres()) {
      const sql = `
        SELECT 
          u.id,
          u.id AS _id,
          u.name,
          u.email,
          u.role,
          wa.name AS authority_name,
          wa.address,
          wa.latitude,
          wa.longitude,
          wa.rating_score,
          wa.rating_count,
          (6371 * acos(
            LEAST(1.0, GREATEST(-1.0,
              cos(radians($1)) * cos(radians(wa.latitude)) * 
              cos(radians(wa.longitude) - radians($2)) + 
              sin(radians($1)) * sin(radians(wa.latitude))
            ))
          )) AS distance_km
        FROM users u
        JOIN ward_authorities wa ON wa.user_id = u.id
        WHERE u.role = 'admin'
        ORDER BY distance_km ASC
        LIMIT $3
      `;

      const result = await db.query(sql, [latitude, longitude, maxResults]);

      const formattedAuthorities = result.rows.map((row) => ({
        _id: row.id,
        id: row.id,
        name: row.name,
        email: row.email,
        role: row.role,
        distanceKm: parseFloat(row.distance_km).toFixed(2),
        authorityDetails: {
          name: row.authority_name || row.name,
          address: row.address,
          location: {
            type: 'Point',
            coordinates: [row.longitude, row.latitude],
          },
          rating: {
            score: parseFloat(row.rating_score) || 0,
            count: row.rating_count || 0,
          },
        },
      }));

      return res.json({
        success: true,
        count: formattedAuthorities.length,
        authorities: formattedAuthorities,
      });
    } else {
      // MongoDB Atlas fallback
      const authorities = await User.find({
        role: 'admin',
        'authorityDetails.location': {
          $near: {
            $geometry: {
              type: 'Point',
              coordinates: [longitude, latitude],
            },
          },
        },
      }).limit(maxResults).select('-password');

      return res.json({ success: true, count: authorities.length, authorities });
    }
  } catch (err) {
    logger.error(`Nearby authorities error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * GET /api/authorities
 */
const getAllAuthorities = async (req, res) => {
  try {
    const fortyEightHoursAgo = new Date(Date.now() - 48 * 60 * 60 * 1000);

    if (isPostgres()) {
      const sql = `
        SELECT 
          u.id,
          u.id AS _id,
          u.name,
          u.email,
          u.role,
          wa.name AS authority_name,
          wa.address,
          wa.latitude,
          wa.longitude,
          wa.rating_score,
          wa.rating_count,
          COUNT(c.id) FILTER (
            WHERE c.status NOT IN ('resolved', 'rejected') 
            AND c.created_at < $1
          ) AS sla_breaches,
          COUNT(c.id) FILTER (WHERE c.status = 'resolved') AS total_resolved
        FROM users u
        JOIN ward_authorities wa ON wa.user_id = u.id
        LEFT JOIN complaints c ON c.authority_id = u.id
        WHERE u.role = 'admin'
        GROUP BY u.id, wa.name, wa.address, wa.latitude, wa.longitude, wa.rating_score, wa.rating_count
        ORDER BY wa.name ASC
      `;

      const result = await db.query(sql, [fortyEightHoursAgo]);

      const authorities = result.rows.map((row) => ({
        _id: row.id,
        id: row.id,
        name: row.name,
        email: row.email,
        role: row.role,
        slaBreaches: parseInt(row.sla_breaches) || 0,
        totalResolved: parseInt(row.total_resolved) || 0,
        authorityDetails: {
          name: row.authority_name || row.name,
          address: row.address,
          location: {
            type: 'Point',
            coordinates: [row.longitude, row.latitude],
          },
          rating: {
            score: parseFloat(row.rating_score) || 0,
            count: row.rating_count || 0,
          },
        },
      }));

      return res.json({ success: true, count: authorities.length, authorities });
    } else {
      // MongoDB Atlas fallback
      const authorities = await User.find({ role: 'admin' }).select('-password').lean();

      for (let auth of authorities) {
        const breachCount = await Complaint.countDocuments({
          authorityId: auth._id,
          status: { $nin: ['resolved', 'rejected'] },
          createdAt: { $lt: fortyEightHoursAgo },
        });
        auth.slaBreaches = breachCount;
      }

      return res.json({ success: true, count: authorities.length, authorities });
    }
  } catch (err) {
    logger.error(`Get all authorities error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * POST /api/authorities/:id/rate
 */
const rateAuthority = async (req, res) => {
  try {
    const authorityId = req.params.id;
    const { complaintId, rating, comment } = req.body;
    const userId = req.user.id || req.user._id;

    if (!rating || rating < 1 || rating > 5) {
      return res.status(400).json({ success: false, message: 'Rating must be between 1 and 5' });
    }

    if (isPostgres()) {
      const complaintRes = await db.query(
        `SELECT id, rating FROM complaints 
         WHERE id = $1 AND user_id = $2 AND authority_id = $3 AND status = 'resolved'`,
        [complaintId, userId, authorityId]
      );

      if (complaintRes.rows.length === 0) {
        return res.status(404).json({
          success: false,
          message: 'Resolved complaint not found or does not belong to you',
        });
      }

      if (complaintRes.rows[0].rating) {
        return res.status(400).json({ success: false, message: 'You have already rated this resolution' });
      }

      await db.transaction(async (client) => {
        await client.query(
          `UPDATE complaints SET rating = $1, rating_comment = $2, updated_at = NOW() WHERE id = $3`,
          [rating, comment || '', complaintId]
        );

        const authRes = await client.query(
          `SELECT rating_score, rating_count FROM ward_authorities WHERE user_id = $1 FOR UPDATE`,
          [authorityId]
        );

        if (authRes.rows.length > 0) {
          const currentScore = parseFloat(authRes.rows[0].rating_score) || 0;
          const currentCount = parseInt(authRes.rows[0].rating_count) || 0;
          const newCount = currentCount + 1;
          const newScore = ((currentScore * currentCount) + rating) / newCount;

          await client.query(
            `UPDATE ward_authorities SET rating_score = $1, rating_count = $2 WHERE user_id = $3`,
            [newScore.toFixed(2), newCount, authorityId]
          );
        }
      });

      return res.json({ success: true, message: 'Rating submitted successfully' });
    } else {
      // MongoDB Atlas fallback
      const complaint = await Complaint.findOne({
        _id: complaintId,
        userId: userId,
        authorityId: authorityId,
        status: 'resolved',
      });

      if (!complaint) {
        return res.status(404).json({ success: false, message: 'Resolved complaint not found or does not belong to you' });
      }

      if (complaint.rating) {
        return res.status(400).json({ success: false, message: 'You have already rated this resolution' });
      }

      complaint.rating = rating;
      if (comment) complaint.ratingComment = comment;
      await complaint.save();

      const authority = await User.findById(authorityId);
      if (authority && authority.role === 'admin') {
        const currentScore = authority.authorityDetails.rating?.score || 0;
        const currentCount = authority.authorityDetails.rating?.count || 0;
        const newCount = currentCount + 1;
        const newScore = ((currentScore * currentCount) + rating) / newCount;

        authority.authorityDetails.rating.score = newScore;
        authority.authorityDetails.rating.count = newCount;
        await authority.save();
      }

      return res.json({ success: true, message: 'Rating submitted successfully' });
    }
  } catch (err) {
    logger.error(`Rate authority error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

module.exports = {
  getNearbyAuthorities,
  getAllAuthorities,
  rateAuthority,
};
