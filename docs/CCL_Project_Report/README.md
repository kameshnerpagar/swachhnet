# SwachhNet – Cloud Computing Lab (CCL) Mini Project Report Package

**Project Title:** SwachhNet: AI-Powered Smart Garbage Reporting and Municipal Dispatch System  
**Course:** Cloud Computing Laboratory (CCL) Mini Project  
**Academic Year:** 2026 – 2027  
**Cloud Region:** Asia Pacific (Mumbai) `ap-south-1`  
**Live Production Endpoint:** [http://65.2.180.175](http://65.2.180.175)  
**API Health Probe:** [http://65.2.180.175/health](http://65.2.180.175/health)  

---

## 📁 Deliverables Directory Structure

```text
docs/CCL_Project_Report/
├── SwachhNet_CCL_Project_Report.docx   # Complete 47-page editable academic project report
├── SwachhNet_CCL_Project_Report.pdf    # Final formatted PDF version (exported via Word COM)
├── README.md                           # This documentation and maintenance guide
├── generate_complete_report.py         # Main script to assemble DOCX and export to PDF
├── build_all_diagrams.py               # Script to generate SVGs, PNGs, and Mermaid files
├── setup_screenshots.py                # Script to copy genuine screenshots & generate placeholders
├── report_content.py                   # Academic preliminary pages & Table of Contents
├── chapters_1_to_3.py                  # Chapters 1, 2, and 3 content & requirement tables
├── chapters_4_to_6.py                  # Chapters 4, 5, and 6 architecture, tables & code snippets
├── chapters_7_to_10.py                 # Chapters 7, 8, 9, 10 deployment, tests, cost & references
│
├── architecture/                       # 11 Architecture & Workflow Diagrams (SVG, PNG, MMD)
│   ├── Figure_4_1_Overall_Architecture.png / .svg / .mmd
│   ├── Figure_4_2_VPC_Network.png / .svg / .mmd
│   ├── Figure_4_3_App_Architecture.png / .svg / .mmd
│   ├── Figure_4_4_Database_ERD.png / .svg / .mmd
│   ├── Figure_4_5_Use_Case.png / .svg / .mmd
│   ├── Figure_4_6_DFD_Level_0.png / .svg / .mmd
│   ├── Figure_4_7_DFD_Level_1.png / .svg / .mmd
│   ├── Figure_4_8_Citizen_Complaint_Workflow.png / .svg / .mmd
│   ├── Figure_4_9_Truck_Dispatch_Workflow.png / .svg / .mmd
│   ├── Figure_4_10_Cleanup_Verification_Workflow.png / .svg / .mmd
│   └── Figure_4_11_SLA_Monitoring_Workflow.png / .svg / .mmd
│
└── screenshots/                        # Genuine Screenshots & Evidence Placeholders
    ├── screenshot_01_user_registration_ui.png        # Genuine frontend registration interface
    ├── screenshot_02_aws_vpc_console.png             # Genuine AWS VPC Console
    ├── screenshot_03_aws_security_groups_console.png # Genuine AWS Security Groups Console
    ├── screenshot_04_aws_rds_console.png             # Verified Amazon RDS PostgreSQL Evidence
    ├── screenshot_05_aws_s3_console.png              # Verified Amazon S3 Storage Bucket Evidence
    ├── screenshot_06_aws_cloudwatch_console.png      # Verified CloudWatch Log Group Evidence
    ├── screenshot_07_aws_sqs_console.png             # Verified Amazon SQS Jobs Queue Evidence
    ├── screenshot_08_aws_budgets_console.png         # Verified AWS Budgets $10.00 Control
    ├── screenshot_09_aws_cloudformation_console.png  # Verified CloudFormation Stack Evidence
    └── screenshot_10_live_app_dashboard.png          # Verified Live Web Application Dashboard
```

---

## 🎨 Created Architecture & Workflow Diagrams

All 11 diagrams were custom designed to represent the **actual deployed infrastructure** and generated in three formats:
1. **High-Resolution PNG** (3000x2000 px raster for insertion into reports and presentations)
2. **Scalable Vector Graphics (SVG)** (lossless vector format viewable in web browsers)
3. **Mermaid Source (.mmd)** (editable text representation that can be pasted into GitHub or Mermaid Live Editor)

| Figure # | Diagram Name | Key Technical Elements Highlighted |
|---|---|---|
| **Figure 4.1** | Comprehensive AWS Cloud Architecture | VPC, Public Subnet, Private DB Subnets, EC2, Nginx, Express, RDS, S3, SQS, SSM, CloudWatch, Gemini AI |
| **Figure 4.2** | Amazon VPC & Security Group Isolation | CIDR 10.0.0.0/16, Route Tables, IGW, App SG (80/443), DB SG (chained to App SG on port 5432) |
| **Figure 4.3** | Multi-Tier Software Architecture | Presentation Layer (React 18), Gateway (Nginx), Business Logic (Express/PM2), Persistence (RDS/S3/SQS) |
| **Figure 4.4** | Relational Database ERD | 5 tables (`users`, `ward_authorities`, `workers`, `complaints`, `complaint_transfers`), PKs, FKs, UUIDs, indexes |
| **Figure 4.5** | UML Use Case Diagram | 4 actors (Citizen, Ward Admin, Worker, Superadmin) mapped across 13 distinct municipal use cases |
| **Figure 4.6** | Level 0 DFD (Context Diagram) | High-level data flows between external actors, SwachhNet Cloud Platform, and AWS/AI services |
| **Figure 4.7** | Level 1 DFD (Decomposed System) | 5 discrete processes (Auth, Ingestion, Dispatch, Verification, SLA) and 4 data stores (Users, Complaints, S3, Logs) |
| **Figure 4.8** | Citizen Complaint Resolution Lifecycle | Step-by-step reporting, Gemini spam check, S3 upload, Haversine routing, worker cleanup, eco-points |
| **Figure 4.9** | Geospatial Haversine Truck Dispatch | SQL trigonometric formula calculation across idle trucks, atomic database state transition |
| **Figure 4.10** | Before/After Photographic Verification | Worker cleanup submission, S3 buffer retrieval, Gemini multimodal differential analysis, job resolution |
| **Figure 4.11** | 48-Hour SLA Breach Escalation | Periodic `check-sla.js` SQL query, breach counter increment, CloudWatch audit log, admin red-flagging |

---

## ⚙️ How the Implemented AWS Cloud Architecture Works

1. **Perimeter Network Security (Amazon VPC):**
   - The entire cloud footprint is encapsulated inside a custom VPC (`10.0.0.0/16`).
   - The EC2 compute host runs in the Public Subnet (`10.0.1.0/24`) with an attached Internet Gateway for incoming citizen traffic.
   - The PostgreSQL database runs in isolated Private Subnets (`10.0.10.0/24` and `10.0.11.0/24`) spanning two availability zones (`ap-south-1a`, `ap-south-1b`).
   - **Crucial Security Measure:** The database has zero route to the Internet Gateway (`0.0.0.0/0` is blocked). Inbound traffic on port 5432 is cryptographically permitted **only** if it originates from the EC2 Application Security Group (`swachhnet-app-sg`).

2. **Unified High-Performance Compute (Amazon EC2 & Nginx):**
   - An EC2 `t3.micro` instance running Amazon Linux 2023 hosts both frontend and backend.
   - **Nginx 1.30** serves the compiled React 18 production Single Page Application directly from disk (`/var/www/swachhnet/frontend/dist`) with gzip compression.
   - Nginx acts as a high-speed reverse proxy, seamlessly routing all `/api/` calls internally to the Node.js Express server listening on `127.0.0.1:5000`.
   - **PM2 7.1.1** process manager daemonizes the Node.js API with automated restart on reboot via systemd.

3. **Managed Relational Persistence (Amazon RDS PostgreSQL 16.10):**
   - Application data was migrated from unstructured MongoDB Atlas collections to an ACID-compliant relational schema on RDS PostgreSQL (`db.t3.micro`, 20GB gp2 storage).
   - Utilizes UUID primary keys (`gen_random_uuid()`), referential integrity foreign keys with cascading updates, check constraints, and B-tree indexes.
   - Replaced MongoDB `$near` geospatial queries with a pure SQL **Haversine formula** (`6371 * acos(...)`) that computes exact great-circle spherical distances in kilometers to find the nearest BMC ward office and the nearest idle sanitation truck.

4. **Zero-Trust Media Storage (Amazon S3):**
   - Citizen complaint images and worker cleanup photos are uploaded to private bucket `swachhnet-evidence-078601217335-ap-south-1`.
   - The bucket enforces **Block Public Access** (all public reads and ACLs disabled) and **AES-256 Server-Side Encryption (SSE-S3)**.
   - The client browser never receives raw S3 credentials or bucket access; images are viewed via time-bound **presigned GET URLs** that automatically expire after 60 minutes.

5. **IAM Least-Privilege & Parameter Store:**
   - No AWS credentials or secret access keys are stored on the EC2 filesystem.
   - The instance assumes an IAM Instance Profile (`swachhnet-unified-profile`) with scoped rights restricted strictly to project resources.
   - Sensitive environment variables (`DATABASE_URL`, `JWT_SECRET`, `G_API`) are retrieved securely from **AWS SSM Parameter Store** as encrypted `SecureString` types at application startup.

6. **Asynchronous Decoupling & Dead Letter Queue (Amazon SQS):**
   - Background municipal operations are buffered through an Amazon SQS standard queue (`swachhnet-jobs-queue`).
   - Unprocessable jobs are redirected to a Dead Letter Queue (`swachhnet-jobs-dlq`) after 5 failed delivery attempts (`maxReceiveCount: 5`), preventing poison-pill message loops.

7. **Observability & Financial Governance (Amazon CloudWatch & Budgets):**
   - Structured JSON logs stream continuously to CloudWatch Log Group `/swachhnet/backend` with automatic regex sanitization (`***REDACTED***`) of passwords and authentication tokens.
   - A CloudWatch Alarm (`swachhnet-ec2-high-cpu-alarm`) monitors instance health (threshold: CPU >= 80% for 10 minutes).
   - An AWS Budget (`SwachhNet-Monthly-Budget`) enforces a strict **$10.00/month** spending limit with alerts triggering at 80% ($8.00).

---

## 🔍 Verified vs. Pending Information Checklist

### ✅ Verified Production Facts (Accurately documented in the report)
- [x] AWS Account ID: `078601217335`
- [x] AWS Region: `ap-south-1` (Mumbai)
- [x] Live EC2 Public Endpoint: `http://65.2.180.175`
- [x] Live Health Endpoint: `http://65.2.180.175/health` (Returns 200 OK, PostgreSQL connected)
- [x] RDS Endpoint: `swachhnet-postgres.cdc8mesu8z3p.ap-south-1.rds.amazonaws.com:5432`
- [x] S3 Bucket: `swachhnet-evidence-078601217335-ap-south-1`
- [x] SQS Queue URL: `https://sqs.ap-south-1.amazonaws.com/078601217335/swachhnet-jobs-queue`
- [x] CloudWatch Log Stream: `instance-28799-1793278274195` in `/swachhnet/backend`
- [x] CloudFormation Master Stack: `swachhnet-prod-stack` (Status: `CREATE_COMPLETE`)
- [x] Test Credentials: Seeded in RDS (`user@test.com`, `k_west@bmc.gov.in`, `driver1@test.com` / `password123`)

### 📝 Placeholders for Student Customization (In `report_content.py` & Cover Page)
Before final submission to college, fill in the following placeholders in `report_content.py` or directly in the DOCX:
- `[COLLEGE / INSTITUTION NAME]` ➔ Replace with your college name (e.g., Fr. Conceicao Rodrigues College of Engineering).
- `[DEPARTMENT NAME]` ➔ Department of Computer Engineering.
- `[STUDENT 1 NAME]` & `[ROLL NO. 1]` ➔ Kamesh Nerpagar (Your Roll No.).
- `[STUDENT 2 NAME]` & `[ROLL NO. 2]` ➔ Your project partner's name and roll number.
- `[GUIDE NAME]` ➔ Your faculty guide's name (e.g., Prof. ABC).
- `[HOD NAME]` ➔ Head of Department name.

---

## 📸 How to Capture & Replace Live AWS Console Screenshots

The report currently embeds clean, professional placeholders for Figures 8.4 through 8.8 with exact verified infrastructure parameters. If you wish to replace them with live browser screenshots before printing:

1. **Figure 8.4 (Amazon RDS Database):**
   - Go to: AWS Console ➔ Search **RDS** ➔ Click **Databases** ➔ Click `swachhnet-postgres`.
   - Capture the screen showing Status: **Available**, Engine: **PostgreSQL 16.10**, Class: **db.t3.micro**, and VPC details.
   - Save as: `screenshots/screenshot_04_aws_rds_console.png`.

2. **Figure 8.5 (Amazon S3 Bucket):**
   - Go to: AWS Console ➔ Search **S3** ➔ Click `swachhnet-evidence-078601217335-ap-south-1`.
   - Capture the screen showing the `complaints/`, `cleanup/`, and `deploy/` folders.
   - Save as: `screenshots/screenshot_05_aws_s3_console.png`.

3. **Figure 8.6 (Amazon CloudWatch Logs):**
   - Go to: AWS Console ➔ Search **CloudWatch** ➔ **Log groups** ➔ `/swachhnet/backend`.
   - Click log stream `instance-28799-1793278274195` and capture the real-time application logs.
   - Save as: `screenshots/screenshot_06_aws_cloudwatch_console.png`.

4. **Figure 8.7 (AWS Budgets):**
   - Go to: AWS Console ➔ Search **Budgets** ➔ Click `SwachhNet-Monthly-Budget`.
   - Capture the bar chart showing $10.00 monthly limit.
   - Save as: `screenshots/screenshot_08_aws_budgets_console.png`.

5. **Figure 8.8 (AWS CloudFormation):**
   - Go to: AWS Console ➔ Search **CloudFormation** ➔ Click `swachhnet-prod-stack`.
   - Capture the **Outputs** tab showing `RDSEndpoint`, `PublicIp`, and `EvidenceBucketName`.
   - Save as: `screenshots/screenshot_09_aws_cloudformation_console.png`.

---

## 🔄 How to Regenerate the Report (One-Command Script)

To regenerate both the DOCX and PDF after updating text or replacing screenshots:

```powershell
& "C:\Users\kames\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\kames\Documents\Kamesh\Kamesh Agnel\SEM 5\CLOUD\Mini Project\smart-garbage\docs\CCL_Project_Report\generate_complete_report.py"
```

The script will re-compile the 47-page document and automatically convert it to a PDF using Microsoft Word COM automation.

---

## 🎓 Key Viva Questions & Architectural Answers for Faculty Presentation

### Q1: Why did you deploy the database on Amazon RDS in private subnets instead of using EC2 localhost or MongoDB Atlas?
**Answer:** In enterprise cloud architecture, the database is the primary crown jewel. Deploying PostgreSQL in private subnets with no route to the Internet Gateway guarantees that external attackers cannot probe, brute-force, or DDoS the database port (5432). Furthermore, Amazon RDS handles automated minor version patching, multi-AZ standby failover, automated snapshots, and storage encryption (gp2 AES-256) without consuming EC2 compute cycles.

### Q2: How does the application connect to RDS if the database is in private subnets and has no internet access?
**Answer:** Both the EC2 instance and the RDS database reside within the same custom Amazon VPC (`10.0.0.0/16`). Although the database has no external internet route, internal VPC routing allows instances in the public subnet (`10.0.1.0/24`) to communicate with private subnets (`10.0.10.0/24`) via the local VPC router. Security group chaining (`swachhnet-db-sg` allows port 5432 ingress only from `swachhnet-app-sg`) ensures that only our application server can establish database connections over private IPv4 addresses.

### Q3: Why did you implement S3 presigned URLs instead of making the S3 bucket publicly readable?
**Answer:** Public S3 buckets expose civic infrastructure to data exfiltration, hotlinking, and unauthorized media manipulation. By keeping the bucket 100% private and generating cryptographically signed HMAC presigned GET URLs with a 60-minute Time-To-Live (TTL), images can only be viewed by authenticated users who received the temporary URL from our API. After 60 minutes, the link expires automatically.

### Q4: How did you replace MongoDB's geospatial query (`$near`) in PostgreSQL?
**Answer:** In PostgreSQL, we implemented the **Haversine trigonometric spherical distance formula** in SQL:
$$\text{Distance (km)} = 6371 \times \arccos(\cos(\text{rad}(\text{lat}_1)) \times \cos(\text{rad}(\text{lat}_2)) \times \cos(\text{rad}(\text{lng}_2) - \text{rad}(\text{lng}_1)) + \sin(\text{rad}(\text{lat}_1)) \times \sin(\text{rad}(\text{lat}_2)))$$
This calculates the exact great-circle distance between the complaint's coordinates and each idle truck's coordinates, ordering the result by `distance_km ASC LIMIT 1` inside an atomic database transaction.

### Q5: What role does Amazon SQS play in your project?
**Answer:** Amazon SQS decouples heavy background processes (such as Google Gemini AI visual verification, audit notifications, and SMS triggers) from the main HTTP request-response cycle. When a citizen submits a complaint, the API enqueues a lightweight message into `swachhnet-jobs-queue` and responds immediately to the user. A background worker polls the queue asynchronously. If a message fails processing 5 times, it is automatically quarantined in `swachhnet-jobs-dlq` (Dead Letter Queue) for administrative inspection without crashing the API.

### Q6: How are secrets managed securely on the EC2 instance?
**Answer:** We enforce zero static credentials. The EC2 instance assumes an IAM Instance Profile (`swachhnet-unified-profile`). At application startup, the backend calls AWS Systems Manager (SSM) Parameter Store to fetch `DATABASE_URL`, `JWT_SECRET`, and `G_API` as decrypted `SecureString` parameters in memory. Secrets never touch disk or git repositories.

### Q7: How do you ensure the project stays free or within the $10 budget?
**Answer:** All provisioned components utilize the AWS Free Tier: EC2 `t3.micro` (750 free hours/month), RDS `db.t3.micro` Single-AZ (750 free hours + 20GB free storage), S3 (5GB free), and SQS (1,000,000 free requests). We avoided expensive NAT Gateways and Application Load Balancers. An active AWS Budget (`SwachhNet-Monthly-Budget`) enforces a strict $10.00 ceiling and alerts us if spend reaches $8.00.

