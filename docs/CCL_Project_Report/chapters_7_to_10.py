# chapters_7_to_10.py
# Detailed chapter texts for Chapter 7, 8, 9, 10 and References

CH7_STEPS = [
    ("Step 1: IAM Deployment User Provisioning", """An IAM programmatic user named cfn-deployer was provisioned in AWS Account 078601217335 with AdministratorAccess privileges to orchestrate multi-service CloudFormation template executions without permission blocks."""),
    ("Step 2: Declarative CloudFormation Template Execution", """The unified CloudFormation template (infrastructure/cloudformation/swachhnet-all-in-one.yaml) was validated using the AWS CLI and deployed to region ap-south-1 under the stack name swachhnet-prod-stack. The deployment provisioned 24 resources including the custom VPC, subnets, route tables, security groups, IAM instance role, S3 bucket, SQS queues, RDS instance, EC2 host, and CloudWatch log group."""),
    ("Step 3: Centralized SSM Parameter Store Population", """Sensitive production credentials were encrypted and pushed to AWS Systems Manager Parameter Store under the /swachhnet/prod/ namespace. DATABASE_URL, JWT_SECRET, and G_API were stored as SecureString types; S3_BUCKET_NAME and SQS_QUEUE_URL were stored as String types."""),
    ("Step 4: EC2 Instance Initialization & User Data Execution", """The EC2 t3.micro instance (Amazon Linux 2023) executed a cloud-init UserData script that updated package repositories, installed Node.js 18, Git, and Nginx, installed PM2 globally, configured Nginx reverse proxy routes, and enabled the Nginx systemd daemon."""),
    ("Step 5: Code Artifact Packaging & S3 Staging", """The production application bundle (backend source code, dependency manifests, and pre-built frontend distribution directory) was packaged into app.tar.gz and staged in the private S3 bucket at s3://swachhnet-evidence-078601217335-ap-south-1/deploy/app.tar.gz."""),
    ("Step 6: Remote In-Place Deployment via AWS Systems Manager", """Using AWS SSM Run Command (AWS-RunShellScript), the EC2 instance securely retrieved the application archive from S3, unpacked it into /var/www/swachhnet, executed npm install --omit=dev, populated production configuration, and initialized the application."""),
    ("Step 7: Relational Database Migration & BMC Seed Execution", """The database bootstrap script (backend/db/seed.js) was executed on the EC2 host. The script applied SQL migration 001_init_schema.sql, creating the relational schema, and seeded 8 BMC administrative wards, 32 municipal truck drivers, test citizen accounts, and historical SLA demo complaints."""),
    ("Step 8: PM2 Process Daemonization & Nginx Reload", """The backend API was launched under PM2 under the process name swachhnet-api. PM2 startup hooks were generated to ensure process respawning across server reboots. Nginx was reloaded to bind port 80 to the React SPA and reverse proxy /api/ traffic to port 5000."""),
    ("Step 9: Health Probe Verification & AWS Budget Creation", """The public deployment was validated by executing curl probes against http://65.2.180.175/health, confirming HTTP 200 OK with PostgreSQL connected. Finally, an AWS Budget (SwachhNet-Monthly-Budget) with a $10.00 ceiling was provisioned.""")
]

