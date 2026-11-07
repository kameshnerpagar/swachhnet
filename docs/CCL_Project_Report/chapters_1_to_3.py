# chapters_1_to_3.py
# Detailed chapter texts for Chapter 1, 2, and 3

CH1_SECTIONS = [
    ("1.1 Introduction to Cloud Computing", [
        """Cloud computing represents a paradigm shift in distributed computing and information technology architecture. According to the standard definition provided by the National Institute of Standards and Technology (NIST SP 800-145), cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction.""",
        """The cloud computing ecosystem is architecturally characterized by five essential characteristics: on-demand self-service, broad network access, resource pooling, rapid elasticity, and measured service. Furthermore, computing services are delivered across three recognized service models:""",
        """1. Infrastructure as a Service (IaaS): Provides fundamental computing capabilities such as physical or virtual servers (e.g., Amazon EC2), storage volumes, and network components (e.g., Amazon VPC). Users maintain administrative control over the operating system, middleware, and application runtime while the cloud vendor manages the underlying hypervisor and physical hardware.""",
        """2. Platform as a Service (PaaS): Provides higher-level environments where hardware and software tools are provisioned to deploy customer applications without managing underlying operating system updates or network topologies (e.g., Amazon RDS, AWS Elastic Beanstalk).""",
        """3. Software as a Service (SaaS): Delivers fully managed, ready-to-use software applications over the internet to end users, completely abstracting infrastructure, middleware, and codebase maintenance.""",
        """In municipal management and smart governance, cloud computing affords critical advantages: operational elasticity allows civic infrastructure to gracefully accommodate severe query surges during monsoon emergencies or municipal sanitation drives; geo-redundancy guarantees continuous operational uptime; and pay-as-you-go financial models prevent municipal capital expenditure overruns."""
    ]),
    ("1.2 Introduction to SwachhNet", [
        """SwachhNet is an intelligent, cloud-native municipal solid waste management and automated dispatch platform specifically modeled around the administrative structure of the Brihanmumbai Municipal Corporation (BMC). Designed to bridge the operational gap between citizen grievance reporting and municipal field execution, SwachhNet replaces bureaucratic manual ticketing with a transparent, spatial, and verifiable workflow.""",
        """The platform enables citizens across Mumbai to report localized garbage accumulations by taking live smartphone photographs and auto-detecting GPS coordinates. Submitted images are audited in real time using multimodal generative artificial intelligence (Google Gemini Flash Vision) to prevent spam submissions. Once validated, complaints are mapped to the nearest BMC ward authority via geospatial Haversine distance computations. Ward administrators dispatch the closest idle municipal garbage collection truck, whose driver receives geographic turn-by-turn coordinates. Upon arriving and clearing the waste, the sanitation worker captures a physical cleanup photo, which the AI engine automatically compares against the initial complaint image before granting resolution.""",
        """Originally developed as a local academic prototype, SwachhNet has been comprehensively refactored and deployed to Amazon Web Services (AWS) in the Asia Pacific (Mumbai) region (ap-south-1). It incorporates managed database services (Amazon RDS PostgreSQL), scalable compute (Amazon EC2 with Nginx), secure encrypted object storage (Amazon S3), asynchronous queue buffering (Amazon SQS), centralized secrets management (AWS SSM Parameter Store), real-time audit logging (Amazon CloudWatch), and automated Infrastructure as Code (AWS CloudFormation)."""
    ]),
    ("1.3 Background and Motivation", [
        """The metropolitan area of Mumbai generates approximately 11,000 metric tons of municipal solid waste every single day across an expanse of over 600 square kilometers inhabited by more than 20 million citizens. The Brihanmumbai Municipal Corporation (BMC) administers this immense territory across 24 administrative wards (such as K/West - Andheri, H/West - Bandra, P/South - Goregaon).""",
        """Despite substantial investments in municipal transport and street cleaning personnel, urban centers suffer from chronic uncollected waste spots, illegal open dumping, and delayed garbage bin clearances. Traditional citizen reporting relies on paper registrations, telephone helplines, or generic grievance portals where complaints languish for days without physical inspection. Sanitation trucks frequently operate on static, unoptimized routes without real-time responsiveness to newly reported heaps.""",
        """The motivation behind SwachhNet is to leverage modern cloud infrastructure and artificial intelligence to establish a participatory civic ecosystem. By enabling instantaneous citizen reporting, automated spatial triage, and verifiable before-and-after photographic evidence, municipal accountability is enforced by design, transforming civic hygiene from a reactive chore into a transparent, metric-driven municipal operation."""
    ]),
    ("1.4 Problem Statement", [
        """Traditional municipal waste collection and grievance management systems in Indian metropolitan cities suffer from severe systemic shortcomings:""",
        """1. Lack of Verifiable Evidence: Complaints lack cryptographic or spatial verification, leading to bogus reports and ghost cleanups where workers claim completion without visiting the site.""",
        """2. Manual and Inefficient Triage: Incoming complaints are manually categorized, leading to inter-ward jurisdiction disputes and delayed routing.""",
        """3. Absence of Fleet Optimization: Municipal sanitation vehicles lack dynamic dispatching, resulting in idle trucks remaining stationary while nearby waste piles overflow.""",
        """4. Lack of Citizen Incentivization: Citizens receive zero feedback regarding reported grievances, extinguishing civic participation.""",
        """5. Unmonitored SLA Breaches: Municipal commissioners lack centralized visibility into wards where grievances exceed the mandatory 48-hour service level agreement (SLA) threshold."""
    ]),
    ("1.5 Existing System Analysis", [
        """Prior to its cloud transformation, SwachhNet existed as an initial full-stack prototype originally authored for the Technology Innovation and Software Development (TISD) course. This preliminary architecture comprised:""",
        """• Frontend: React 18 Single Page Application running strictly on local Node.js development servers (localhost:3000).""",
        """• Backend: Monolithic Express.js server hosted on developer machines (localhost:5000).""",
        """• Database: MongoDB Atlas cloud cluster utilizing Mongoose ODM schemas.""",
        """• Media Storage: Cloudinary third-party image hosting.""",
        """• Authentication: Hardcoded JSON Web Tokens utilizing local .env file variables."""
    ]),
    ("1.6 Limitations of the Existing System", [
        """The initial implementation suffered from critical enterprise and cloud limitations:""",
        """1. Unmanaged and Fragmented Infrastructure: Hosting the backend and frontend on arbitrary local developer environments created severe availability vulnerabilities and zero fault tolerance.""",
        """2. Third-Party Vendor Lock-In: Relying on Cloudinary and MongoDB Atlas fractured application data across unrelated external platforms without enterprise security boundaries or centralized billing control.""",
        """3. No Network Segmentation or Boundary Isolation: MongoDB Atlas and Cloudinary endpoints communicated over public internet channels without private subnet isolation, exposing database connection strings and secrets.""",
        """4. Absence of Infrastructure as Code (IaC): Environments could not be reproducibly deployed, repaired, or audited; provisioning required manual, error-prone console steps.""",
        """5. Complete Absence of Cloud Monitoring: There were no automated mechanisms to track CPU spikes, application errors, memory leaks, or financial expenditures, violating core enterprise standards."""
    ]),
    ("1.7 Proposed Cloud-Based System", [
        """The proposed system completely transforms SwachhNet into an enterprise-grade, cloud-native architecture deployed within Amazon Web Services (AWS) ap-south-1 (Mumbai). The proposed architecture introduces:""",
        """1. Custom Amazon Virtual Private Cloud (VPC): A dedicated 10.0.0.0/16 virtual network with segregated public subnets (10.0.1.0/24) for internet-facing compute and private subnets (10.0.10.0/24, 10.0.11.0/24) for isolated database storage.""",
        """2. High-Performance Relational Database (Amazon RDS PostgreSQL 16.10): Migrates all application state from MongoDB Atlas to a fully managed, encrypted relational schema with transactional integrity and geospatial Haversine math.""",
        """3. Secure Compute Layer (Amazon EC2 & Nginx): Hosts both the built React 18 SPA and the Node.js API behind a battle-tested Nginx reverse proxy with PM2 process daemonization and systemd auto-restart.""",
        """4. Private Object Storage (Amazon S3): Stores all photographic evidence inside a private bucket with server-side AES-256 encryption, zero public read access, and time-bound 60-minute presigned URLs.""",
        """5. Centralized Secrets Management (AWS SSM Parameter Store): Eliminates plain-text environment files by securely loading encrypted credentials directly from SSM at server bootstrap.""",
        """6. Asynchronous Task Buffering (Amazon SQS): Decouples heavy AI vision inference and audit notifications into a durable message queue with an integrated Dead Letter Queue (DLQ).""",
        """7. Comprehensive Telemetry (Amazon CloudWatch & Budgets): Streams structured application logs with automated secret redaction, tracks CPU utilization alarms, and enforces a strict $10.00/month cost ceiling.""",
        """8. Single-Click Declarative IaC (AWS CloudFormation): Provisions all 24 cloud resources deterministically using a unified YAML template."""
    ]),
    ("1.8 Project Objectives", [
        """The primary objectives of this Cloud Computing Laboratory mini-project are:""",
        """1. To design and deploy a secure, custom Amazon VPC architecture with public-private subnet isolation and least-privilege security groups in the Mumbai region.""",
        """2. To migrate application persistence from MongoDB Atlas to Amazon RDS PostgreSQL, implementing a clean relational schema, transactional foreign keys, and SQL-level Haversine distance computations.""",
        """3. To deploy and host the complete full-stack application on an Amazon EC2 instance running Amazon Linux 2023, configuring Nginx as a reverse proxy and PM2 as a resilient process manager.""",
        """4. To integrate private Amazon S3 object storage with server-side encryption and implement secure presigned URL generation for evidence retrieval.""",
        """5. To enforce cloud security best practices by implementing AWS IAM instance roles, least-privilege security group ingress, and AWS SSM Parameter Store SecureString encryption.""",
        """6. To decouple background municipal events using Amazon SQS queues and implement Dead Letter Queue fault handling.""",
        """7. To implement centralized monitoring, structured log streaming, and metric alarm triggers via Amazon CloudWatch, accompanied by AWS Budgets financial governance.""",
        """8. To automate full-stack provisioning via AWS CloudFormation templates and verify end-to-end functionality at the public endpoint http://65.2.180.175."""
    ]),
    ("1.9 Scope of the Project", [
        """The operational scope of SwachhNet encompasses:""",
        """• Spatial Coverage: The 24 administrative municipal wards of Greater Mumbai, with initial development seeding covering 8 key BMC wards (Andheri West, Bandra, Goregaon, Malad, Kurla, Dadar, Borivali, Chembur).""",
        """• User Personas: Citizens, Ward Sanitation Administrators, Field Truck Drivers / Workers, and the Central Municipal Commissioner.""",
        """• Functional Workflow: Complaint logging, AI validation, geospatial dispatching, before/after cleanup verification, and 48-hour SLA breach escalation.""",
        """• Cloud Infrastructure: All AWS compute, database, network, storage, security, and messaging components provisioned in the ap-south-1 region."""
    ]),
    ("1.10 Advantages of the Proposed Cloud Architecture", [
        """The deployed cloud architecture provides profound technical and municipal advantages:""",
        """• Enhanced Data Confidentiality: Isolating PostgreSQL within private subnets prevents external SQL injection vectors and direct internet probing.""",
        """• Elastic Performance: Nginx reverse proxying combined with PM2 clustering ensures high concurrency and sub-second response times.""",
        """• Cost Predictability: Operating within AWS Free Tier parameters alongside an active $10.00 AWS Budget alert ensures near-zero operational costs for municipal demonstrations.""",
        """• Verifiable Accountability: Cryptographic presigned S3 URLs combined with CloudWatch audit logging prevent rogue municipal claims and ensure complete audit trails."""
    ])
]

