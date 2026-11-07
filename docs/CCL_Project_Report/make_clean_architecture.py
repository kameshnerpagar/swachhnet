import os
import pymupdf

BASE_DIR = r"C:\Users\kames\Documents\Kamesh\Kamesh Agnel\SEM 5\CLOUD\Mini Project\smart-garbage"
ARCH_DIR = os.path.join(BASE_DIR, "docs", "CCL_Project_Report", "architecture")
os.makedirs(ARCH_DIR, exist_ok=True)

# Clean, unified, single-screen architecture SVG
# Dimensions: 1200 x 820
svg_unified = """<svg width="1200" height="820" viewBox="0 0 1200 820" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif">
  <defs>
    <!-- Filter for clean card elevation -->
    <filter id="cardShadow" x="-2%" y="-2%" width="104%" height="106%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>

    <!-- Arrow markers -->
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#7c3aed"/>
    </marker>
    <marker id="arrow-slate" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569"/>
    </marker>
  </defs>

  <!-- Canvas Background -->
  <rect width="1200" height="820" fill="#f8fafc" rx="12"/>

  <!-- Top Title Banner -->
  <rect x="30" y="20" width="1140" height="56" rx="8" fill="#0f172a"/>
  <text x="50" y="55" fill="#ffffff" font-size="20" font-weight="700" letter-spacing="0.3">SwachhNet — End-to-End AWS Production Architecture</text>
  <text x="960" y="54" fill="#94a3b8" font-size="13" font-weight="500">Region: ap-south-1 (Mumbai)</text>

  <!-- ======================================================== -->
  <!-- 1. CLIENT LAYER (TOP)                                    -->
  <!-- ======================================================== -->
  <rect x="30" y="92" width="760" height="76" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="50" y="114" font-size="12" font-weight="700" fill="#475569" letter-spacing="0.5">CLIENT LAYER (WEB BROWSERS / MOBILE CLIENTS)</text>

  <!-- 4 Role Badges -->
  <g transform="translate(50, 124)">
    <rect width="160" height="34" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
    <text x="12" y="21" font-size="12" font-weight="600" fill="#1d4ed8">👤 Citizen (Report/Track)</text>
  </g>
  <g transform="translate(225, 124)">
    <rect width="165" height="34" rx="6" fill="#f0fdf4" stroke="#bbf7d0"/>
    <text x="12" y="21" font-size="12" font-weight="600" fill="#15803d">🏢 Ward Admin (Dispatch)</text>
  </g>
  <g transform="translate(405, 124)">
    <rect width="175" height="34" rx="6" fill="#fefce8" stroke="#fef08a"/>
    <text x="12" y="21" font-size="12" font-weight="600" fill="#854d0e">🚛 Sanitation Worker (Clean)</text>
  </g>
  <g transform="translate(595, 124)">
    <rect width="180" height="34" rx="6" fill="#faf5ff" stroke="#e9d5ff"/>
    <text x="12" y="21" font-size="12" font-weight="600" fill="#7e22ce">🏛️ Central Superadmin (SLA)</text>
  </g>

  <!-- ======================================================== -->
  <!-- 2. CUSTOM VPC (LEFT CONTAINER)                           -->
  <!-- ======================================================== -->
  <rect x="30" y="185" width="760" height="610" rx="10" fill="#f8fafc" stroke="#2563eb" stroke-width="2"/>
  
  <!-- VPC Header Badge -->
  <rect x="45" y="198" width="410" height="26" rx="4" fill="#dbeafe"/>
  <text x="55" y="216" font-size="13" font-weight="700" fill="#1e40af">Amazon VPC (swachhnet-vpc) — CIDR: 10.0.0.0/16</text>

  <!-- Internet Gateway -->
  <rect x="290" y="238" width="240" height="36" rx="6" fill="#1d4ed8" filter="url(#cardShadow)"/>
  <text x="315" y="261" font-size="13" font-weight="700" fill="#ffffff">🌐 Internet Gateway (IGW)</text>

  <!-- -------------------------------------------------------- -->
  <!-- 2A. PUBLIC SUBNET                                        -->
  <!-- -------------------------------------------------------- -->
  <rect x="50" y="292" width="720" height="210" rx="8" fill="#ffffff" stroke="#60a5fa" stroke-width="1.5" filter="url(#cardShadow)"/>
  
  <text x="68" y="314" font-size="13" font-weight="700" fill="#1d4ed8">Public Subnet (10.0.1.0/24) — AZ: ap-south-1a</text>
  <text x="450" y="313" font-size="11" font-weight="600" fill="#059669">Security Group: swachhnet-app-sg (Ports 80, 443 Inbound)</text>

  <!-- EC2 Instance Box -->
  <rect x="68" y="328" width="684" height="160" rx="6" fill="#f0f9ff" stroke="#38bdf8" stroke-width="1.2"/>
  <text x="86" y="350" font-size="13" font-weight="700" fill="#0369a1">Amazon EC2 (t3.micro, Amazon Linux 2023) — Public IP: 65.2.180.175</text>
  <text x="560" y="349" font-size="11" font-weight="600" fill="#475569">Role: swachhnet-unified-role</text>

  <!-- Inner EC2 modules: Nginx & Express -->
  <!-- Module 1: Nginx -->
  <rect x="86" y="365" width="280" height="108" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <rect x="86" y="365" width="280" height="26" rx="6 6 0 0" fill="#16a34a"/>
  <text x="98" y="383" font-size="12" font-weight="700" fill="#ffffff">Nginx 1.30 Web Server (Port 80)</text>
  <text x="98" y="408" font-size="11" fill="#334155">• Serves React 18 SPA static files (/dist)</text>
  <text x="98" y="428" font-size="11" fill="#334155">• Reverse Proxy: /api/* → localhost:5000</text>
  <text x="98" y="448" font-size="11" fill="#334155">• Health Probe: /health → localhost:5000</text>
  <text x="98" y="465" font-size="10" font-weight="600" fill="#16a34a">✓ Fully eliminates CORS issues</text>

  <!-- Module 2: Node Express + PM2 -->
  <rect x="382" y="365" width="370" height="108" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <rect x="382" y="365" width="370" height="26" rx="6 6 0 0" fill="#0284c7"/>
  <text x="394" y="383" font-size="12" font-weight="700" fill="#ffffff">Node.js Express Backend API (Port 5000 / PM2)</text>
  <text x="394" y="408" font-size="11" fill="#334155">• Controllers: Auth, Complaint, Ward Authority, Central SLA</text>
  <text x="394" y="428" font-size="11" fill="#334155">• JWT Authentication (12-salt Bcrypt) &amp; RBAC Middleware</text>
  <text x="394" y="448" font-size="11" fill="#334155">• Geospatial Haversine SQL: Nearest Ward &amp; Nearest Truck</text>
  <text x="394" y="465" font-size="10" font-weight="600" fill="#0284c7">✓ Process Managed by PM2 with Systemd auto-reboot</text>

  <!-- -------------------------------------------------------- -->
  <!-- 2B. PRIVATE DB SUBNET GROUP (ISOLATED)                   -->
  <!-- -------------------------------------------------------- -->
  <rect x="50" y="520" width="720" height="260" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="1.5" filter="url(#cardShadow)"/>
  
  <text x="68" y="542" font-size="13" font-weight="700" fill="#c2410c">Private DB Subnet Group (Isolated — No Internet Route / 0.0.0.0/0 Blocked)</text>
  <text x="68" y="560" font-size="11" font-weight="600" fill="#b91c1c">Security Group: swachhnet-db-sg — Inbound: TCP 5432 exclusively from swachhnet-app-sg</text>

  <!-- Active RDS Database Box in Subnet 1 -->
  <rect x="68" y="574" width="410" height="190" rx="6" fill="#ffffff" stroke="#ea580c" stroke-width="1.5"/>
  <rect x="68" y="574" width="410" height="28" rx="6 6 0 0" fill="#ea580c"/>
  <text x="82" y="593" font-size="12" font-weight="700" fill="#ffffff">Primary DB: Amazon RDS for PostgreSQL 16.10</text>
  <text x="82" y="618" font-size="11" font-weight="600" fill="#7c2d12">Subnet 1: 10.0.10.0/24 (ap-south-1a) | Class: db.t3.micro</text>
  <text x="82" y="636" font-size="11" fill="#431407">Endpoint: swachhnet-postgres.cdc8mesu8z3p.ap-south-1.rds...</text>
  <text x="82" y="654" font-size="11" fill="#431407">Storage: 20 GB gp2 Encrypted (StorageEncrypted: true)</text>
  <text x="82" y="672" font-size="11" fill="#431407">Publicly Accessible: No | Direct Internet Probing Blocked</text>
  
  <line x1="82" y1="684" x2="460" y2="684" stroke="#fed7aa" stroke-width="1"/>
  <text x="82" y="702" font-size="10" font-weight="700" fill="#15803d">Relational Schema (5 Tables with UUID PKs &amp; Foreign Keys):</text>
  <text x="82" y="720" font-size="10" fill="#334155">1. users | 2. ward_authorities (8 BMC wards seeded)</text>
  <text x="82" y="736" font-size="10" fill="#334155">3. workers (32 trucks) | 4. complaints | 5. complaint_transfers</text>
  <text x="82" y="752" font-size="10" font-weight="600" fill="#c2410c">✓ Pure SQL Haversine spherical distance queries</text>

  <!-- Subnet 2 Standby (Multi-AZ requirement compliance) -->
  <rect x="495" y="574" width="257" height="190" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-dasharray="4,3"/>
  <text x="510" y="600" font-size="12" font-weight="700" fill="#475569">Subnet 2: 10.0.11.0/24</text>
  <text x="510" y="618" font-size="11" fill="#64748b">AZ: ap-south-1b (Standby)</text>
  <text x="510" y="646" font-size="11" fill="#475569">• Satisfies AWS RDS DB Subnet</text>
  <text x="520" y="662" font-size="11" fill="#475569">Group multi-AZ requirement</text>
  <text x="510" y="688" font-size="11" fill="#475569">• Single-AZ active mode keeps</text>
  <text x="520" y="704" font-size="11" fill="#475569">costs at $0.00 (Free Tier)</text>
  <text x="510" y="735" font-size="10" font-weight="600" fill="#16a34a">✓ Ready for Multi-AZ failover</text>

  <!-- ======================================================== -->
  <!-- 3. MANAGED AWS SERVICES & EXTERNAL AI (RIGHT COLUMN)     -->
  <!-- ======================================================== -->
  <rect x="815" y="92" width="355" height="703" rx="10" fill="#ffffff" stroke="#94a3b8" stroke-width="1.5" filter="url(#cardShadow)"/>
  <rect x="815" y="92" width="355" height="38" rx="10 10 0 0" fill="#1e293b"/>
  <text x="835" y="117" font-size="13" font-weight="700" fill="#ffffff" letter-spacing="0.5">AWS MANAGED SERVICES &amp; AI</text>

  <!-- 3A. Amazon S3 -->
  <g transform="translate(830, 142)">
    <rect width="325" height="96" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1.2"/>
    <text x="14" y="22" font-size="12" font-weight="700" fill="#15803d">🪣 Amazon S3 (Private Evidence Storage)</text>
    <text x="14" y="42" font-size="11" font-weight="600" fill="#334155">Bucket: swachhnet-evidence-078601217335-ap-south-1</text>
    <text x="14" y="60" font-size="10.5" fill="#475569">• Block Public Access: 100% Enabled (No public bucket)</text>
    <text x="14" y="76" font-size="10.5" fill="#475569">• Encryption: AES-256 Server-Side (SSE-S3)</text>
    <text x="14" y="90" font-size="10" font-weight="600" fill="#15803d">✓ Access via temporary 60-min Presigned GET URLs</text>
  </g>

  <!-- 3B. Amazon SQS + DLQ -->
  <g transform="translate(830, 250)">
    <rect width="325" height="96" rx="6" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.2"/>
    <text x="14" y="22" font-size="12" font-weight="700" fill="#7e22ce">📬 Amazon SQS (Decoupled Message Queue)</text>
    <text x="14" y="42" font-size="11" font-weight="600" fill="#334155">Queue: swachhnet-jobs-queue (Visibility: 60s)</text>
    <text x="14" y="60" font-size="10.5" fill="#475569">• Buffers background municipal events &amp; notifications</text>
    <text x="14" y="76" font-size="10.5" fill="#475569">• Dead Letter Queue (DLQ): swachhnet-jobs-dlq</text>
    <text x="14" y="90" font-size="10" font-weight="600" fill="#7e22ce">✓ maxReceiveCount: 5 (Isolates poison-pill messages)</text>
  </g>

  <!-- 3C. AWS SSM Parameter Store -->
  <g transform="translate(830, 358)">
    <rect width="325" height="96" rx="6" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.2"/>
    <text x="14" y="22" font-size="12" font-weight="700" fill="#b91c1c">🔐 AWS SSM Parameter Store (Secrets)</text>
    <text x="14" y="42" font-size="11" font-weight="600" fill="#334155">Path Namespace: /swachhnet/prod/*</text>
    <text x="14" y="60" font-size="10.5" fill="#475569">• SecureString (KMS encrypted): DATABASE_URL, JWT, G_API</text>
    <text x="14" y="76" font-size="10.5" fill="#475569">• Loaded at startup via AWS SDK v3 into memory</text>
    <text x="14" y="90" font-size="10" font-weight="600" fill="#b91c1c">✓ Zero static secrets on EC2 disk or GitHub</text>
  </g>

  <!-- 3D. CloudWatch & AWS Budgets -->
  <g transform="translate(830, 466)">
    <rect width="325" height="96" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.2"/>
    <text x="14" y="22" font-size="12" font-weight="700" fill="#1d4ed8">📊 Amazon CloudWatch &amp; AWS Budgets</text>
    <text x="14" y="42" font-size="11" font-weight="600" fill="#334155">Log Group: /swachhnet/backend (Stream: instance-28799)</text>
    <text x="14" y="60" font-size="10.5" fill="#475569">• Structured JSON logs with automated PII token sanitization</text>
    <text x="14" y="76" font-size="10.5" fill="#475569">• Alarm: swachhnet-ec2-high-cpu-alarm (CPU &gt;= 80%)</text>
    <text x="14" y="90" font-size="10" font-weight="600" fill="#1d4ed8">✓ AWS Budget: $10.00/month (Alert at 80% / $8.00)</text>
  </g>

  <!-- 3E. Google Gemini Vision AI -->
  <g transform="translate(830, 574)">
    <rect width="325" height="96" rx="6" fill="#fdf4ff" stroke="#f0abfc" stroke-width="1.2"/>
    <text x="14" y="22" font-size="12" font-weight="700" fill="#a21caf">🤖 Google Gemini 1.5 Flash AI (Multimodal)</text>
    <text x="14" y="42" font-size="11" font-weight="600" fill="#334155">1. Pre-validation: Flags non-garbage/spam photos</text>
    <text x="14" y="60" font-size="10.5" fill="#475569">• Rejects selfies/fake reports before saving to DB</text>
    <text x="14" y="76" font-size="10.5" fill="#475569">2. Differential Verification: Before vs After cleanup</text>
    <text x="14" y="90" font-size="10" font-weight="600" fill="#a21caf">✓ Confirms site is genuinely clean before resolving</text>
  </g>

  <!-- 3F. AWS CloudFormation Badge -->
  <g transform="translate(830, 682)">
    <rect width="325" height="96" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="14" y="22" font-size="12" font-weight="700" fill="#0f172a">⚡ AWS CloudFormation (Single-Click IaC)</text>
    <text x="14" y="42" font-size="11" font-weight="600" fill="#334155">Stack Name: swachhnet-prod-stack (CREATE_COMPLETE)</text>
    <text x="14" y="60" font-size="10.5" fill="#475569">• Declarative template: swachhnet-all-in-one.yaml</text>
    <text x="14" y="76" font-size="10.5" fill="#475569">• Deterministically provisions all 24 AWS resources</text>
    <text x="14" y="90" font-size="10" font-weight="600" fill="#0f172a">✓ Outputs: RDSEndpoint, PublicIp, Bucket, Queue</text>
  </g>

  <!-- ======================================================== -->
  <!-- 4. CLEAN, DIRECT ARROW ROUTING (NO WEIRD OVERLAPS)       -->
  <!-- ======================================================== -->

  <!-- Flow 1: Clients to IGW -->
  <path d="M 410 168 L 410 238" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <rect x="360" y="188" width="100" height="18" rx="3" fill="#ffffff" stroke="#93c5fd"/>
  <text x="366" y="201" font-size="9.5" font-weight="700" fill="#1e40af">HTTP/S (80/443)</text>

  <!-- Flow 2: IGW to EC2 Nginx -->
  <path d="M 410 274 L 410 328" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-blue)"/>

  <!-- Flow 3: EC2 Node API to RDS PostgreSQL (Internal TCP 5432) -->
  <!-- Clean straight path down on the left-center -->
  <path d="M 270 473 L 270 574" fill="none" stroke="#ea580c" stroke-width="2.5" marker-end="url(#arrow-orange)"/>
  <rect x="185" y="498" width="170" height="20" rx="4" fill="#ffffff" stroke="#fdba74"/>
  <text x="193" y="512" font-size="10" font-weight="700" fill="#c2410c">TCP:5432 (SSL / App-SG Only)</text>

  <!-- Flow 4: EC2 to Amazon S3 (Direct horizontal connector) -->
  <path d="M 752 385 L 830 190" fill="none" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arrow-green)"/>
  
  <!-- Flow 5: EC2 to SQS -->
  <path d="M 752 405 L 830 298" fill="none" stroke="#7c3aed" stroke-width="1.8" marker-end="url(#arrow-purple)"/>

  <!-- Flow 6: EC2 to SSM Parameter Store -->
  <path d="M 752 425 L 830 406" fill="none" stroke="#b91c1c" stroke-width="1.8" marker-end="url(#arrow-slate)"/>

  <!-- Flow 7: EC2 to CloudWatch -->
  <path d="M 752 445 L 830 514" fill="none" stroke="#1d4ed8" stroke-width="1.8" marker-end="url(#arrow-blue)"/>

  <!-- Flow 8: EC2 to Google Gemini AI -->
  <path d="M 752 465 L 830 622" fill="none" stroke="#a21caf" stroke-width="1.8" marker-end="url(#arrow-purple)"/>

</svg>
"""

# Save unified SVG
svg_path = os.path.join(ARCH_DIR, "Figure_4_1_Overall_Architecture.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_unified.strip())

# Render to high-res PNG (200 DPI -> 2400 x 1640)
doc = pymupdf.open("svg", svg_unified.encode("utf-8"))
pix = doc[0].get_pixmap(dpi=200)
png_path = os.path.join(ARCH_DIR, "Figure_4_1_Overall_Architecture.png")
pix.save(png_path)
print(f"Generated clean unified Figure 4.1: {pix.width}x{pix.height} at {png_path}")
