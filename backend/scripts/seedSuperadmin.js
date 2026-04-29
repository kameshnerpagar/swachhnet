const mongoose = require('mongoose');
const dotenv = require('dotenv');
// Fix path relative to execution
const path = require('path');
dotenv.config({ path: path.join(__dirname, '../.env') });
const User = require('../models/User');

const seedSuperadmin = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    
    const existing = await User.findOne({ role: 'superadmin' });
    if (existing) {
      console.log('Superadmin already exists! Email:', existing.email);
      process.exit(0);
    }

    const superadmin = new User({
      name: 'Central Authority',
      email: 'central@swachhnet.com',
      password: 'password123', // Will be hashed by pre-save hook
      role: 'superadmin'
    });

    await superadmin.save();
    console.log('✅ Superadmin created successfully!');
    console.log('Email: central@swachhnet.com');
    console.log('Password: password123');
    
    process.exit(0);
  } catch (err) {
    console.error('Failed to create superadmin:', err.message);
    process.exit(1);
  }
};

seedSuperadmin();
