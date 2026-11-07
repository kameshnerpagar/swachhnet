import os
import shutil
import pymupdf

BASE_DIR = r"C:\Users\kames\Documents\Kamesh\Kamesh Agnel\SEM 5\CLOUD\Mini Project\smart-garbage"
USER_UP = r"C:\Users\kames\.gemini\antigravity\brain\faf643b9-e61c-46b8-b189-0c517d8996b5\.user_uploaded"
SHOTS_DIR = os.path.join(BASE_DIR, "docs", "CCL_Project_Report", "screenshots")
os.makedirs(SHOTS_DIR, exist_ok=True)

# 1. Copy Genuine Screenshots
genuine_mapping = [
    ("media_1793269809135_393b4959.jpg", "screenshot_01_user_registration_ui.jpg"),
    ("media_1793273821893_17812609.jpg", "screenshot_02_aws_vpc_console.jpg"),
    ("media_1793273826884_f427afc9.jpg", "screenshot_03_aws_security_groups_console.jpg"),
]

for src_name, dst_name in genuine_mapping:
    src = os.path.join(USER_UP, src_name)
    dst = os.path.join(SHOTS_DIR, dst_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied genuine screenshot: {dst_name}")

# 2. Helper to generate clear, academic-grade evidence placeholders
def generate_placeholder(filename, title, service, path_instruction, verified_details):
    svg = f"""<svg width="800" height="450" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
      <rect width="800" height="450" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" rx="8"/>
      
      <!-- Header Bar -->
      <rect x="0" y="0" width="800" height="50" fill="#1e293b" rx="8 8 0 0"/>
      <text x="25" y="32" fill="#ffffff" font-size="16" font-weight="bold">AWS CONSOLE EVIDENCE PLACEHOLDER: {service}</text>
      <text x="650" y="32" fill="#94a3b8" font-size="12">Region: ap-south-1</text>
      
      <!-- Body Container -->
      <rect x="30" y="75" width="740" height="345" fill="#ffffff" stroke="#93c5fd" stroke-dasharray="6,4" rx="6"/>
      
      <!-- Icon & Title -->
      <circle cx="70" cy="115" r="22" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
      <text x="63" y="122" font-size="18" fill="#1d4ed8" font-weight="bold">📷</text>
      
      <text x="110" y="112" font-size="16" font-weight="bold" fill="#0f172a">{title}</text>
      <text x="110" y="130" font-size="12" fill="#64748b">Console Navigation: {path_instruction}</text>
      
      <!-- Details Card -->
      <rect x="55" y="160" width="690" height="235" fill="#f8fafc" stroke="#e2e8f0" rx="4"/>
      <text x="75" y="185" font-size="13" font-weight="bold" fill="#1e293b">Verified Production Infrastructure Parameters:</text>
    """
    
    y = 212
    for line in verified_details:
        svg += f'<text x="85" y="{y}" font-size="11" fill="#334155">• {line}</text>\n'
        y += 24
        
    svg += f"""
      <text x="75" y="380" font-size="11" fill="#dc2626" font-weight="bold">[ACTION FOR LAB VIVA: Capture full-window AWS Console screenshot from browser and replace this image]</text>
    </svg>
    """
    
    png_path = os.path.join(SHOTS_DIR, filename)
    doc = pymupdf.open("svg", svg.encode("utf-8"))
    pix = doc[0].get_pixmap(dpi=150)
    pix.save(png_path)
    print(f"Generated placeholder: {filename}")

placeholders = [
    (
        "screenshot_04_aws_rds_console.png",
        "Amazon RDS PostgreSQL Database Instance",
        "Amazon RDS",
        "AWS Management Console ➔ RDS ➔ Databases ➔ swachhnet-postgres",
        [
            "DB Identifier: swachhnet-postgres | Status: Available",
            "Engine: PostgreSQL 16.10 | Instance Class: db.t3.micro",
            "Storage: 20 GB gp2 Encrypted (StorageEncrypted: true)",
            "VPC: swachhnet-vpc | DB Subnet Group: swachhnet-db-subnet-group-master",
            "Public Accessibility: No (Private Subnets 10.0.10.0/24 & 10.0.11.0/24)",
            "Security Group: swachhnet-db-sg (Port 5432 inbound from swachhnet-app-sg only)",
            "Endpoint: swachhnet-postgres.cdc8mesu8z3p.ap-south-1.rds.amazonaws.com:5432"
        ]
    ),
    (
        "screenshot_05_aws_s3_console.png",
        "Amazon S3 Evidence Storage Bucket",
        "Amazon S3",
        "AWS Management Console ➔ S3 ➔ Buckets ➔ swachhnet-evidence-078601217335-ap-south-1",
        [
            "Bucket Name: swachhnet-evidence-078601217335-ap-south-1 | Region: ap-south-1",
            "Access: Bucket and objects not public (Block Public Access: ON)",
            "Default Encryption: SSE-S3 (Server-Side Encryption with Amazon S3 managed keys)",
            "Versioning: Enabled | Object Folders: /complaints, /cleanup, /deploy",
            "Access Pattern: Secure Presigned GET URLs with 60-minute expiration for browser viewing"
        ]
    ),
    (
        "screenshot_06_aws_cloudwatch_console.png",
        "Amazon CloudWatch Log Group & Stream",
        "Amazon CloudWatch",
        "AWS Management Console ➔ CloudWatch ➔ Logs ➔ Log groups ➔ /swachhnet/backend",
        [
            "Log Group Name: /swachhnet/backend | Retention: 7 days",
            "Active Log Stream: instance-28799-1793278274195 (PID 28799)",
            "Audit Events: [HTTP_REQUEST], [DB_QUERY], [SLA_BREACH_CHECK], [S3_UPLOAD]",
            "Secret Redaction: Automatically sanitizes passwords and JWT tokens with ***REDACTED***",
            "CloudWatch Alarm: swachhnet-ec2-high-cpu-alarm (EC2 CPUUtilization &gt;= 80% for 10 min)"
        ]
    ),
    (
        "screenshot_07_aws_sqs_console.png",
        "Amazon SQS Decoupled Job Queue & DLQ",
        "Amazon SQS",
        "AWS Management Console ➔ Simple Queue Service ➔ Queues",
        [
            "Primary Queue: swachhnet-jobs-queue (Visibility Timeout: 60s, Retention: 4 days)",
            "Dead Letter Queue: swachhnet-jobs-dlq (Retention: 14 days, maxReceiveCount: 5)",
            "Purpose: Decouples heavy AI vision inference and asynchronous background municipal tasks",
            "Consumer: Built-in worker polling loop in backend/services/sqsService.js"
        ]
    ),
    (
        "screenshot_08_aws_budgets_console.png",
        "AWS Budgets - Zero Cost Safety Control",
        "AWS Budgets",
        "AWS Management Console ➔ Billing and Cost Management ➔ Budgets",
        [
            "Budget Name: SwachhNet-Monthly-Budget",
            "Budget Limit: $10.00 USD / Monthly",
            "Alert Threshold: 80% ($8.00) actual spend notification",
            "Scope: All AWS Services across Mumbai (ap-south-1) region"
        ]
    ),
    (
        "screenshot_09_aws_cloudformation_console.png",
        "AWS CloudFormation Master Stack",
        "AWS CloudFormation",
        "AWS Management Console ➔ CloudFormation ➔ Stacks ➔ swachhnet-prod-stack",
        [
            "Stack Name: swachhnet-prod-stack | Status: CREATE_COMPLETE",
            "Template: swachhnet-all-in-one.yaml (13 KB declarative Infrastructure as Code)",
            "Resources Created: 24 (VPC, Subnets, IGW, RouteTables, SG, IAM, S3, SQS, RDS, EC2, CloudWatch)",
            "Outputs Exported: RDSEndpoint, PublicIp (65.2.180.175), EvidenceBucketName, JobsQueueUrl"
        ]
    ),
    (
        "screenshot_10_live_app_dashboard.png",
        "SwachhNet Live Web Portal on EC2",
        "Live Production Web App",
        "Web Browser ➔ http://65.2.180.175/",
        [
            "Public Endpoint: http://65.2.180.175 (Amazon EC2 Elastic IP)",
            "Web Server: Nginx 1.30.6 (serving React 18 production bundle at /)",
            "Reverse Proxy: Nginx proxying /api/ to internal Express.js server (port 5000)",
            "Health Check Endpoint: http://65.2.180.175/health (Returns 200 OK + PostgreSQL status)",
            "Seeded Accounts: citizen (user@test.com), admin (k_west@bmc.gov.in), driver (driver1@test.com)"
        ]
    )
]

for fname, title, srv, path_inst, details in placeholders:
    generate_placeholder(fname, title, srv, path_inst, details)

print("All screenshots and placeholders configured successfully!")

