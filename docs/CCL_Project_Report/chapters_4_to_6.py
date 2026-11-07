# chapters_4_to_6.py
# Detailed chapter texts for Chapter 4, 5, and 6

CH4_CONTENT = {
    "4.1 Overall SwachhNet Cloud Architecture": [
        """The comprehensive cloud architecture of SwachhNet, depicted in Figure 4.1, is engineered following modern AWS Well-Architected Framework guidelines, specifically adhering to the pillars of Security, Reliability, Performance Efficiency, and Cost Optimization.""",
        """At the edge of the architecture, diverse client personas (Citizens, Ward Administrators, Sanitation Truck Drivers, and the Central Municipal Commissioner) access the platform through standard web browsers over HTTPS and HTTP protocols. Inbound client traffic traverses the public internet and enters the AWS Cloud infrastructure through an Amazon Internet Gateway (IGW) attached to the custom Amazon Virtual Private Cloud (VPC), designated as swachhnet-vpc (CIDR: 10.0.0.0/16).""",
        """Within the VPC, network traffic is segregated into discrete security boundaries:""",
        """• Public Subnet (10.0.1.0/24 - Availability Zone ap-south-1a): Houses the unified application compute instance (Amazon EC2 t3.micro, public IP: 65.2.180.175). Inbound access is strictly regulated by the swachhnet-app-sg security group, which permits inbound TCP traffic on ports 80 (HTTP) and 443 (HTTPS) while allowing all outbound traffic to facilitate API communication with external AI services and AWS service endpoints.""",
        """• Inside the EC2 instance, an optimized dual-tier application stack operates: Nginx 1.30 serves pre-rendered static React 18 production assets directly from disk (/var/www/swachhnet/frontend/dist) and acts as a high-speed reverse proxy, forwarding /api/* REST calls to an internal Node.js Express server running on port 5000. Process reliability and auto-restart are governed by PM2 and systemd.""",
        """• Private DB Subnet Group: Comprises two isolated subnets across distinct availability zones: swachhnet-private-subnet-1 (10.0.10.0/24 in ap-south-1a) and swachhnet-private-subnet-2 (10.0.11.0/24 in ap-south-1b). These subnets have no route to the Internet Gateway, rendering them completely inaccessible from the public internet. The primary relational database—Amazon RDS for PostgreSQL 16.10—resides within the private subnet. Access is guarded by the swachhnet-db-sg security group, which strictly permits inbound TCP traffic on port 5432 exclusively originating from members of swachhnet-app-sg.""",
        """• Supporting AWS Managed Services: The compute instance leverages an attached AWS IAM Instance Profile (swachhnet-unified-profile) to securely interact with surrounding AWS services without storing static credentials: (1) Amazon S3 stores citizen and worker evidence photographs with AES-256 server-side encryption; (2) Amazon SQS buffers asynchronous municipal dispatch and audit tasks; (3) AWS SSM Parameter Store delivers encrypted environment secrets at bootstrap; (4) Amazon CloudWatch captures structured runtime logs and metric alarms; and (5) AWS Budgets monitors monthly expenditure."""
    ],
    "4.2 Amazon VPC Network & Subnet Topography": [
        """The network architecture, illustrated in Figure 4.2, establishes a robust perimeter defense through Classless Inter-Domain Routing (CIDR) block partitioning and route table segregation.""",
        """1. VPC Address Space: The VPC is provisioned with a /16 CIDR block (10.0.0.0/16), yielding 65,536 private IPv4 addresses. DNS resolution and DNS hostnames are explicitly enabled (EnableDnsSupport: true, EnableDnsHostnames: true) to allow internal AWS service discovery.""",
        """2. Public Subnet Configuration: A /24 subnet (10.0.1.0/24) is provisioned in the ap-south-1a availability zone. The subnet has MapPublicIpOnLaunch enabled, assigning an Elastic/Public IPv4 address to the EC2 host. Its associated route table (swachhnet-public-rt) contains an explicit default route (0.0.0.0/0) directed to the Internet Gateway.""",
        """3. Private DB Subnet Configuration: Two /24 subnets are created: 10.0.10.0/24 (ap-south-1a) and 10.0.11.0/24 (ap-south-1b). Both subnets are associated with swachhnet-private-rt, which contains solely the local VPC route (10.0.0.0/16 → local). There is no NAT Gateway or Internet Gateway route, physically preventing inbound or outbound internet connections to the database tier, which eliminates database egress costs and eliminates internet attack surfaces.""",
        """4. Security Group Ingress Chaining: Security is implemented as stateful firewalls. The application security group (swachhnet-app-sg) permits internet ingress on web ports. The database security group (swachhnet-db-sg) references the application security group by ID (SourceSecurityGroupId: !Ref AppSecurityGroup), establishing a cryptographic security chain where database packets are accepted solely from the EC2 application host."""
    ],
    "4.3 Multi-Tier Software Architecture": [
        """SwachhNet is structured as a decoupled, four-tier software architecture as illustrated in Figure 4.3:""",
        """1. Presentation Tier (Client Layer): Developed using React 18, Tailwind CSS, and Leaflet. Implements responsive views for citizens, ward admins, workers, and superadmins, communicating with the backend exclusively via asynchronous Axios HTTP REST calls.""",
        """2. Web Gateway & Reverse Proxy Tier: Powered by Nginx 1.30. Handles client connection pooling, static asset delivery with gzip compression, and reverse proxies /api/ requests to the backend application, insulating Node.js from direct internet exposure.""",
        """3. Application & Business Logic Tier: Developed in Node.js and Express.js. Contains domain controllers: AuthController (bcrypt password hashing, JWT signing), ComplaintController (Multer memory uploads, S3 integration, Gemini AI verification), AuthorityController (Haversine spatial calculations, nearest truck matching), and CentralController (48h SLA breach tracking, city metrics).""",
        """4. Persistence & Cloud Services Tier: Amazon RDS PostgreSQL manages relational data integrity; Amazon S3 manages binary image artifacts; Amazon SQS provides asynchronous job queues; AWS SSM delivers encrypted secrets; Amazon CloudWatch captures runtime telemetry; and Google Gemini Vision performs AI image verification."""
    ],
    "4.4 Relational Database Design (PostgreSQL Schema & ERD)": [
        """The relational database schema, illustrated in the Entity-Relationship Diagram (Figure 4.4), was custom-designed to replace the original unstructured MongoDB collections, enforcing strict referential integrity, check constraints, and indexing.""",
        """The schema comprises five normalized relational tables:""",
        """• users: Central identity table. Primary key id (UUID, default gen_random_uuid()). Stores user name, unique email, bcrypt-hashed password, role (enforced via CHECK constraint IN ('user', 'admin', 'worker', 'superadmin')), and timestamps. B-tree indexes are applied on email and role.""",
        """• ward_authorities: Stores administrative BMC ward metadata. Primary key user_id references users(id) with ON DELETE CASCADE. Stores ward name (e.g., 'K/West Ward (Andheri West)'), civic office address, geographic office latitude and longitude (DOUBLE PRECISION), aggregate rating score (NUMERIC(3,2)), and rating count.""",
        """• workers: Manages municipal sanitation trucks and driver assignments. Primary key user_id references users(id). Stores vehicle registration truck_number (VARCHAR(64)), assigned_ward_id referencing users(id), real-time truck GPS coordinates (latitude, longitude), and status (CHECK constraint IN ('idle', 'busy')). A composite B-tree index idx_workers_ward_status optimizes Haversine nearest truck queries.""",
        """• complaints: Core transactional entity. Primary key id (UUID). Captures user_id, authority_id, optional worker_id, private S3 object keys (s3_key and after_s3_key), geographic coordinates (latitude, longitude), street address, status (CHECK constraint IN ('open', 'assigned', 'pending_verification', 'resolved', 'rejected')), citizen description, feedback rating (INT CHECK 1-5), and rating comments. Indexed by user_id, authority_id, worker_id, status, and created_at.""",
        """• complaint_transfers: Immutable audit log tracking inter-ward jurisdictional transfers. Primary key id (BIGSERIAL). Foreign key complaint_id references complaints(id) ON DELETE CASCADE. Records from_authority_name, to_authority_name, and timestamp."""
    ],
    "4.5 UML Use Case Modeling": [
        """Figure 4.5 delineates the functional boundaries and interactions across the four primary system actors:""",
        """• Citizen Actor: Interacts with use cases UC1 (Register & Login), UC2 (Report Garbage Photo & GPS), UC3 (Track Complaint Status), and UC4 (Give Feedback & Earn Eco-Points).""",
        """• Ward Administrator Actor: Interacts with UC5 (View Ward Complaints), UC6 (Dispatch Nearest Truck via Haversine), and UC7 (Transfer Out-of-Boundary Complaints).""",
        """• Sanitation Worker Actor: Engages with UC8 (View Assigned Jobs), UC9 (Upload Cleanup Proof Photo), and UC10 (Update Truck Availability Status).""",
        """• Central Superadmin Actor: Manages high-level civic oversight via UC11 (Monitor 48h SLA Breaches), UC12 (View City-Wide Ward Analytics), and UC13 (Inspect CloudWatch Audit Telemetry)."""
    ],
    "4.6 Data Flow Modeling (Level 0 Context & Level 1 DFD)": [
        """The data flow architecture is modeled at two hierarchical abstractions:""",
        """• Level 0 Context Diagram (Figure 4.6): Depicts the central SwachhNet Cloud Platform interacting with five external entities: Citizens (submitting image and GPS data; receiving status and gamification rewards), Ward Administrators (receiving ward complaints; issuing dispatch orders), Sanitation Workers (receiving navigation tasks; returning cleanup photos), Central Authorities (receiving city metrics and breach alerts), and Cloud/AI Services (storing objects, validating images, and querying relational data).""",
        """• Level 1 DFD (Figure 4.7): Decomposes the platform into five coordinated functional processes: Process 1.0 (Authentication & RBAC), Process 2.0 (Photo Ingestion & AI Verification), Process 3.0 (Geospatial Dispatch Engine), Process 4.0 (Cleanup Verification & Gamification), and Process 5.0 (SLA Tracking & Audit Logging). Each process interfaces with discrete data stores (D1: RDS Users, D2: RDS Complaints, D3: S3 Evidence, D4: CloudWatch Logs)."""
    ],
    "4.7 Core Municipal Workflows": [
        """The system executes three specialized municipal workflows:""",
        """1. Citizen Complaint Lifecycle (Figure 4.8): Traces a report from initial citizen camera capture, through Gemini AI spam filtering, S3 upload, Haversine ward routing, truck assignment, worker cleanup, before/after comparative AI verification, and final citizen eco-point allocation.""",
        """2. Geospatial Nearest Truck Dispatch (Figure 4.9): Details how the ward administrator executes a single-click dispatch, triggering a mathematical Haversine SQL query across all idle trucks in the ward and executing an atomic database transaction updating complaint and vehicle states simultaneously.""",
        """3. Photographic Cleanup Verification (Figure 4.10): Outlines the verification pipeline where worker cleanup evidence uploaded to S3 is paired with the original complaint image and submitted to Google Gemini Vision for differential cleanliness verification.""",
        """4. 48-Hour SLA Breach Escalation (Figure 4.11): Details the periodic execution of check-sla.js, which evaluates unresolved complaints older than 48 hours, increments city-wide breach counters, alerts administrators, and emits structured audit logs to CloudWatch."""
    ]
}

