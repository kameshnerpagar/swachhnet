# SwachhNet — Smart Garbage Reporting & Municipal Dispatch System
### Cloud Computing Lab (CCL) Mini-Project — Enterprise AWS Cloud Architecture

SwachhNet is an enterprise municipal solid waste management, AI verification, and fleet dispatch platform modeled around the administrative structure of the **Brihanmumbai Municipal Corporation (BMC)**. 

Originally developed with local tools, the platform has been fully migrated to a resilient, secure, and cost-effective cloud architecture on **Amazon Web Services (AWS)**.

---

## 1. Key Features Preserved & Enhanced

* **Citizen Experience:** GPS-assisted report filing (auto-detect or Leaflet map pin), in-browser camera capture, Google Gemini AI garbage validation (anti-spam), 6-tier gamification rewards (points, levels, badges), and ward feedback.
* **Ward Admin Governance:** Scoped complaint tracking across 8 BMC wards, automatic nearest-truck dispatching via spherical Haversine distance math, inter-ward transfers with audit logging, and side-by-side Before/After cleanup verification.
* **Sanitation Worker Dashboard:** Real-time driver task feed, job route locations, "After" photo cleanup evidence upload, and multi-modal AI cleanup verification.
* **Central Municipal Oversight:** City-wide resolution analytics, ward comparison leaderboard, and automatic 48-hour SLA breach detection.

---

## 2. AWS Cloud Architecture Overview

* **Networking:** Custom Amazon VPC (`10.0.0.0/16`) with 1 Public Subnet (EC2 web server) and 2 Multi-AZ Private Subnets (RDS database), Internet Gateway, and least-privilege Security Groups.
* **Compute:** Amazon EC2 (`t3.micro` / Amazon Linux 2023) running an Nginx reverse proxy serving the compiled React 18 SPA and proxying `/api` requests to Express (managed via PM2).
* **Managed Database:** Amazon RDS for PostgreSQL (`db.t3.micro`, Single-AZ, non-publicly accessible) with ACID transactions, foreign keys, and native Haversine spatial indexing.
* **Storage:** Private Amazon S3 bucket with all public access blocked; Before/After photos accessed strictly via temporary 1-hour presigned GET URLs.
* **Security & Configuration:** Dedicated EC2 IAM Instance Profile and AWS Systems Manager (SSM) Parameter Store using `SecureString` KMS encryption for database credentials, JWT secrets, and AI keys.
* **Asynchronous Jobs (Ext 1):** Amazon SQS standard queue and Dead-Letter Queue (DLQ) for asynchronous dispatch notifications and SLA audit processing.
* **Monitoring & Alarms:** Amazon CloudWatch Logs (`/swachhnet/backend`) with secret sanitization and CloudWatch Alarm for high EC2 CPU utilization (`> 80%`).
* **Cost Governance:** AWS Budgets with a \$10 monthly spending threshold alert.
* **Infrastructure as Code (Ext 2):** Fully automated, reproducible deployment templates using AWS CloudFormation.

---

## 3. Project Documentation Links

Detailed engineering documentation is located in the [`docs/`](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/) directory:
* [Architecture Specification (`docs/architecture.md`)](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/architecture.md)
* [AWS Services & Justification Matrix (`docs/aws-services.md`)](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/aws-services.md)
* [Step-by-Step Deployment Guide (`docs/deployment.md`)](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/deployment.md)
* [Cost Estimation & Budget Management (`docs/cost-estimate.md`)](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/cost-estimate.md)
* [Live Demonstration Script (`docs/demo-guide.md`)](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/demo-guide.md)
* [Viva Questions & Defense Guide (`docs/viva-preparation.md`)](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/viva-preparation.md)
* [Verification & Evidence Checklist (`docs/evidence-checklist.md`)](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/evidence-checklist.md)

---

## 4. Local Development & Verification

### 1. Run Verification Suite
Verify geospatial calculations, S3 presigned URLs, SQS message structures, and log sanitization:
```bash
node backend/tests/cloud-verification.test.js
```

### 2. Validate CloudFormation Templates
```bash
aws cloudformation validate-template --template-body file://infrastructure/cloudformation/swachhnet-all-in-one.yaml
```

### 3. Build Frontend for Production
```bash
cd frontend
npm install
npm run build
```

---

## 5. Pre-Seeded Test Credentials

All test accounts use the universal password: **`password123`**

| Role | Email | Description |
|---|---|---|
| **Citizen** | `user@test.com` | Reports garbage, tests AI vision validation, tracks rewards. |
| **Ward Admin** | `p_north@bmc.gov.in` | Malad Ward officer; auto-assigns nearest trucks and verifies cleanup. |
| **Ward Admin** | `r_central@bmc.gov.in` | Borivali Ward officer; handles inter-ward transfers. |
| **Sanitation Worker** | `driver1@test.com` | Borivali / Gorai Garage truck worker; uploads "After" photos. |
| **Sanitation Worker** | `driver9@test.com` | Malad Garage truck worker. |
| **Central Superadmin** | `central@swachhnet.com` | Municipal Commissioner oversight and 48-hour SLA breach monitoring. |

---

## 6. Cloud Deployment Quickstart

Deploy the complete infrastructure to AWS via CloudFormation:
```bash
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/swachhnet-all-in-one.yaml \
  --stack-name swachhnet-prod-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
      EnvironmentName=swachhnet \
      DBMasterUserPassword=YourSecurePassword123! \
  --region ap-south-1
```
Refer to [`docs/deployment.md`](file:///c:/Users/kames/Documents/Kamesh/Kamesh%20Agnel/SEM%205/CLOUD/Mini%20Project/smart-garbage/docs/deployment.md) for complete EC2 configuration and Parameter Store setup.
