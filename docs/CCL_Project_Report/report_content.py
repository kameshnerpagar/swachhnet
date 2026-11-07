# report_content.py
# Contains all structured academic text, tables, and code snippets for SwachhNet CCL Report

COVER_PAGE_DATA = {
    "title": "SwachhNet: AI-Powered Smart Garbage Reporting and Municipal Dispatch System",
    "subtitle": "A Cloud-Native Municipal Solid Waste Management Platform Built on Amazon Web Services (AWS)",
    "course": "Cloud Computing Lab (CCL) Mini Project Report",
    "degree": "Bachelor of Engineering in Computer Engineering",
    "academic_year": "Academic Year: 2026 – 2027",
    "students": [
        {"name": "Kamesh Nerpagar", "roll": "Roll No: [ROLL NO. 1]"},
        {"name": "[STUDENT 2 NAME]", "roll": "Roll No: [ROLL NO. 2]"}
    ],
    "guide": "Prof. [GUIDE NAME]",
    "guide_desig": "Assistant Professor, Department of Computer Engineering",
    "department": "Department of Computer Engineering",
    "institution": "[COLLEGE / INSTITUTION NAME]",
    "location": "Mumbai, Maharashtra, India"
}

CERTIFICATE_TEXT = """This is to certify that the mini-project report entitled "SwachhNet: AI-Powered Smart Garbage Reporting and Municipal Dispatch System" is a bona fide work carried out by Kamesh Nerpagar (Roll No: [ROLL NO. 1]) and [STUDENT 2 NAME] (Roll No: [ROLL NO. 2]) in partial fulfillment of the requirements for the award of the Degree of Bachelor of Engineering in Computer Engineering in Cloud Computing Laboratory during the academic year 2026–2027.

The project has been executed under our supervision and guidance, and the infrastructure has been deployed, tested, and verified on Amazon Web Services (AWS)."""

DECLARATION_TEXT = """We hereby declare that the mini-project entitled "SwachhNet: AI-Powered Smart Garbage Reporting and Municipal Dispatch System" submitted for the Cloud Computing Laboratory examination is our original work conducted under the guidance of Prof. [GUIDE NAME]. 

The information and empirical findings presented in this report represent actual software implementations, database schemas, and cloud infrastructure provisioned in the Amazon Web Services (AWS) Asia Pacific (Mumbai) region (ap-south-1). Any material or reference drawn from external literature, documentation, or cloud providers has been properly cited and acknowledged."""

ACKNOWLEDGEMENT_TEXT = """We express our deepest gratitude to our project guide, Prof. [GUIDE NAME], for their constant encouragement, invaluable suggestions, and constructive guidance throughout the duration of this Cloud Computing Lab project. 

We are also thankful to the Head of the Department of Computer Engineering and the faculty members of the Cloud Computing Laboratory for providing state-of-the-art laboratory facilities and technical support. Finally, we thank our peers and families for their continuous motivation and support during the design, cloud deployment, and documentation phases of this project."""

ABSTRACT_TEXT = """Rapid urbanization and escalating municipal solid waste generation pose critical operational challenges for metropolitan governance bodies like the Brihanmumbai Municipal Corporation (BMC). Traditional grievance redressal mechanisms are predominantly centralized, manually mediated, lack automated spatial triage, and exhibit poor accountability due to absence of verifiable physical evidence. 

This project presents SwachhNet, an enterprise-grade, cloud-native municipal solid waste reporting and automated dispatch platform architected on Amazon Web Services (AWS). SwachhNet facilitates end-to-end municipal grievance handling: citizens report localized garbage dumps with real-time GPS coordinates and camera captures; multimodal artificial intelligence (Google Gemini Vision) autonomously audits photographs to reject fraudulent submissions; geospatial Haversine algorithms dynamically partition and route complaints to the appropriate administrative ward; and automated dispatch mechanisms assign the nearest idle municipal garbage truck. Upon sanitation completion, workers submit photographic evidence, which undergoes before-and-after visual differential verification before a complaint is marked resolved.

To satisfy the requirements of the Cloud Computing Laboratory (CCL) curriculum, the system underwent a complete cloud transformation from a monolithic local architecture into a decoupled, highly secure, and cost-optimized AWS infrastructure deployed in the Mumbai (ap-south-1) region. The production cloud architecture features: (1) a custom Amazon VPC (10.0.0.0/16) with segregated public and multi-AZ private subnets; (2) Amazon EC2 (t3.micro) compute running Nginx as a reverse proxy and Express.js daemonized via PM2; (3) Amazon RDS for PostgreSQL 16.10 (db.t3.micro) housed within an isolated private DB subnet group with zero public internet exposure; (4) Amazon S3 private object storage with AES-256 server-side encryption and 60-minute presigned URL security; (5) AWS IAM instance profiles enforcing least-privilege security; (6) AWS Systems Manager (SSM) Parameter Store for centralized encrypted configuration; (7) Amazon SQS with a Dead Letter Queue (DLQ) for asynchronous background task processing; (8) Amazon CloudWatch for centralized application log streaming and metric alarms; (9) AWS Budgets enforcing a strict $10.00/month cost ceiling; and (10) AWS CloudFormation delivering single-click Infrastructure as Code (IaC) deployment. The system is fully operational at public endpoint http://65.2.180.175, achieving sub-second API latencies, zero database internet exposure, and 100% automated municipal dispatching."""

