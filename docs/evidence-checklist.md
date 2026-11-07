# SwachhNet Cloud Verification & Evidence Checklist

Use this checklist during your laboratory evaluation and report preparation to collect and present verifiable proof of your cloud deployment.

---

## 1. Automated Test Results

| Test Item | Verification Command | Expected Output | Status |
|---|---|---|---|
| **Frontend Production Build** | `cd frontend && npm run build` | `dist/index.html`, bundle generated in < 10s with 0 errors | **PASS** |
| **Cloud Verification Suite** | `node backend/tests/cloud-verification.test.js` | 4 Passed (Haversine, S3 Presigned URLs, SQS, CloudWatch Sanitization) | **PASS** |
| **CloudFormation Validation** | `aws cloudformation validate-template ...` | Returns parameter lists and zero template syntax errors | **PASS** |
| **PostgreSQL Migration Check** | `node backend/db/seed.js` | `8 BMC Ward Authorities`, `32 Truck Drivers`, `1 Citizen`, `1 Superadmin` created | **PASS** |
| **SLA Diagnostic Check** | `node backend/check-sla.js` | Detects active complaints and sample >48h SLA breaches | **PASS** |

---

## 2. AWS Management Console Evidence Checklist

Collect the following screenshots or live views to demonstrate to your evaluator:

### 1. Amazon VPC & Networking
- [ ] **VPC List:** Shows `swachhnet-vpc` with IPv4 CIDR `10.0.0.0/16`.
- [ ] **VPC Resource Map:** Visual diagram showing `swachhnet-vpc` connected to `swachhnet-igw`, with 1 Public Subnet (`10.0.1.0/24`) and 2 Private Subnets (`10.0.10.0/24`, `10.0.11.0/24`).
- [ ] **Security Groups:**
  - `swachhnet-app-sg`: Inbound rules for HTTP (80) and HTTPS (443).
  - `swachhnet-db-sg`: Inbound rule for PostgreSQL (5432) restricted strictly to `swachhnet-app-sg`.

### 2. Amazon EC2
- [ ] **EC2 Instances:** `swachhnet-web-server` running on `t3.micro` with assigned Public IPv4 address.
- [ ] **IAM Role Attached:** Verify IAM instance profile `swachhnet-ec2-instance-profile` is attached to the EC2 instance.
- [ ] **Nginx & PM2 Status (Terminal):**
  ```bash
  systemctl status nginx
  pm2 list
  ```

### 3. Amazon RDS for PostgreSQL
- [ ] **RDS Databases:** Database identifier `swachhnet-postgres` in `Available` status.
- [ ] **Connectivity & Security:**
  - DB Subnet Group: Shows multi-AZ private subnets.
  - Public Accessibility: **No**.
  - Port: `5432`.
  - Security Group: `swachhnet-db-sg`.

### 4. Amazon S3 (Private Storage)
- [ ] **Bucket Properties:** `swachhnet-evidence-...` with **"Block all public access: On"**.
- [ ] **Bucket Objects:** Folder view showing `complaints/` and `cleanup/` containing citizen and worker evidence images.
- [ ] **Presigned URL Verification:** Show that clicking the raw object URL results in `403 Access Denied`, whereas viewing through the SwachhNet frontend loads the photo seamlessly via a presigned URL.

### 5. AWS Systems Manager (SSM) Parameter Store
- [ ] **Parameter List:** Shows parameters under path `/swachhnet/prod/`:
  - `/swachhnet/prod/DATABASE_URL` (Type: `SecureString`, Key ID: `alias/aws/ssm`)
  - `/swachhnet/prod/JWT_SECRET` (Type: `SecureString`)
  - `/swachhnet/prod/G_API` (Type: `SecureString`)
  - `/swachhnet/prod/S3_BUCKET_NAME` (Type: `String`)
  - `/swachhnet/prod/SQS_QUEUE_URL` (Type: `String`)

### 6. Amazon CloudWatch
- [ ] **Log Groups:** `/swachhnet/backend` showing timestamped, sanitized HTTP access and application logs.
- [ ] **Alarms:** `swachhnet-ec2-high-cpu-alarm` with metric `CPUUtilization >= 80%` in `OK` state.

### 7. Amazon SQS
- [ ] **Queues:** `swachhnet-jobs-queue` and `swachhnet-jobs-dlq` (Dead-Letter Queue).
- [ ] **Queue Details:** Shows visibility timeout of `60 seconds` and linked dead-letter target ARN.

### 8. AWS CloudFormation
- [ ] **Stacks:** `swachhnet-prod-stack` with status `CREATE_COMPLETE`.
- [ ] **Outputs Tab:** Shows `WebsiteURL`, `PublicIp`, `RDSEndpoint`, and `EvidenceBucketName`.

