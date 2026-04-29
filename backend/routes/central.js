const express = require('express');
const router = express.Router();
const { protect, superAdminOnly } = require('../middleware/auth');
const { getCentralDashboard } = require('../controllers/centralController');

router.get('/dashboard', protect, superAdminOnly, getCentralDashboard);

module.exports = router;