# -------------------------------------------------------------
# CHAPTER 2: LITERATURE REVIEW & TECHNOLOGY OVERVIEW
# -------------------------------------------------------------
CH2_TECH = [
    {
        "name": "2.1 React 18 & Vite Build Tool",
        "what": "React 18 is an industry-standard open-source JavaScript library developed by Meta for building dynamic, reactive user interfaces via a virtual Document Object Model (DOM). Vite is a next-generation frontend development server and bundler utilizing native ES modules and Rollup.",
        "why": "React's component-based modularity enables seamless state management across citizen reporting maps, administrative dispatch consoles, and analytical dashboards. Vite provides sub-second hot module replacement and produces optimized, minified production assets.",
        "role": "Powers the entire client-tier Single Page Application (SPA), rendering responsive interfaces for citizens, ward admins, workers, and superadmins."
    },
    {
        "name": "2.2 Node.js & Express.js Framework",
        "what": "Node.js is an open-source, cross-platform JavaScript runtime environment built on Google Chrome's V8 engine that executes JavaScript code outside a web browser using an event-driven, non-blocking I/O model. Express.js is a minimal and flexible Node.js web application framework.",
        "why": "The asynchronous, single-threaded event loop of Node.js excels at I/O-intensive workloads such as processing multipart image uploads, querying relational databases, and invoking external AWS SDK and AI APIs without thread-blocking latency.",
        "role": "Serves as the central RESTful API gateway, managing client requests, orchestrating business logic, enforcing role-based access control, and interfacing with PostgreSQL and AWS services."
    },
    {
        "name": "2.3 Amazon Relational Database Service (RDS for PostgreSQL)",
        "what": "Amazon RDS is a fully managed relational database cloud service that automates hardware provisioning, database setup, patching, backups, and encryption. PostgreSQL is an advanced enterprise-grade open-source object-relational database management system.",
        "why": "Unlike unstructured NoSQL databases, PostgreSQL enforces strict schema validation, ACID transactional guarantees, foreign key referential integrity, and powerful mathematical querying capabilities required for civic accountability.",
        "role": "Functions as the single source of truth for SwachhNet, securely storing user identities, ward boundaries, fleet locations, complaints, and audit history inside isolated private subnets."
    },
    {
        "name": "2.4 Amazon Elastic Compute Cloud (EC2)",
        "what": "Amazon EC2 provides scalable, resizable compute capacity in the cloud, allowing developers to launch virtual computing environments (instances) with custom operating systems, network associations, and storage.",
        "why": "EC2 offers full administrative control over the operating system environment (Amazon Linux 2023), allowing installation of custom software stacks including Node.js 18, PM2, and Nginx without PaaS runtime constraints.",
        "role": "Acts as the unified application compute host in the public subnet (IP: 65.2.180.175), running the Nginx web server and daemonized Express.js backend."
    },
    {
        "name": "2.5 Amazon Virtual Private Cloud (VPC)",
        "what": "Amazon VPC allows developers to provision a logically isolated section of the AWS Cloud where resources run in a virtual network defined by custom IP address ranges, subnets, route tables, and network gateways.",
        "why": "Enterprise cloud security mandates network perimeter defense. A custom VPC prevents default VPC security flaws and enforces strict segregation between public-facing web components and sensitive database storage.",
        "role": "Encapsulates the entire SwachhNet cloud infrastructure (10.0.0.0/16) across the Mumbai region, establishing dedicated public and private subnets and least-privilege security groups."
    },
    {
        "name": "2.6 Amazon Simple Storage Service (S3)",
        "what": "Amazon S3 is an industry-leading object storage service offering 99.999999999% (11 9s) of data durability, industry-standard scalability, security, and performance.",
        "why": "Storing high-resolution civic evidence images directly in relational databases leads to database bloat and performance degradation. S3 provides unlimited, inexpensive, and encrypted storage specifically engineered for binary media.",
        "role": "Stores all photographic evidence (complaints/ and cleanup/ folders) with AES-256 server-side encryption, blocking public access and generating 60-minute presigned URLs for authenticated viewing."
    },
    {
        "name": "2.7 AWS Identity and Access Management (IAM)",
        "what": "AWS IAM is a web service that enables fine-grained access control across AWS services and resources by creating users, groups, roles, and JSON-defined permission policies.",
        "why": "Hardcoding AWS access keys inside server code or configuration files creates catastrophic security vulnerabilities. IAM roles allow EC2 instances to securely assume temporary credentials via the AWS Security Token Service (STS).",
        "role": "Provides the EC2 instance role (swachhnet-unified-role) and instance profile, granting least-privilege permissions to access S3 buckets, SSM parameters, SQS queues, and CloudWatch log groups."
    },
    {
        "name": "2.8 AWS Systems Manager (SSM) Parameter Store",
        "what": "AWS Systems Manager Parameter Store provides secure, centralized, hierarchical storage for configuration data management and secrets management with native AWS KMS encryption.",
        "why": "Storing sensitive connection strings, JWT secrets, and API keys in .env files on disk introduces leakage risks. Parameter Store centralizes secret management with fine-grained encryption and version history.",
        "role": "Stores database connection strings, JWT secret keys, and Google Gemini API keys under the /swachhnet/prod/ namespace as SecureString parameters."
    },
    {
        "name": "2.9 Amazon Simple Queue Service (SQS) & DLQ",
        "what": "Amazon SQS is a fully managed message queuing service that enables decoupling and scaling of microservices, distributed systems, and serverless applications.",
        "why": "Synchronously processing compute-intensive image validation or dispatch routines during user complaint submission increases API latency and creates failure points. SQS buffers incoming tasks durably.",
        "role": "Receives and buffers background municipal tasks (swachhnet-jobs-queue), with unprocessable messages routed to a Dead Letter Queue (swachhnet-jobs-dlq) after 5 failed attempts."
    },
    {
        "name": "2.10 Amazon CloudWatch & CloudWatch Logs",
        "what": "Amazon CloudWatch is a monitoring and observability service that collects monitoring and operational data in the form of logs, metrics, and events across AWS resources.",
        "why": "Provides centralized observability into system health, application errors, and resource utilization without requiring manual SSH sessions to inspect local log files.",
        "role": "Collects structured application logs in the /swachhnet/backend log group and monitors EC2 CPU utilization with an alarm configured at 80% capacity."
    },
    {
        "name": "2.11 AWS Budgets",
        "what": "AWS Budgets allows organizations to track and manage their AWS costs and usage, setting custom alerts when spending exceeds budgeted thresholds.",
        "why": "Prevents accidental billing overruns caused by unintended cloud resource consumption during academic laboratory experimentation.",
        "role": "Enforces a strict $10.00/month spending limit (SwachhNet-Monthly-Budget), triggering notification warnings when expenditure crosses 80% ($8.00)."
    },
    {
        "name": "2.12 AWS CloudFormation",
        "what": "AWS CloudFormation is an Infrastructure as Code (IaC) service that allows developers to model, provision, and manage AWS and third-party resources declaratively using JSON or YAML templates.",
        "why": "Manual point-and-click infrastructure creation is non-reproducible, prone to configuration drift, and difficult to audit. CloudFormation ensures repeatable, deterministic deployments.",
        "role": "Automates the unified deployment of all 24 SwachhNet cloud resources (VPC, subnets, route tables, security groups, IAM roles, S3, SQS, RDS, EC2, CloudWatch) via swachhnet-all-in-one.yaml."
    },
    {
        "name": "2.13 Google Gemini Flash Generative AI",
        "what": "Google Gemini is an advanced multimodal generative AI model developed by Google DeepMind capable of native multimodal reasoning across text, code, images, and audio.",
        "why": "Eliminates citizen spam and fraudulent complaint submissions by performing visual semantic reasoning on uploaded photographs in real time.",
        "role": "Executes two critical verification pipelines: (1) Initial complaint validation to confirm presence of physical garbage; (2) Before-and-after photographic differential analysis to verify cleanup completion."
    },
    {
        "name": "2.14 Nginx & PM2 Process Manager",
        "what": "Nginx is a high-performance HTTP web server, reverse proxy, and load balancer. PM2 is an enterprise-grade production process manager for Node.js applications.",
        "why": "Running Node.js directly on port 80 is insecure and exposes applications to crash outages. Nginx handles static file caching and TLS termination, while PM2 ensures automatic process respawning upon failure.",
        "role": "Nginx serves built React SPA files and reverse-proxies /api/ calls to localhost:5000; PM2 daemonizes the backend server and ensures automatic boot on EC2 restart."
    },
    {
        "name": "2.15 Leaflet & OpenStreetMap",
        "what": "Leaflet is the leading open-source JavaScript library for mobile-friendly interactive maps, integrated with OpenStreetMap geospatial tiles.",
        "why": "Provides smooth, lightweight geospatial mapping without requiring costly commercial mapping API licenses.",
        "role": "Renders interactive complaint location maps, ward boundaries, and truck driver navigation pins across citizen, admin, and worker dashboards."
    }
]