ABBREVIATIONS = [
    ("AWS", "Amazon Web Services"),
    ("VPC", "Virtual Private Cloud"),
    ("EC2", "Elastic Compute Cloud"),
    ("RDS", "Relational Database Service"),
    ("S3", "Simple Storage Service"),
    ("IAM", "Identity and Access Management"),
    ("SSM", "Systems Manager"),
    ("SQS", "Simple Queue Service"),
    ("DLQ", "Dead Letter Queue"),
    ("IGW", "Internet Gateway"),
    ("CIDR", "Classless Inter-Domain Routing"),
    ("BMC", "Brihanmumbai Municipal Corporation"),
    ("SLA", "Service Level Agreement"),
    ("SPA", "Single Page Application"),
    ("API", "Application Programming Interface"),
    ("JWT", "JSON Web Token"),
    ("RBAC", "Role-Based Access Control"),
    ("IaC", "Infrastructure as Code"),
    ("SSE", "Server-Side Encryption"),
    ("URL", "Uniform Resource Locator"),
    ("DFD", "Data Flow Diagram"),
    ("ERD", "Entity-Relationship Diagram")
]

TABLE_OF_CONTENTS = [
    ("Preliminary Pages", [
        "Certificate",
        "Declaration",
        "Acknowledgement",
        "Abstract",
        "List of Abbreviations",
        "List of Figures",
        "List of Tables"
    ]),
    ("Chapter 1: Introduction", [
        "1.1 Introduction to Cloud Computing",
        "1.2 Introduction to SwachhNet",
        "1.3 Background and Motivation",
        "1.4 Problem Statement",
        "1.5 Existing System Analysis",
        "1.6 Limitations of the Existing System",
        "1.7 Proposed Cloud-Based System",
        "1.8 Project Objectives",
        "1.9 Scope of the Project",
        "1.10 Advantages of the Proposed Cloud Architecture"
    ]),
    ("Chapter 2: Literature Review & Technology Overview", [
        "2.1 Overview of Modern Cloud Architecture",
        "2.2 Frontend Framework (React 18 & Vite)",
        "2.3 Backend Runtime & Framework (Node.js & Express.js)",
        "2.4 Managed Relational Database (Amazon RDS PostgreSQL)",
        "2.5 Virtual Compute Infrastructure (Amazon EC2)",
        "2.6 Private Cloud Isolation (Amazon VPC)",
        "2.7 Secure Object Storage (Amazon S3)",
        "2.8 Identity & Access Management (AWS IAM)",
        "2.9 Configuration Management (AWS SSM Parameter Store)",
        "2.10 Asynchronous Messaging & Buffering (Amazon SQS)",
        "2.11 Telemetry & Monitoring (Amazon CloudWatch)",
        "2.12 Financial Governance (AWS Budgets)",
        "2.13 Infrastructure as Code (AWS CloudFormation)",
        "2.14 Artificial Intelligence (Google Gemini Vision API)",
        "2.15 Token Security & Geospatial Libraries (JWT & Leaflet)"
    ]),
    ("Chapter 3: System Analysis & Requirements", [
        "3.1 Functional Requirements",
        "3.2 Non-Functional Requirements",
        "3.3 Hardware Requirements (Development & Production)",
        "3.4 Software Requirements",
        "3.5 Cloud Infrastructure Requirements",
        "3.6 User Roles & Privilege Matrix",
        "3.7 Feasibility Study (Technical, Economic, Operational)",
        "3.8 Cloud Security & Boundary Requirements"
    ]),
    ("Chapter 4: System Architecture & Design", [
        "4.1 Overall SwachhNet Cloud Architecture",
        "4.2 Amazon VPC Network & Subnet Topography",
        "4.3 Multi-Tier Software Architecture",
        "4.4 Relational Database Design (PostgreSQL Schema & ERD)",
        "4.5 UML Use Case Modeling",
        "4.6 Data Flow Modeling (Level 0 Context & Level 1 DFD)",
        "4.7 Core Municipal Workflows (Complaint, Dispatch, Cleanup, SLA)"
    ]),
    ("Chapter 5: AWS Cloud Services Integration", [
        "5.1 Amazon Virtual Private Cloud (VPC)",
        "5.2 Amazon Elastic Compute Cloud (EC2)",
        "5.3 Amazon Relational Database Service (RDS for PostgreSQL)",
        "5.4 Amazon Simple Storage Service (S3)",
        "5.5 AWS Identity and Access Management (IAM)",
        "5.6 AWS Systems Manager (SSM) Parameter Store",
        "5.7 Amazon Simple Queue Service (SQS) & DLQ",
        "5.8 Amazon CloudWatch Monitoring & Metrics",
        "5.9 AWS Budgets & Cost Governance",
        "5.10 AWS CloudFormation (Infrastructure as Code)",
        "5.11 Comprehensive Service Mapping & Curriculum Compliance"
    ]),
    ("Chapter 6: Implementation & Working", [
        "6.1 Frontend User Interface Implementation",
        "6.2 Backend Dual-Database Engine Bootstrap",
        "6.3 Authentication & Role-Based Middleware",
        "6.4 Database Pool, Migrations & Transaction Helpers",
        "6.5 Amazon S3 Evidence Upload & Presigned URL Resolution",
        "6.6 Multimodal AI Visual Verification Engine",
        "6.7 Geospatial Ward Partitioning (Haversine SQL)",
        "6.8 Automated Nearest Truck Dispatch Mechanism",
        "6.9 Sanitation Worker Task Life Cycle",
        "6.10 Before-and-After Verification Algorithm",
        "6.11 Citizen Reward Points & Badging Gamification",
        "6.12 48-Hour SLA Breach Background Evaluation",
        "6.13 Asynchronous Worker Polling via Amazon SQS",
        "6.14 CloudWatch Structured Logging with PII Sanitization"
    ]),
    ("Chapter 7: Deployment & Configuration", [
        "7.1 Pre-Deployment Prerequisites & IAM Credentials",
        "7.2 Declarative Infrastructure Provisioning (CloudFormation)",
        "7.3 Parameter Store Secret Population",
        "7.4 Amazon EC2 Host Bootstrapping & Nginx Configuration",
        "7.5 Database Migrations & BMC Seed Execution",
        "7.6 PM2 Process Daemonization & Startup Hooks",
        "7.7 Production Verification & Health Probes"
    ]),
    ("Chapter 8: Testing & Results", [
        "8.1 Testing Methodology",
        "8.2 Comprehensive Test Suite (20 Test Scenarios)",
        "8.3 Empirical Test Execution Results",
        "8.4 Cloud Evidence & Console Verification Gallery"
    ]),
    ("Chapter 9: Cost Analysis & Cloud Security", [
        "9.1 Monthly Cloud Infrastructure Cost Breakdown",
        "9.2 AWS Free Tier Utilization & Optimization Strategies",
        "9.3 Multi-Layered Defense-in-Depth Security Architecture"
    ]),
    ("Chapter 10: Conclusion & Future Scope", [
        "10.1 Project Summary & Achievements",
        "10.2 Academic & Practical Cloud Principles Demonstrated",
        "10.3 Limitations of Current Implementation",
        "10.4 Future Roadmap & Enhancements"
    ]),
    ("References", [
        "Academic & Professional Citations"
    ])
]

