/**
 * middleware/auth.js — Dual-Database JWT Verification Middleware
 * Supports both PostgreSQL (Amazon RDS) and MongoDB Atlas (Local Development).
 */

const jwt = require('jsonwebtoken');
const db = require('../db');
const User = require('../models/User');

const isPostgres = () => Boolean(process.env.DATABASE_URL || process.env.PGHOST);

const protect = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ success: false, message: 'Not authorized. No token.' });
    }

    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'fallback_secret_for_local_testing_only');

    if (isPostgres()) {
      const result = await db.query(
        'SELECT id, name, email, role, created_at FROM users WHERE id = $1',
        [decoded.id]
      );

      if (result.rows.length === 0) {
        return res.status(401).json({ success: false, message: 'User not found' });
      }

      req.user = result.rows[0];
      req.user._id = req.user.id;

      if (req.user.role === 'admin') {
        const authRes = await db.query(
          'SELECT name, address, latitude, longitude, rating_score, rating_count FROM ward_authorities WHERE user_id = $1',
          [req.user.id]
        );
        if (authRes.rows.length > 0) {
          const row = authRes.rows[0];
          req.user.authorityDetails = {
            name: row.name,
            address: row.address,
            location: {
              type: 'Point',
              coordinates: [row.longitude, row.latitude],
            },
            rating: {
              score: parseFloat(row.rating_score) || 0,
              count: row.rating_count || 0,
            },
          };
        }
      } else if (req.user.role === 'worker') {
        const workerRes = await db.query(
          'SELECT truck_number, assigned_ward_id, latitude, longitude, status FROM workers WHERE user_id = $1',
          [req.user.id]
        );
        if (workerRes.rows.length > 0) {
          const row = workerRes.rows[0];
          req.user.workerDetails = {
            truckNumber: row.truck_number,
            assignedWard: row.assigned_ward_id,
            location: {
              type: 'Point',
              coordinates: [row.longitude, row.latitude],
            },
            status: row.status,
          };
        }
      }
    } else {
      // MongoDB Atlas Fallback
      req.user = await User.findById(decoded.id).select('-password');
      if (!req.user) {
        return res.status(401).json({ success: false, message: 'User not found' });
      }
    }

    next();
  } catch (err) {
    return res.status(401).json({ success: false, message: 'Token invalid or expired' });
  }
};

const adminOnly = (req, res, next) => {
  if (req.user && req.user.role === 'admin') {
    return next();
  }
  return res.status(403).json({ success: false, message: 'Access denied. Ward Admins only.' });
};

const superAdminOnly = (req, res, next) => {
  if (req.user && req.user.role === 'superadmin') {
    return next();
  }
  return res.status(403).json({ success: false, message: 'Access denied. Central Authority only.' });
};

const workerOnly = (req, res, next) => {
  if (req.user && req.user.role === 'worker') {
    return next();
  }
  return res.status(403).json({ success: false, message: 'Access denied. Workers only.' });
};

module.exports = { protect, adminOnly, superAdminOnly, workerOnly };
