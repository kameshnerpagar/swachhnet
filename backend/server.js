/**
 * server.js — Entry point for SwachhNet API
 * Dual Database Architecture: Supports Amazon RDS PostgreSQL (Production Cloud)
 * and MongoDB Atlas (Local Development & Fallback).
 */

const dotenv = require('dotenv');
// Load environment variables immediately before requiring services
dotenv.config();

const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const db = require('./db');
const { loadParametersFromSSM } = require('./services/ssmService');
const { startSqsWorker } = require('./services/sqsService');
const logger = require('./services/logger');

const app = express();

// ─── Middleware ───────────────────────────────────────────────────────────────
app.use(cors({
  origin: (origin, callback) => {
    // Allow any origin and reflect it so Access-Control-Allow-Origin matches origin with credentials: true
    callback(null, true);
  },
  credentials: true,
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    if (req.originalUrl !== '/health') {
      logger.info(`${req.method} ${req.originalUrl} ${res.statusCode} - ${duration}ms`);
    }
  });
  next();
});

// ─── Routes ───────────────────────────────────────────────────────────────────
const authRoutes = require('./routes/auth');
const complaintRoutes = require('./routes/complaints');
const authorityRoutes = require('./routes/authorityRoutes');
const centralRoutes = require('./routes/central');

app.use('/api/auth', authRoutes);
app.use('/api/complaints', complaintRoutes);
app.use('/api/authorities', authorityRoutes);
app.use('/api/central', centralRoutes);

// Health check endpoint
app.get(['/', '/health', '/api/health'], async (req, res) => {
  const isPostgres = Boolean(process.env.DATABASE_URL || process.env.PGHOST);
  let dbStatus = 'healthy';
  let dbEngine = isPostgres ? 'PostgreSQL (Amazon RDS)' : 'MongoDB Atlas';

  try {
    if (isPostgres) {
      await db.query('SELECT 1');
    } else {
      if (mongoose.connection.readyState !== 1) {
        dbStatus = 'disconnected';
      }
    }
  } catch (err) {
    dbStatus = `unhealthy: ${err.message}`;
  }

  res.status(dbStatus === 'healthy' ? 200 : 503).json({
    status: dbStatus === 'healthy' ? 'OK' : 'ERROR',
    service: 'SwachhNet Municipal API',
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    database: {
      engine: dbEngine,
      status: dbStatus,
    },
    aws: {
      region: process.env.AWS_REGION || 'ap-south-1',
      s3Bucket: process.env.S3_BUCKET_NAME || 'configured',
    },
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ success: false, message: 'Route not found' });
});

// Global error handler
app.use((err, req, res, next) => {
  logger.error(`Unhandled Server Error: ${err.message}`, { stack: err.stack });
  res.status(500).json({ success: false, message: err.message || 'Internal Server Error' });
});

// ─── Server Startup ───────────────────────────────────────────────────────────
const PORT = process.env.PORT || 5000;

async function bootstrap() {
  try {
    // 1. Optionally load secrets from AWS SSM Parameter Store if enabled
    await loadParametersFromSSM();

    const isPostgres = Boolean(process.env.DATABASE_URL || process.env.PGHOST);

    if (isPostgres) {
      logger.info('🐘 Connecting to Amazon RDS / PostgreSQL...');
      await db.runMigrations();
      logger.info('✅ Connected to PostgreSQL successfully.');
    } else if (process.env.MONGO_URI) {
      logger.info('🍃 Connecting to MongoDB Atlas...');
      await mongoose.connect(process.env.MONGO_URI);
      logger.info('✅ Connected to MongoDB Atlas successfully.');
    } else {
      throw new Error('No database configured. Please provide DATABASE_URL (PostgreSQL) or MONGO_URI in .env');
    }

    // 2. Start SQS background worker if configured
    startSqsWorker(async (job) => {
      logger.info(`[SQS Background Worker] Processing job: ${job.jobType}`, job.payload);
    });

    // 3. Start HTTP server
    app.listen(PORT, '0.0.0.0', () => {
      logger.info(`🚀 SwachhNet API running on http://localhost:${PORT}`);
    });
  } catch (err) {
    logger.error(`❌ Startup Failure: ${err.message}`, { stack: err.stack });
    process.exit(1);
  }
}

bootstrap();

module.exports = app;
