# AWS Services Integration & Justification Matrix

This document provides a detailed breakdown of every AWS service utilized in the **SwachhNet** project, explaining its architectural necessity, source code integration, and demonstration methodology.

---

## 1. AWS Services Matrix

| # | AWS Service | Category | Specific Role in SwachhNet | Code Integration File | Free Tier / Cost Profile |
|---|---|---|---|---|---|
| **1** | **Amazon VPC** | Networking | Custom isolated network with public & private subnets | `infrastructure/cloudformation/01-networking.yaml` | Free (Standard VPC components have no hourly charge) |
| **2** | **Amazon EC2** | Compute | Hosts Express REST API and Nginx reverse proxy serving React SPA | `infrastructure/cloudformation/05-compute.yaml` | 750 hours/month of `t2.micro` or `t3.micro` Free Tier |
| **3** | **Amazon RDS (PostgreSQL)** | Managed Database | Stores relational records (Users, Wards, Workers, Complaints, Transfers) | `backend/db/index.js`, `infrastructure/cloudformation/04-database.yaml` | 750 hours/month of Single-AZ `db.t3.micro` / `db.t4g.micro` |
| **4** | **Amazon S3** | Storage | Private object store for Before/After complaint photographs | `backend/services/s3Service.js`, `infrastructure/cloudformation/03-storage-sqs.yaml` | 5 GB standard storage, 20,000 GET, 2,000 PUT Free Tier |
| **5** | **AWS IAM** | Security | Least-privilege role & instance profile for EC2 | `infrastructure/cloudformation/02-security-iam.yaml` | Free (No cost for IAM roles or policies) |
| **6** | **AWS SSM Parameter Store** | Management & Governance | Encrypted SecureString configuration store for DB, JWT, and AI keys | `backend/services/ssmService.js` | Free (Standard parameters have no charge) |
| **7** | **Amazon CloudWatch** | Monitoring | Application logging and EC2 CPU utilization alarms | `backend/services/logger.js`, `infrastructure/cloudformation/05-compute.yaml` | 5 GB logs ingestion & 10 custom metrics/alarms Free Tier |
| **8** | **AWS Budgets** | Cost Management | \$10 monthly spending budget with email notifications | Configured via AWS CLI / Console | Free (First 2 action-enabled budgets free) |
| **9** | **Amazon SQS** *(Ext 1)* | Application Integration | Asynchronous job queuing for dispatch notifications & SLA audits | `backend/services/sqsService.js`, `infrastructure/cloudformation/03-storage-sqs.yaml` | 1,000,000 requests/month Free Tier |
| **10**| **AWS CloudFormation** *(Ext 2)* | Infrastructure as Code | Reproducible declarative infrastructure templates | `infrastructure/cloudformation/*.yaml` | Free (Charges apply only to provisioned resources) |

---

## 2. Deep Dive by Service

### 1. Amazon VPC & Networking
* **Why required:** Default VPCs expose instances directly to a single shared network. SwachhNet requires strict network isolation to prevent unauthorized access to the database.
* **How it works:**
  * One Public Subnet (`10.0.1.0/24`) attached to an Internet Gateway for web traffic.
  * Two Private Subnets (`10.0.10.0/24`, `10.0.11.0/24`) spanning two AZs without an IGW route for RDS.
  * Security groups enforce that PostgreSQL port `5432` only accepts connections from the EC2 application security group.
* **Faculty Demonstration:** Show VPC Resource Map in AWS Console: `VPC > Your VPCs > swachhnet-vpc > Resource map`.

---

### 2. Amazon EC2 (Elastic Compute Cloud)
* **Why required:** Serves as the continuous application host. Monolithic applications with integrated background consumers benefit from low latency, zero cold starts, and flat-rate pricing.
* **How it works:** An Amazon Linux 2023 instance runs Nginx and PM2. Nginx serves the React Vite static build at `/` and reverse-proxies `/api/` to Express on `localhost:5000`.
* **Faculty Demonstration:** Open `http://<EC2_PUBLIC_IP>` in browser, log in as citizen, and show PM2 status in terminal (`pm2 status`).

---