# -------------------------------------------------------------
# CHAPTER 3: SYSTEM ANALYSIS & REQUIREMENTS
# -------------------------------------------------------------
FUNC_REQ_TABLE = [
    ("FR-01", "Citizen Registration & Login", "Citizens must register with name, email, and password. Passwords must be hashed via bcrypt; sessions authenticated via JWT.", "High"),
    ("FR-02", "GPS & Photo Garbage Reporting", "Citizens must be able to capture or upload a garbage photograph and automatically capture device GPS coordinates.", "High"),
    ("FR-03", "AI-Based Spam & Image Validation", "Uploaded complaint photographs must be evaluated by Gemini Vision AI to verify that actual municipal solid waste is present.", "High"),
    ("FR-04", "Geospatial Ward Partitioning", "The system must automatically assign each complaint to the geographically closest BMC ward using the Haversine distance formula.", "High"),
    ("FR-05", "Nearest Idle Truck Dispatch", "Ward administrators must be able to query the nearest available municipal garbage truck and assign it to an open complaint in one click.", "High"),
    ("FR-06", "Sanitation Worker Task View", "Assigned truck drivers must view real-time task locations, navigation coordinates, and complaint descriptions on their portal.", "High"),
    ("FR-07", "Cleanup Evidence Submission", "Workers must capture and upload a photographic cleanup proof upon completing physical site waste removal.", "High"),
    ("FR-08", "Before/After AI Verification", "The AI engine must compare initial complaint photos against cleanup photos to verify that the waste was satisfactorily removed.", "High"),
    ("FR-09", "Gamification Points & Badges", "Citizens must earn 10 eco-points upon verified resolution of their complaint, progressing through Bronze, Silver, and Gold tiers.", "Medium"),
    ("FR-10", "Citizen Feedback & Ward Ratings", "Resolved complaints must allow citizens to submit a 1-to-5 star rating and comments, updating aggregate ward performance scores.", "Medium"),
    ("FR-11", "48-Hour SLA Breach Tracking", "The system must identify unresolved complaints exceeding 48 hours and escalate alerts to ward admins and the central commissioner.", "High"),
    ("FR-12", "City-Wide Superadmin Analytics", "Central authorities must view holistic metrics, total complaints, ward resolution percentages, and breached complaint counts.", "Medium")
]