TEST_CASES_TABLE = [
    ("TC-01", "API Health & Engine Probe", "GET /health returns HTTP 200 with engine 'PostgreSQL (Amazon RDS)'", "HTTP 200 OK, PostgreSQL connected, status healthy", "PASS"),
    ("TC-02", "VPC & Subnet Isolation", "PostgreSQL database resides in private subnets with no internet route", "Subnet 10.0.10.0/24 route table has local route only; no IGW", "PASS"),
    ("TC-03", "Security Group Ingress Chaining", "Port 5432 rejects direct internet connections, accepting EC2 SG only", "Port 5432 inaccessible from internet; connects from app-sg", "PASS"),
    ("TC-04", "Citizen Registration", "POST /api/auth/register inserts new user into RDS users table", "User record inserted, bcrypt password hashed, JWT returned", "PASS"),
    ("TC-05", "Citizen Login Authentication", "POST /api/auth/login with valid credentials returns signed JWT", "HTTP 200 OK with valid JWT and role 'user'", "PASS"),
    ("TC-06", "Role-Based Access Control", "Citizen token attempting access to /api/authority routes is rejected", "HTTP 403 Forbidden returned by role-based middleware", "PASS"),
    ("TC-07", "Garbage Photo AI Validation", "Photo showing legitimate garbage passes Gemini AI inspection", "Gemini returns isGarbage: true; complaint accepted", "PASS"),
    ("TC-08", "Spam & Non-Garbage Rejection", "Random image/selfie submitted is rejected with error notice", "Gemini returns isGarbage: false; HTTP 400 returned", "PASS"),
    ("TC-09", "Private S3 Evidence Upload", "Uploaded complaint photo stored in S3 complaints/ with SSE-S3", "Object stored in S3 bucket with AES-256 encryption", "PASS"),
    ("TC-10", "S3 Presigned URL Resolution", "Frontend receives valid presigned GET URL with 60-min expiration", "Secure time-bound presigned URL returned and rendered in UI", "PASS"),
    ("TC-11", "Geospatial Ward Partitioning", "Complaint coordinates matched to closest BMC ward via Haversine", "Coordinates (19.11, 72.84) correctly matched to K/West Ward", "PASS"),
    ("TC-12", "Nearest Truck Dispatch", "Ward Admin dispatches nearest idle truck using SQL Haversine query", "Nearest truck selected, complaint 'assigned', truck 'busy'", "PASS"),
    ("TC-13", "Worker Task Retrieval", "Driver logs in and views assigned complaint with navigation map", "Task coordinates, address, and complaint photo displayed", "PASS"),
    ("TC-14", "Cleanup Photo Evidence Upload", "Worker uploads cleanup photo to S3 cleanup/ folder", "Object uploaded, status updated to 'pending_verification'", "PASS"),
    ("TC-15", "Before/After AI Verification", "Gemini compares before and after photos to verify clean site", "AI verifies waste removed; complaint marked 'resolved'", "PASS"),
    ("TC-16", "Gamification Points Credit", "Citizen receives +10 eco-points upon verified resolution", "Citizen point tally incremented from 0 to 10 in database", "PASS"),
    ("TC-17", "48-Hour SLA Breach Escalation", "Complaints older than 48 hours flagged as breached in dashboards", "check-sla.js flags seeded complaint; dashboard counter increments", "PASS"),
    ("TC-18", "CloudWatch Structured Logging", "Server runtime events logged to /swachhnet/backend with redaction", "Log stream active; passwords and tokens sanitized as ***REDACTED***", "PASS"),
    ("TC-19", "CloudWatch CPU Metric Alarm", "Alarm configured to trigger when EC2 CPUUtilization >= 80%", "Alarm swachhnet-ec2-high-cpu-alarm verified active", "PASS"),
    ("TC-20", "AWS Budget Enforcement", "Monthly budget ceiling configured at $10.00 with 80% threshold", "SwachhNet-Monthly-Budget active and verified in AWS Budgets", "PASS")
]

