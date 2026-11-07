/**
 * db/seed.js — PostgreSQL Database Seeder for SwachhNet
 * Seeds BMC Ward Authorities, Truck Drivers, Test Citizens, and Superadmin.
 */

const dotenv = require('dotenv');
dotenv.config();

const bcrypt = require('bcryptjs');
const db = require('./index');

const wards = [
  {
    name: 'R/Central Ward (Borivali)',
    email: 'r_central@bmc.gov.in',
    address: 'Chandavarkar Lane, S.V. Road, Borivali (West), Mumbai-400092.',
    lat: 19.2295,
    lng: 72.8573,
  },
  {
    name: 'R/South Ward (Kandivali)',
    email: 'r_south@bmc.gov.in',
    address: 'M.G. Road, Kandivali (West), Mumbai-400067.',
    lat: 19.2084,
    lng: 72.8453,
  },
  {
    name: 'P/North Ward (Malad)',
    email: 'p_north@bmc.gov.in',
    address: 'Mamletdar Wadi Road, Liberty Garden, Malad (West), Mumbai-400064.',
    lat: 19.1860,
    lng: 72.8480,
  },
  {
    name: 'P/South Ward (Goregaon)',
    email: 'p_south@bmc.gov.in',
    address: 'S.V. Road, Goregaon (West), Mumbai-400104.',
    lat: 19.1645,
    lng: 72.8465,
  },
  {
    name: 'K/West Ward (Andheri West)',
    email: 'k_west@bmc.gov.in',
    address: 'S.V. Road, Andheri (West), Mumbai-400058.',
    lat: 19.1136,
    lng: 72.8406,
  },
  {
    name: 'K/East Ward (Andheri East)',
    email: 'k_east@bmc.gov.in',
    address: 'Azad Road, Gundavali, Andheri (East), Mumbai-400069.',
    lat: 19.1155,
    lng: 72.8530,
  },
  {
    name: 'H/West Ward (Bandra)',
    email: 'h_west@bmc.gov.in',
    address: 'St. Martins Road, Behind Bandra Police Station, Bandra (West), Mumbai-400050.',
    lat: 19.0553,
    lng: 72.8335,
  },
  {
    name: 'H/East Ward (Santacruz East)',
    email: 'h_east@bmc.gov.in',
    address: 'Plot No.137, TPS-V, Prabhat Colony, Santacruz (East), Mumbai-400055.',
    lat: 19.0805,
    lng: 72.8455,
  },
];

async function seed() {
  console.log('🌱 Starting PostgreSQL database seeding for SwachhNet...');

  try {
    // 1. Run migrations first to ensure schema exists
    await db.runMigrations();

    const hashedPassword = await bcrypt.hash('password123', 12);

    await db.transaction(async (client) => {
      // Clear existing records
      console.log('🧹 Clearing old tables...');
      await client.query('DELETE FROM complaints');
      await client.query('DELETE FROM workers');
      await client.query('DELETE FROM ward_authorities');
      await client.query('DELETE FROM users');

      // Seed Citizen
      const citizenRes = await client.query(
        `INSERT INTO users (name, email, password, role)
         VALUES ($1, $2, $3, 'user')
         RETURNING id`,
        ['Ramesh Citizen', 'user@test.com', hashedPassword]
      );
      console.log('✅ Created Citizen: user@test.com');

      // Seed Superadmin
      await client.query(
        `INSERT INTO users (name, email, password, role)
         VALUES ($1, $2, $3, 'superadmin')`,
        ['Central Municipal Commissioner', 'central@swachhnet.com', hashedPassword]
      );
      console.log('✅ Created Superadmin: central@swachhnet.com');

      // Seed Ward Authorities
      const createdWardIds = [];
      for (const ward of wards) {
        const adminRes = await client.query(
          `INSERT INTO users (name, email, password, role)
           VALUES ($1, $2, $3, 'admin')
           RETURNING id`,
          ['Admin - ' + ward.name, ward.email, hashedPassword]
        );
        const adminId = adminRes.rows[0].id;

        await client.query(
          `INSERT INTO ward_authorities (user_id, name, address, latitude, longitude, rating_score, rating_count)
           VALUES ($1, $2, $3, $4, $5, $6, $7)`,
          [
            adminId,
            ward.name,
            ward.address,
            ward.lat,
            ward.lng,
            (3.8 + Math.random() * 1.0).toFixed(1),
            Math.floor(20 + Math.random() * 80),
          ]
        );
        createdWardIds.push({ id: adminId, name: ward.name, lat: ward.lat, lng: ward.lng });
      }
      console.log(`✅ Created ${createdWardIds.length} BMC Ward Authorities`);

      // Seed Trucks / Sanitation Workers (4 trucks per ward)
      let workerCount = 1;
      for (const ward of createdWardIds) {
        for (let i = 1; i <= 4; i++) {
          const truckNo = `MH-04-WD-${1000 + workerCount}`;
          const workerRes = await client.query(
            `INSERT INTO users (name, email, password, role)
             VALUES ($1, $2, $3, 'worker')
             RETURNING id`,
            [`Driver ${workerCount} (${ward.name})`, `driver${workerCount}@test.com`, hashedPassword]
          );
          const workerId = workerRes.rows[0].id;

          // Place truck near ward office coordinates
          const offsetLat = ward.lat + (Math.random() - 0.5) * 0.01;
          const offsetLng = ward.lng + (Math.random() - 0.5) * 0.01;

          await client.query(
            `INSERT INTO workers (user_id, truck_number, assigned_ward_id, latitude, longitude, status)
             VALUES ($1, $2, $3, $4, $5, 'idle')`,
            [workerId, truckNo, ward.id, offsetLat, offsetLng]
          );
          workerCount++;
        }
      }
      console.log(`✅ Created ${workerCount - 1} Sanitation Workers / Trucks across all wards`);

      // Seed 1 Sample historical complaint to demonstrate 48h SLA breach detection
      const threeDaysAgo = new Date(Date.now() - 72 * 60 * 60 * 1000);
      await client.query(
        `INSERT INTO complaints (
          user_id, user_name, authority_id, s3_key, image_url,
          latitude, longitude, address, description, status, created_at, updated_at
        ) VALUES (
          $1, $2, $3, $4, $5, $6, $7, $8, $9, 'open', $10, $10
        )`,
        [
          citizenRes.rows[0].id,
          'Ramesh Citizen',
          createdWardIds[2].id, // P/North Malad
          'sample/malad_dump.jpg',
          'https://images.unsplash.com/photo-1530587191325-3db32d826c18?auto=format&fit=crop&w=600&q=80',
          19.1865,
          72.8485,
          'Liberty Garden Lane, Malad West',
          'Severe municipal garbage overflow near market entrance.',
          threeDaysAgo,
        ]
      );
      console.log('✅ Created 1 sample historical SLA-breached complaint for testing');
    });

    console.log('🎉 Seeding successfully completed! Universal password is: password123');
    process.exit(0);
  } catch (err) {
    console.error('❌ Seeding failed:', err.message, err.stack);
    process.exit(1);
  }
}

if (require.main === module) {
  seed();
}

module.exports = seed;