NON_FUNC_REQ_TABLE = [
    ("NFR-01", "Availability", "The web application and API must maintain 99.5% uptime during operational municipal hours.", "Measured via CloudWatch Uptime & Health Endpoint"),
    ("NFR-02", "Performance & Latency", "API endpoints must respond in under 500ms; AI image verification must complete within 3.5 seconds.", "Measured via CloudWatch Request Latency"),
    ("NFR-03", "Security & Data Protection", "Database must reside in private subnets with zero direct internet access; S3 objects must use AES-256 SSE encryption.", "AWS Trusted Advisor & Security Group Ingress Rules"),
    ("NFR-04", "Scalability", "System architecture must support decoupled queue processing via SQS to absorb burst complaint filings without API failure.", "Simulated load testing via concurrent request scripts"),
    ("NFR-05", "Maintainability & Portability", "Infrastructure must be 100% reproducible through declarative CloudFormation templates without manual setup.", "Template validation via `aws cloudformation validate-template`"),
    ("NFR-06", "Cost Efficiency", "Total ongoing cloud expenditure must stay strictly below $10.00/month, leveraging AWS Free Tier allowances.", "Tracked via AWS Budgets and Cost Explorer")
]

USER_ROLES_TABLE = [
    ("Citizen (Nagarik)", "File complaints, upload evidence, track progress, view interactive city map, receive points/badges, submit ratings.", "Citizen Dashboard (/dashboard)"),
    ("Ward Administrator", "View all complaints within assigned ward, execute Haversine dispatch to nearest idle truck, transfer complaints to adjacent wards.", "Ward Admin Portal (/authority)"),
    ("Sanitation Worker", "View assigned tasks, access complaint coordinates, navigate to site, upload after-cleanup evidence photo, complete job.", "Worker Task Portal (/worker)"),
    ("Central Superadmin", "Monitor all 24 BMC wards, track city-wide complaint statistics, audit 48-hour SLA breaches, inspect operational bottlenecks.", "Central Command Dashboard (/central)")
]