# -------------------------------------------------------------
# CHAPTER 5: AWS CLOUD SERVICES INTEGRATION
# -------------------------------------------------------------
AWS_SERVICES_TABLE = [
    ("Amazon VPC", "Custom isolated virtual network (10.0.0.0/16)", "Attached to IGW, Public Subnet & Private DB Subnets", "Networking & Perimeter Security", "AWS Console: VPC Dashboard; Route Tables"),
    ("Amazon EC2", "Virtual application compute host (t3.micro)", "Runs Amazon Linux 2023, Nginx 1.30, Node.js 18 & PM2", "Compute & Application Hosting", "AWS Console: EC2 Dashboard; Public IP 65.2.180.175"),
    ("Amazon RDS", "Managed PostgreSQL 16.10 relational database", "Housed in Private DB Subnet Group; Port 5432 ingress", "Primary Application Persistence", "AWS Console: RDS Databases; swachhnet-postgres"),
    ("Amazon S3", "Private encrypted object storage bucket", "Integrated via AWS SDK v3 with 60-min presigned URLs", "Evidence Media Storage (Photos)", "AWS Console: S3 Buckets; swachhnet-evidence-*"),
    ("AWS IAM", "Least-privilege role & instance profile", "Attached to EC2; grants S3, SQS, SSM & CloudWatch rights", "Security & Access Control", "AWS Console: IAM Roles; swachhnet-unified-role"),
    ("AWS SSM", "Centralized Parameter Store (SecureString)", "Loaded at server bootstrap; stores DB URL, JWT & API keys", "Configuration & Secrets Management", "AWS Console: Systems Manager Parameter Store"),
    ("Amazon SQS", "Decoupled asynchronous message queue & DLQ", "Buffers background tasks; DLQ maxReceiveCount: 5", "Asynchronous Task Processing", "AWS Console: SQS Queues; swachhnet-jobs-queue"),
    ("Amazon CloudWatch", "Centralized logging and CPU utilization alarm", "Streams runtime logs (/swachhnet/backend); 80% CPU alarm", "Monitoring & Telemetry", "AWS Console: CloudWatch Log Groups & Alarms"),
    ("AWS Budgets", "Financial governance and cost ceiling alert", "Enforces $10.00/month limit; triggers at 80% ($8.00)", "Cost Management & Governance", "AWS Console: Budgets Dashboard; SwachhNet-Budget"),
    ("AWS CloudFormation", "Declarative Infrastructure as Code (IaC)", "Provisions all 24 AWS resources via single YAML template", "Automation & Deployment", "AWS Console: CloudFormation; swachhnet-prod-stack")
]

