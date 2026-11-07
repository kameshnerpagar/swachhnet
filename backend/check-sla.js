/**
 * check-sla.js — Standalone 48-Hour SLA Breach Diagnostic Script
 * Checks PostgreSQL for active complaints exceeding the 48-hour municipal SLA window.
 */

const dotenv = require('dotenv');
dotenv.config();

const db = require('./db');

async function checkSLA() {
  console.log('🔍 Checking SwachhNet Municipal 48-hour SLA status...');
  const fortyEightHoursAgo = new Date(Date.now() - 48 * 60 * 60 * 1000);

  try {
    const totalActiveRes = await db.query(
      `SELECT COUNT(*) FROM complaints WHERE status IN ('open', 'assigned', 'pending_verification')`
    );
    const totalActive = parseInt(totalActiveRes.rows[0].count);

    const breachedRes = await db.query(
      `SELECT c.id, c.status, c.created_at, c.address, u.name AS ward_name
       FROM complaints c
       JOIN users u ON u.id = c.authority_id
       WHERE c.status IN ('open', 'assigned', 'pending_verification')
       AND c.created_at < $1
       ORDER BY c.created_at ASC`,
      [fortyEightHoursAgo]
    );

    console.log(`📊 Total Active Complaints: ${totalActive}`);
    console.log(`⚠️ Breached Complaints (>48 hours): ${breachedRes.rows.length}`);

    if (breachedRes.rows.length > 0) {
      console.log('\n--- Sample SLA Breaches ---');
      breachedRes.rows.forEach((row, i) => {
        console.log(`[#${i + 1}] ID: ${row.id} | Ward: ${row.ward_name} | Status: ${row.status} | Filed: ${row.created_at}`);
      });
    }

    process.exit(0);
  } catch (err) {
    console.error('❌ Error checking SLA:', err.message);
    process.exit(1);
  }
}

checkSLA();
