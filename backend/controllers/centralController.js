/**
 * controllers/centralController.js — Central Authority Oversight & 48h SLA Tracking
 * Dual-Database Engine: Supports PostgreSQL (Amazon RDS) & MongoDB Atlas.
 */

const db = require('../db');
const User = require('../models/User');
const Complaint = require('../models/Complaint');
const logger = require('../services/logger');

const isPostgres = () => Boolean(process.env.DATABASE_URL || process.env.PGHOST);

/**
 * GET /api/central/dashboard
 * Superadmin only
 */
const getCentralDashboard = async (req, res) => {
  try {
    const fortyEightHoursAgo = new Date(Date.now() - 48 * 60 * 60 * 1000);

    if (isPostgres()) {
      // ── PostgreSQL ────────────────────────────────────────────────────────
      const countsRes = await db.query(`
        SELECT 
          COUNT(*) AS total_complaints,
          COUNT(*) FILTER (WHERE status = 'resolved') AS total_resolved,
          COUNT(*) FILTER (WHERE status NOT IN ('resolved', 'rejected') AND created_at < $1) AS total_breaches
        FROM complaints
      `, [fortyEightHoursAgo]);

      const systemMetrics = {
        totalComplaints: parseInt(countsRes.rows[0].total_complaints) || 0,
        totalResolved: parseInt(countsRes.rows[0].total_resolved) || 0,
        totalBreaches: parseInt(countsRes.rows[0].total_breaches) || 0,
      };

      const authSql = `
        SELECT 
          u.id,
          u.id AS _id,
          u.name,
          u.email,
          wa.name AS authority_name,
          wa.address,
          wa.latitude,
          wa.longitude,
          wa.rating_score,
          wa.rating_count,
          COUNT(c.id) FILTER (WHERE c.status NOT IN ('resolved', 'rejected') AND c.created_at < $1) AS active_breaches,
          COUNT(c.id) FILTER (WHERE c.status = 'resolved') AS total_resolved
        FROM users u
        JOIN ward_authorities wa ON wa.user_id = u.id
        LEFT JOIN complaints c ON c.authority_id = u.id
        WHERE u.role = 'admin'
        GROUP BY u.id, wa.name, wa.address, wa.latitude, wa.longitude, wa.rating_score, wa.rating_count
        ORDER BY wa.name ASC
      `;
      const authRes = await db.query(authSql, [fortyEightHoursAgo]);

      const authorities = authRes.rows.map((row) => ({
        _id: row.id,
        id: row.id,
        name: row.name,
        email: row.email,
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
        metrics: {
          activeBreaches: parseInt(row.active_breaches) || 0,
          totalResolved: parseInt(row.total_resolved) || 0,
        },
      }));

      systemMetrics.totalWards = authorities.length;

      const breachSql = `
        SELECT 
          c.id,
          c.id AS _id,
          c.user_id,
          c.user_name,
          c.authority_id,
          c.worker_id,
          c.s3_key,
          c.image_url,
          c.after_s3_key,
          c.after_image_url,
          c.latitude,
          c.longitude,
          c.address,
          c.status,
          c.description,
          c.created_at AS "createdAt",
          c.updated_at AS "updatedAt",
          json_build_object(
            '_id', u.id,
            'id', u.id,
            'name', u.name,
            'authorityDetails', json_build_object('name', wa.name)
          ) AS "authorityId"
        FROM complaints c
        JOIN users u ON u.id = c.authority_id
        JOIN ward_authorities wa ON wa.user_id = u.id
        WHERE c.status NOT IN ('resolved', 'rejected') AND c.created_at < $1
        ORDER BY c.created_at ASC
      `;
      const breachRes = await db.query(breachSql, [fortyEightHoursAgo]);

      const breachedComplaints = breachRes.rows.map((row) => ({
        ...row,
        location: {
          latitude: row.latitude,
          longitude: row.longitude,
          address: row.address,
        },
      }));

      return res.json({
        success: true,
        data: {
          systemMetrics,
          authorities,
          breachedComplaints,
        },
      });
    } else {
      // ── MongoDB Atlas Fallback ────────────────────────────────────────────
      const authorities = await User.find({ role: 'admin' }).select('-password').lean();

      let totalComplaints = await Complaint.countDocuments();
      const resolvedComplaints = await Complaint.find({ status: 'resolved' }).lean();
      let totalResolved = resolvedComplaints.length;

      const breachedComplaints = await Complaint.find({
        status: { $nin: ['resolved', 'rejected'] },
        createdAt: { $lt: fortyEightHoursAgo },
      }).populate('authorityId', 'name authorityDetails').lean();

      const authorityMetrics = authorities.map((auth) => {
        const authBreaches = breachedComplaints.filter(
          (c) => c.authorityId && c.authorityId._id.toString() === auth._id.toString()
        );
        const authResolved = resolvedComplaints.filter(
          (c) => c.authorityId && c.authorityId.toString() === auth._id.toString()
        );

        return {
          ...auth,
          metrics: {
            activeBreaches: authBreaches.length,
            totalResolved: authResolved.length,
          },
        };
      });

      return res.json({
        success: true,
        data: {
          systemMetrics: {
            totalWards: authorities.length,
            totalComplaints,
            totalResolved,
            totalBreaches: breachedComplaints.length,
          },
          authorities: authorityMetrics,
          breachedComplaints,
        },
      });
    }
  } catch (err) {
    logger.error(`Central dashboard error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

module.exports = {
  getCentralDashboard,
};
