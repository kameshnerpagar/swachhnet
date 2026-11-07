/**
 * routes/complaints.js — Complaint management routes
 * Uses memory storage upload for direct S3 upload & verification
 */

const express = require('express');
const router = express.Router();
const { upload } = require('../middleware/s3Upload');
const { protect, adminOnly, workerOnly } = require('../middleware/auth');
const {
  createComplaint,
  getUserComplaints,
  getAllComplaints,
  getComplaintById,
  getWorkerComplaints,
  assignTruck,
  transferComplaint,
  workerSubmit,
  verifyComplaint,
  rejectComplaint,
} = require('../controllers/complaintController');

// User routes (any authenticated user)
router.post('/', protect, upload.single('image'), createComplaint);
router.get('/user', protect, getUserComplaints);

// Worker routes
router.get('/worker', protect, workerOnly, getWorkerComplaints);
router.post('/:id/worker-submit', protect, workerOnly, upload.single('image'), workerSubmit);

// Admin-only routes
router.get('/all', protect, adminOnly, getAllComplaints);
router.post('/:id/assign-truck', protect, adminOnly, assignTruck);
router.patch('/:id/transfer', protect, adminOnly, transferComplaint);
router.patch('/:id/verify', protect, adminOnly, verifyComplaint);
router.patch('/:id/reject', protect, adminOnly, rejectComplaint);

// Single complaint (authenticated)
router.get('/:id', protect, getComplaintById);

module.exports = router;
