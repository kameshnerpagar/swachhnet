/**
 * middleware/s3Upload.js — Multer Memory Storage for Direct S3 Uploads
 * Replaces Cloudinary with private Amazon S3 storage.
 */

const multer = require('multer');

// Store uploaded files in memory buffer for direct streaming to S3 and Gemini AI
const storage = multer.memoryStorage();

const upload = multer({
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5 MB limit
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'), false);
    }
  },
});

module.exports = { upload };