COST_TABLE = [
    ("Amazon EC2", "t3.micro (2 vCPU, 1 GB RAM, Amazon Linux 2023)", "750 Hours / Month Free Tier", "$0.00", "Production Web & API Host"),
    ("Amazon RDS", "db.t3.micro (Single-AZ, PostgreSQL 16.10, 20GB gp2)", "750 Hours + 20GB Storage Free Tier", "$0.00", "Managed Relational Database"),
    ("Amazon S3", "Standard Storage (Private Bucket, Versioning Enabled)", "5 GB Free Tier Storage", "$0.00", "Photographic Evidence Storage"),
    ("Amazon SQS", "Standard Queue + Dead Letter Queue", "1,000,000 Free Requests / Month", "$0.00", "Asynchronous Task Buffering"),
    ("AWS SSM", "Parameter Store (Standard SecureString Parameters)", "Free Tier Unlimited Standard Usage", "$0.00", "Encrypted Secrets Management"),
    ("Amazon CloudWatch", "Log Group (/swachhnet/backend) + 1 Metric Alarm", "5 GB Log Ingestion + 10 Alarms Free", "$0.00", "Structured Logging & Alarms"),
    ("Amazon VPC & IGW", "Custom VPC (10.0.0.0/16) + Internet Gateway", "Free Tier (No NAT Gateway Used)", "$0.00", "Isolated Network Infrastructure"),
    ("AWS Budgets", "1 Monthly Budget Alert ($10.00 Limit)", "2 Free Budgets per AWS Account", "$0.00", "Financial Governance"),
    ("AWS CloudFormation", "Stack Management & Resource Provisioning", "Free Tier for Native AWS Resources", "$0.00", "Infrastructure as Code"),
    ("Public IPv4 Address", "1 In-Use Public IPv4 Address on EC2", "First 750 Hours / Month Free Tier", "$0.00", "Public Application Endpoint"),
    ("Total Estimated Spend", "All 10 Implemented AWS Services Combined", "Operating within Free Tier Parameters", "$0.00 - $1.50", "Cost-Optimized Architecture")
]

REFERENCES = [
    ("1", "Amazon Web Services Documentation. (2024). Amazon Elastic Compute Cloud (EC2) User Guide for Linux Instances. AWS Documentation. https://docs.aws.amazon.com/ec2/"),
    ("2", "Amazon Web Services Documentation. (2024). Amazon Relational Database Service (RDS) User Guide for PostgreSQL. AWS Documentation. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/"),
    ("3", "Amazon Web Services Documentation. (2024). Amazon Simple Storage Service (S3) User Guide. AWS Documentation. https://docs.aws.amazon.com/AmazonS3/latest/userguide/"),
    ("4", "Amazon Web Services Documentation. (2024). Amazon Virtual Private Cloud (VPC) User Guide. AWS Documentation. https://docs.aws.amazon.com/vpc/"),
    ("5", "Amazon Web Services Documentation. (2024). AWS CloudFormation User Guide: Infrastructure as Code. AWS Documentation. https://docs.aws.amazon.com/cloudformation/"),
    ("6", "Amazon Web Services Documentation. (2024). Amazon Simple Queue Service (SQS) Developer Guide. AWS Documentation. https://docs.aws.amazon.com/AWSSimpleQueueService/"),
    ("7", "Amazon Web Services Documentation. (2024). Amazon CloudWatch User Guide: Monitoring and Observability. AWS Documentation. https://docs.aws.amazon.com/cloudwatch/"),
    ("8", "Amazon Web Services Documentation. (2024). AWS Identity and Access Management (IAM) User Guide. AWS Documentation. https://docs.aws.amazon.com/IAM/"),
    ("9", "Amazon Web Services Documentation. (2024). AWS Systems Manager Parameter Store User Guide. AWS Documentation. https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html"),
    ("10", "Google DeepMind. (2024). Gemini 1.5 Flash: Efficient Multimodal Generative AI for High-Speed Reasoning. Google AI Developer Documentation. https://ai.google.dev/docs"),
    ("11", "Mell, P., & Grance, T. (2011). The NIST Definition of Cloud Computing. National Institute of Standards and Technology (NIST) Special Publication 800-145. U.S. Department of Commerce. https://doi.org/10.6028/NIST.SP.800-145"),
    ("12", "PostgreSQL Global Development Group. (2024). PostgreSQL 16.10 Documentation: Relational Database System. https://www.postgresql.org/docs/16/"),
    ("13", "React Documentation Group. (2024). React 18: The Library for Web and Native User Interfaces. Meta Platforms. https://react.dev/"),
    ("14", "OpenJS Foundation. (2024). Node.js v18 LTS Documentation: Asynchronous Event-Driven JavaScript Runtime. https://nodejs.org/docs/latest-v18.x/"),
    ("15", "Igor Sysoev & Nginx Inc. (2024). Nginx HTTP Server and Reverse Proxy Documentation. F5 Networks. https://nginx.org/en/docs/")
]