### 3. Amazon RDS for PostgreSQL
* **Why required:** Replaced MongoDB Atlas with an enterprise relational database supporting ACID transactions, foreign key constraints, and spherical Haversine spatial indexing.
* **How it works:**
  * `ward_authorities` and `workers` store GPS coordinates.
  * When a citizen submits a complaint or an admin dispatches a truck, the backend executes the Haversine trigonometric formula:
    ```sql
    SELECT user_id, truck_number,
      (6371 * acos(
        cos(radians($1)) * cos(radians(latitude)) * 
        cos(radians(longitude) - radians($2)) + 
        sin(radians($1)) * sin(radians(latitude))
      )) AS distance_km
    FROM workers
    WHERE assigned_ward_id = $3 AND status = 'idle'
    ORDER BY distance_km ASC LIMIT 1;
    ```
* **Faculty Demonstration:** Show RDS instance status in AWS Console: `RDS > Databases > swachhnet-postgres`.

---

### 4. Amazon S3 (Simple Storage Service)
* **Why required:** Replaced third-party Cloudinary with a native, private AWS storage bucket for all municipal photo evidence.
* **How it works:**
  * All public access is blocked at the bucket level.
  * The backend uploads photos via AWS SDK `PutObjectCommand`.
  * Temporary access is granted via presigned GET URLs with a 1-hour expiration generated by `getSignedUrl`.
* **Faculty Demonstration:** Open `S3 > Buckets > swachhnet-evidence-...`. Show that the bucket has **"Block all public access: On"** and demonstrate that direct URL access without the presigned query string returns `AccessDenied (403)`.

---

### 5. AWS Systems Manager (SSM) Parameter Store
* **Why required:** Eliminates hardcoded passwords, plaintext `.env` files in git repositories, and exposes secrets only to the authorized EC2 instance profile.
* **Parameters Configured:**
  * `/swachhnet/prod/DATABASE_URL` (SecureString with KMS)
  * `/swachhnet/prod/JWT_SECRET` (SecureString)
  * `/swachhnet/prod/G_API` (SecureString)
* **Faculty Demonstration:** Show SSM Parameter Store: `AWS Systems Manager > Parameter Store`. Demonstrate that values are stored as `SecureString` with KMS encryption.

---

### 6. Amazon CloudWatch
* **Why required:** Provides operational observability and proactive fault detection for municipal infrastructure.
* **How it works:**
  * Backend logs are sanitized of passwords/tokens and streamed to `/swachhnet/backend`.
  * A CloudWatch Alarm (`swachhnet-ec2-high-cpu-alarm`) continuously monitors `CPUUtilization >= 80%` over two 5-minute periods.
* **Faculty Demonstration:** Navigate to `CloudWatch > Log groups > /swachhnet/backend` to view real-time API logs, and show `CloudWatch > Alarms` with the configured CPU alarm in `OK` state.

---

### 7. Amazon SQS (Simple Queue Service) — Additional Capability 1
* **Why required:** Decouples customer-facing complaint creation and admin dispatching from slow downstream operations like SMS alerts and SLA breach auditing.
* **How it works:**
  * On dispatch, the API calls `enqueueJob('TRUCK_ASSIGNED', payload)`.
  * The background worker polls `swachhnet-jobs-queue`, processes the event, and deletes the message upon success.
  * Messages failing 5 times are routed to `swachhnet-jobs-dlq`.
* **Faculty Demonstration:** In AWS Console, open `SQS > Queues > swachhnet-jobs-queue`. Show message statistics, visibility timeout (60s), and the linked Dead-Letter Queue.

---

### 8. AWS CloudFormation — Additional Capability 2
* **Why required:** Implements Infrastructure as Code (IaC) to guarantee 100% reproducibility of the entire municipal cloud environment across student accounts or enterprise regions.
* **Templates Provided:**
  * `01-networking.yaml` (VPC, Subnets, IGW, Route Tables)
  * `02-security-iam.yaml` (Security Groups, IAM Role & Profile)
  * `03-storage-sqs.yaml` (S3 Bucket, SQS Queues)
  * `04-database.yaml` (RDS DB Subnet Group, PostgreSQL DB)
  * `05-compute.yaml` (EC2 Instance, UserData, CloudWatch)
  * `swachhnet-all-in-one.yaml` (Unified single-stack template)
* **Faculty Demonstration:** Show `CloudFormation > Stacks` in the AWS Console with `CREATE_COMPLETE` status and inspect the generated resource tree and outputs.