# -------------------------------------------------------------
# CHAPTER 6: IMPLEMENTATION & WORKING (CODE SNIPPETS)
# -------------------------------------------------------------
CODE_SNIPPETS = {
    "server_bootstrap": """// backend/server.js - Dual-Database Bootstrap & SSM Parameter Integration
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
dotenv.config();

const db = require('./db');
const { loadParametersFromSSM } = require('./services/ssmService');
const { startSqsWorker } = require('./services/sqsService');
const logger = require('./services/logger');

const app = express();
app.use(cors({ origin: (orig, cb) => cb(null, true), credentials: true }));
app.use(express.json());

// Load production parameters from AWS SSM Parameter Store if enabled
if (process.env.USE_SSM === 'true') {
  loadParametersFromSSM().then(() => {
    logger.info('✅ Production parameters successfully loaded from AWS SSM Parameter Store');
  }).catch(err => {
    logger.error('❌ Failed to load SSM parameters:', err);
  });
}

// Database Connection Lifecycle
if (process.env.DATABASE_URL || process.env.PGHOST) {
  logger.info('🐘 Active Database Engine: Amazon RDS PostgreSQL');
  db.query('SELECT NOW()').then(() => {
    logger.info('✅ Amazon RDS PostgreSQL connection pool healthy');
  });
} else if (process.env.MONGO_URI) {
  logger.info('🍃 Fallback Database Engine: MongoDB Atlas');
  mongoose.connect(process.env.MONGO_URI);
}

// Start SQS Background Consumer Worker
if (process.env.SQS_QUEUE_URL) {
  startSqsWorker();
}""",

    "s3_presigned": """// backend/services/s3Service.js - S3 Direct Upload & Presigned URL Resolution
const { S3Client, PutObjectCommand, GetObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
const { randomUUID: uuidv4 } = require('crypto');

const region = process.env.AWS_REGION || 'ap-south-1';
const bucketName = process.env.S3_BUCKET_NAME;
const s3Client = new S3Client({ region });

async function uploadToS3(buffer, originalName, mimeType, folder = 'complaints') {
  const extension = originalName.split('.').pop() || 'jpg';
  const s3Key = `${folder}/${uuidv4()}.${extension}`;

  const command = new PutObjectCommand({
    Bucket: bucketName,
    Key: s3Key,
    Body: buffer,
    ContentType: mimeType,
    ServerSideEncryption: 'AES256',
  });

  await s3Client.send(command);
  const presignedUrl = await getPresignedDownloadUrl(s3Key);
  return { s3Key, bucket: bucketName, url: presignedUrl };
}

async function getPresignedDownloadUrl(s3Key, expiresInSeconds = 3600) {
  if (!s3Key) return null;
  const command = new GetObjectCommand({ Bucket: bucketName, Key: s3Key });
  return await getSignedUrl(s3Client, command, { expiresIn: expiresInSeconds });
}""",

    "haversine_dispatch": """// backend/controllers/authorityController.js - Haversine Nearest Truck Dispatch
// Haversine formula calculates great-circle distance between two GPS coordinates in kilometers
const dispatchQuery = `
  SELECT 
    w.user_id,
    w.truck_number,
    w.latitude,
    w.longitude,
    (6371 * acos(
      cos(radians($1)) * cos(radians(w.latitude)) *
      cos(radians(w.longitude) - radians($2)) +
      sin(radians($1)) * sin(radians(w.latitude))
    )) AS distance_km
  FROM workers w
  WHERE w.assigned_ward_id = $3 AND w.status = 'idle'
  ORDER BY distance_km ASC
  LIMIT 1;
`;

// Atomic transaction: assign nearest truck and mark truck busy simultaneously
await db.transaction(async (client) => {
  const truckRes = await client.query(dispatchQuery, [complaintLat, complaintLng, wardId]);
  if (truckRes.rows.length === 0) {
    throw new Error('No idle trucks currently available in this ward');
  }
  const assignedWorker = truckRes.rows[0];

  await client.query(
    `UPDATE complaints SET worker_id = $1, status = 'assigned', updated_at = NOW() WHERE id = $2`,
    [assignedWorker.user_id, complaintId]
  );
  await client.query(
    `UPDATE workers SET status = 'busy' WHERE user_id = $1`,
    [assignedWorker.user_id]
  );
});""",

    "gemini_verification": """// backend/controllers/complaintController.js - Gemini Vision AI Verification
const { GoogleGenerativeAI } = require('@google/generative-ai');
const genAI = new GoogleGenerativeAI(process.env.G_API);

async function validateGarbageImageWithAI(imageBuffer, mimeType) {
  const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
  const prompt = `Analyze this image and determine if it shows uncollected garbage, litter,
                  overflowing dumpsters, or civic waste heaps.
                  Respond with valid JSON: { "isGarbage": boolean, "confidence": number, "reason": string }`;

  const imagePart = {
    inlineData: { data: imageBuffer.toString('base64'), mimeType }
  };

  const result = await model.generateContent([prompt, imagePart]);
  const response = await result.response;
  return JSON.parse(response.text().trim());
}""",

    "cloudwatch_logger": """// backend/services/logger.js - CloudWatch Structured Logging with PII Sanitization
const { CloudWatchLogsClient, PutLogEventsCommand } = require('@aws-sdk/client-cloudwatch-logs');
const cwClient = new CloudWatchLogsClient({ region: 'ap-south-1' });

function sanitize(data) {
  if (typeof data !== 'string') data = JSON.stringify(data);
  return data
    .replace(/"password":\\s*"[^"]*"/gi, '"password":"***REDACTED***"')
    .replace(/"token":\\s*"[^"]*"/gi, '"token":"***REDACTED***"')
    .replace(/"DATABASE_URL":\\s*"[^"]*"/gi, '"DATABASE_URL":"***REDACTED***"');
}

async function logToCloudWatch(level, message, metadata = {}) {
  const timestamp = Date.now();
  const logMessage = `[${level.toUpperCase()}] ${message} | ${sanitize(metadata)}`;
  
  console.log(logMessage);
  if (process.env.ENABLE_CLOUDWATCH_LOGS === 'true') {
    await cwClient.send(new PutLogEventsCommand({
      logGroupName: '/swachhnet/backend',
      logStreamName: process.env.CLOUDWATCH_LOG_STREAM,
      logEvents: [{ message: logMessage, timestamp }]
    }));
  }
}"""
}

