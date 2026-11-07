/**
 * controllers/authController.js — User Registration & Authentication
 * Dual-Database Engine: Supports PostgreSQL (Amazon RDS) & MongoDB Atlas (Local Development).
 */

const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const db = require('../db');
const User = require('../models/User');
const logger = require('../services/logger');

const isPostgres = () => Boolean(process.env.DATABASE_URL || process.env.PGHOST);

// Generate JWT token valid for 7 days
const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET || 'fallback_secret_for_local_testing_only', {
    expiresIn: '7d',
  });
};

/**
 * POST /api/auth/register
 */
const register = async (req, res) => {
  try {
    const {
      name,
      email,
      password,
      role = 'user',
      authorityName,
      latitude,
      longitude,
      address,
      truckNumber,
      garageName,
    } = req.body;

    if (!name || !email || !password) {
      return res.status(400).json({ success: false, message: 'Name, email, and password are required' });
    }

    if (password.length < 6) {
      return res.status(400).json({ success: false, message: 'Password must be at least 6 characters' });
    }

    if (isPostgres()) {
      // ── PostgreSQL (Amazon RDS) ───────────────────────────────────────────
      const existing = await db.query('SELECT id FROM users WHERE LOWER(email) = LOWER($1)', [email.trim()]);
      if (existing.rows.length > 0) {
        return res.status(409).json({ success: false, message: 'Email already registered' });
      }

      const hashedPassword = await bcrypt.hash(password, 12);

      const newUser = await db.transaction(async (client) => {
        const userRes = await client.query(
          `INSERT INTO users (name, email, password, role)
           VALUES ($1, $2, $3, $4)
           RETURNING id, name, email, role, created_at`,
          [name.trim(), email.toLowerCase().trim(), hashedPassword, role]
        );
        const user = userRes.rows[0];

        if (role === 'admin') {
          if (!latitude || !longitude) {
            throw new Error('Latitude and Longitude are required for Ward Authority accounts');
          }
          await client.query(
            `INSERT INTO ward_authorities (user_id, name, address, latitude, longitude)
             VALUES ($1, $2, $3, $4, $5)`,
            [user.id, authorityName || name, address || '', parseFloat(latitude), parseFloat(longitude)]
          );
        } else if (role === 'worker') {
          if (!latitude || !longitude || !truckNumber) {
            throw new Error('Latitude, Longitude, and Truck Number are required for Worker accounts');
          }
          await client.query(
            `INSERT INTO workers (user_id, truck_number, latitude, longitude, status)
             VALUES ($1, $2, $3, $4, 'idle')`,
            [user.id, truckNumber, parseFloat(latitude), parseFloat(longitude)]
          );
        }

        return user;
      });

      logger.info(`[PostgreSQL] User registered successfully: ${newUser.email}`);

      return res.status(201).json({
        success: true,
        message: 'Account created successfully',
        token: generateToken(newUser.id),
        user: {
          id: newUser.id,
          _id: newUser.id,
          name: newUser.name,
          email: newUser.email,
          role: newUser.role,
        },
      });
    } else {
      // ── MongoDB Atlas Fallback ────────────────────────────────────────────
      const existingUser = await User.findOne({ email: email.toLowerCase().trim() });
      if (existingUser) {
        return res.status(409).json({ success: false, message: 'Email already registered' });
      }

      const userData = {
        name: name.trim(),
        email: email.toLowerCase().trim(),
        password, // hashed automatically by User.js pre-save hook
        role,
      };

      if (role === 'admin') {
        if (!latitude || !longitude) {
          return res.status(400).json({ success: false, message: 'Location is required for an Authority account' });
        }
        userData.authorityDetails = {
          name: authorityName || name,
          location: {
            type: 'Point',
            coordinates: [parseFloat(longitude), parseFloat(latitude)],
            address: address || '',
          },
          rating: { score: 0, count: 0 },
        };
      } else if (role === 'worker') {
        if (!latitude || !longitude || !truckNumber) {
          return res.status(400).json({ success: false, message: 'Location and truck number are required for Worker' });
        }
        userData.workerDetails = {
          truckNumber,
          garageName: garageName || 'General Garage',
          location: {
            type: 'Point',
            coordinates: [parseFloat(longitude), parseFloat(latitude)],
          },
          status: 'idle',
        };
      }

      const user = await User.create(userData);
      logger.info(`[MongoDB] User registered successfully: ${user.email}`);

      return res.status(201).json({
        success: true,
        message: 'Account created successfully',
        token: generateToken(user._id),
        user: {
          id: user._id,
          _id: user._id,
          name: user.name,
          email: user.email,
          role: user.role,
        },
      });
    }
  } catch (err) {
    logger.error(`Registration error: ${err.message}`);
    res.status(400).json({ success: false, message: err.message });
  }
};

/**
 * POST /api/auth/login
 */
const login = async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ success: false, message: 'Email and password required' });
    }

    if (isPostgres()) {
      // ── PostgreSQL ────────────────────────────────────────────────────────
      const userRes = await db.query(
        'SELECT id, name, email, password, role FROM users WHERE LOWER(email) = LOWER($1)',
        [email.trim()]
      );

      if (userRes.rows.length === 0) {
        return res.status(401).json({ success: false, message: 'Invalid email or password' });
      }

      const user = userRes.rows[0];
      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        return res.status(401).json({ success: false, message: 'Invalid email or password' });
      }

      logger.info(`[PostgreSQL] Login successful: ${user.email}`);
      return res.json({
        success: true,
        message: 'Login successful',
        token: generateToken(user.id),
        user: {
          id: user.id,
          _id: user.id,
          name: user.name,
          email: user.email,
          role: user.role,
        },
      });
    } else {
      // ── MongoDB Atlas Fallback ────────────────────────────────────────────
      const user = await User.findOne({ email: email.toLowerCase().trim() });
      if (!user) {
        return res.status(401).json({ success: false, message: 'Invalid email or password' });
      }

      const isMatch = await user.comparePassword(password);
      if (!isMatch) {
        return res.status(401).json({ success: false, message: 'Invalid email or password' });
      }

      logger.info(`[MongoDB] Login successful: ${user.email}`);
      return res.json({
        success: true,
        message: 'Login successful',
        token: generateToken(user._id),
        user: {
          id: user._id,
          _id: user._id,
          name: user.name,
          email: user.email,
          role: user.role,
        },
      });
    }
  } catch (err) {
    logger.error(`Login error: ${err.message}`);
    res.status(500).json({ success: false, message: err.message });
  }
};

/**
 * GET /api/auth/me
 */
const getMe = async (req, res) => {
  res.json({ success: true, user: req.user });
};

module.exports = { register, login, getMe };
