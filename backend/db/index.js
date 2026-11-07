/**
 * db/index.js — PostgreSQL Connection Pool & Query Interface
 * Supports Amazon RDS PostgreSQL with SSL and local PostgreSQL development.
 */

const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

let pool = null;

function getPool() {
  if (!pool) {
    const config = {
      connectionString: process.env.DATABASE_URL,
      host: process.env.PGHOST,
      port: process.env.PGPORT ? parseInt(process.env.PGPORT) : 5432,
      database: process.env.PGDATABASE,
      user: process.env.PGUSER,
      password: process.env.PGPASSWORD,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 5000,
    };

    // If connecting to RDS or if PGSSL=true is requested, enable SSL
    if (process.env.PGSSL === 'true' || (process.env.DATABASE_URL && process.env.DATABASE_URL.includes('rds.amazonaws.com'))) {
      config.ssl = { rejectUnauthorized: false };
    }

    pool = new Pool(config);

    pool.on('error', (err) => {
      console.error('❌ Unexpected PostgreSQL pool error:', err.message);
    });
  }
  return pool;
}

/**
 * Execute a query with parameterized values
 */
async function query(text, params) {
  const start = Date.now();
  const client = getPool();
  try {
    const res = await client.query(text, params);
    const duration = Date.now() - start;
    if (process.env.NODE_ENV !== 'production' && duration > 500) {
      console.log(`⏱️ Slow query (${duration}ms):`, text.substring(0, 80));
    }
    return res;
  } catch (err) {
    console.error(`❌ DB Query Error on [${text.substring(0, 60)}]:`, err.message);
    throw err;
  }
}

/**
 * Execute multiple queries within a database transaction
 */
async function transaction(callback) {
  const client = await getPool().connect();
  try {
    await client.query('BEGIN');
    const result = await callback(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

/**
 * Run migration files on startup
 */
async function runMigrations() {
  const migrationsDir = path.join(__dirname, 'migrations');
  if (!fs.existsSync(migrationsDir)) return;

  const files = fs.readdirSync(migrationsDir).filter(f => f.endsWith('.sql')).sort();
  for (const file of files) {
    const sql = fs.readFileSync(path.join(migrationsDir, file), 'utf8');
    console.log(`🔄 Applying migration: ${file}...`);
    await query(sql);
  }
  console.log('✅ PostgreSQL migrations applied successfully');
}

module.exports = {
  getPool,
  query,
  transaction,
  runMigrations,
};

