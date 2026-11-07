/**
 * services/s3Service.js — Amazon S3 Integration for SwachhNet
 * Handles private S3 uploads, deletions, and presigned GET URL generation.
 */

const { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
const { randomUUID: uuidv4 } = require('crypto');

const region = process.env.AWS_REGION || process.env.AWS_DEFAULT_REGION || 'ap-south-1';
const bucketName = process.env.S3_BUCKET_NAME || 'swachhnet-evidence-storage';

// Initialize S3 client. When running on EC2, credentials come automatically from IAM Instance Profile.
// When running locally, it picks up standard AWS credentials or environment variables.
const s3Client = new S3Client({
  region,
});

/**
 * Upload a file buffer directly to Amazon S3
 * @param {Buffer} buffer - File buffer
 * @param {string} originalName - Original filename
 * @param {string} mimeType - Image MIME type (e.g., 'image/jpeg')
 * @param {string} folder - Destination folder (e.g., 'complaints' or 'cleanup')
 * @returns {Promise<{ s3Key: string, bucket: string, url: string }>}
 */
async function uploadToS3(buffer, originalName, mimeType = 'image/jpeg', folder = 'complaints') {
  // If no S3 bucket configured or in mock/offline mode without AWS
  if (process.env.USE_MOCK_STORAGE === 'true' || !process.env.S3_BUCKET_NAME) {
    const mockKey = `${folder}/${Date.now()}-${originalName || 'image.jpg'}`;
    return {
      s3Key: mockKey,
      bucket: bucketName,
      url: `https://${bucketName}.s3.${region}.amazonaws.com/${mockKey}`,
    };
  }

  const extension = originalName ? originalName.split('.').pop() : 'jpg';
  const s3Key = `${folder}/${uuidv4()}.${extension}`;

  const command = new PutObjectCommand({
    Bucket: bucketName,
    Key: s3Key,
    Body: buffer,
    ContentType: mimeType,
    ServerSideEncryption: 'AES256',
  });

  await s3Client.send(command);

  // Generate an initial presigned GET URL valid for 1 hour (3600 seconds)
  const presignedUrl = await getPresignedDownloadUrl(s3Key);

  return {
    s3Key,
    bucket: bucketName,
    url: presignedUrl,
  };
}

/**
 * Generate a short-lived presigned URL for downloading a private S3 object
 * @param {string} s3Key - S3 object key
 * @param {number} expiresIn - Expiration in seconds (default 3600 = 1 hr)
 * @returns {Promise<string>} Presigned URL
 */
async function getPresignedDownloadUrl(s3Key, expiresIn = 3600) {
  if (!s3Key) return null;
  // If already an absolute http/https URL (e.g. legacy Cloudinary), return as is
  if (s3Key.startsWith('http://') || s3Key.startsWith('https://')) {
    return s3Key;
  }

  if (process.env.USE_MOCK_STORAGE === 'true' || !process.env.S3_BUCKET_NAME) {
    return `https://${bucketName}.s3.${region}.amazonaws.com/${s3Key}`;
  }

  const command = new GetObjectCommand({
    Bucket: bucketName,
    Key: s3Key,
  });

  return await getSignedUrl(s3Client, command, { expiresIn });
}

/**
 * Fetch object byte buffer from S3 (used for AI validation)
 * @param {string} s3Key
 * @returns {Promise<Buffer>}
 */
async function getObjectBuffer(s3Key) {
  const command = new GetObjectCommand({
    Bucket: bucketName,
    Key: s3Key,
  });

  const response = await s3Client.send(command);
  const streamToBuffer = async (stream) => {
    const chunks = [];
    for await (const chunk of stream) {
      chunks.push(chunk);
    }
    return Buffer.concat(chunks);
  };

  return await streamToBuffer(response.Body);
}

/**
 * Delete an object from Amazon S3
 * @param {string} s3Key - S3 object key
 */
async function deleteFromS3(s3Key) {
  if (!s3Key || s3Key.startsWith('http://') || s3Key.startsWith('https://')) return;
  if (process.env.USE_MOCK_STORAGE === 'true' || !process.env.S3_BUCKET_NAME) return;

  try {
    const command = new DeleteObjectCommand({
      Bucket: bucketName,
      Key: s3Key,
    });
    await s3Client.send(command);
  } catch (err) {
    console.error(`⚠️ S3 Deletion warning for ${s3Key}:`, err.message);
  }
}

module.exports = {
  s3Client,
  uploadToS3,
  getPresignedDownloadUrl,
  getObjectBuffer,
  deleteFromS3,
};

