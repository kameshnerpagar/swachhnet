import os
import pymupdf

BASE_DIR = r"C:\Users\kames\Documents\Kamesh\Kamesh Agnel\SEM 5\CLOUD\Mini Project\smart-garbage"
ARCH_DIR = os.path.join(BASE_DIR, "docs", "CCL_Project_Report", "architecture")
os.makedirs(ARCH_DIR, exist_ok=True)

def save_and_render(name, svg_content, mmd_content):
    svg_path = os.path.join(ARCH_DIR, f"{name}.svg")
    png_path = os.path.join(ARCH_DIR, f"{name}.png")
    mmd_path = os.path.join(ARCH_DIR, f"{name}.mmd")
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
        
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mmd_content.strip())
        
    doc = pymupdf.open("svg", svg_content.encode("utf-8"))
    pix = doc[0].get_pixmap(dpi=200)
    pix.save(png_path)
    print(f"Generated {name} (PNG: {pix.width}x{pix.height})")

# -------------------------------------------------------------
# 1. Overall AWS Architecture
# -------------------------------------------------------------
svg_01 = """<svg width="1100" height="750" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.1"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c"/>
    </marker>
  </defs>

  <rect width="1100" height="750" fill="url(#bgGrad)" rx="12"/>
  <rect x="25" y="15" width="1050" height="50" rx="8" fill="#1e293b"/>
  <text x="40" y="46" fill="#ffffff" font-size="20" font-weight="bold">Figure 4.1: SwachhNet - Comprehensive AWS Cloud Architecture</text>
  <text x="820" y="46" fill="#94a3b8" font-size="13">Region: ap-south-1 (Mumbai)</text>

  <rect x="40" y="80" width="1020" height="70" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="60" y="105" font-size="14" font-weight="bold" fill="#0f172a">Client Layer (Web Browsers / Mobile Clients)</text>
  
  <g transform="translate(60, 115)">
    <rect width="180" height="26" rx="4" fill="#eff6ff" stroke="#93c5fd"/>
    <text x="15" y="18" font-size="12" fill="#1e40af">Citizen (Report &amp; Track)</text>
  </g>
  <g transform="translate(260, 115)">
    <rect width="190" height="26" rx="4" fill="#f0fdf4" stroke="#86efac"/>
    <text x="15" y="18" font-size="12" fill="#166534">Ward Admin (Dispatch &amp; SLA)</text>
  </g>
  <g transform="translate(470, 115)">
    <rect width="200" height="26" rx="4" fill="#fefce8" stroke="#fde047"/>
    <text x="15" y="18" font-size="12" fill="#854d0e">Sanitation Worker (Cleanup)</text>
  </g>
  <g transform="translate(690, 115)">
    <rect width="210" height="26" rx="4" fill="#faf5ff" stroke="#d8b4fe"/>
    <text x="15" y="18" font-size="12" fill="#6b21a8">Central Superadmin (City Metrics)</text>
  </g>

  <rect x="40" y="170" width="700" height="550" rx="10" fill="#f8fafc" stroke="#2563eb" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="60" y="195" font-size="15" font-weight="bold" fill="#1e40af">Amazon VPC (swachhnet-vpc) - CIDR: 10.0.0.0/16</text>

  <rect x="300" y="210" width="180" height="35" rx="6" fill="#2563eb" filter="url(#shadow)"/>
  <text x="325" y="233" font-size="13" font-weight="bold" fill="#ffffff">Internet Gateway (IGW)</text>

  <rect x="60" y="265" width="660" height="195" rx="8" fill="#eff6ff" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="80" y="290" font-size="13" font-weight="bold" fill="#1d4ed8">Public Subnet (10.0.1.0/24) - AZ: ap-south-1a [swachhnet-public-subnet-1]</text>
  <text x="80" y="307" font-size="11" fill="#64748b">Route: 0.0.0.0/0 → Internet Gateway | Security Group: swachhnet-app-sg (Inbound: 80, 443)</text>

  <rect x="80" y="320" width="620" height="125" rx="6" fill="#ffffff" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="100" y="342" font-size="14" font-weight="bold" fill="#0f172a">Amazon EC2 (t3.micro - Amazon Linux 2023) - Elastic IP: 65.2.180.175</text>
  <text x="100" y="358" font-size="11" fill="#475569">IAM Profile: swachhnet-unified-profile | Auto-restart via PM2 &amp; Systemd</text>

  <g transform="translate(100, 370)">
    <rect width="180" height="60" rx="4" fill="#f0fdf4" stroke="#4ade80"/>
    <text x="15" y="22" font-size="12" font-weight="bold" fill="#15803d">Nginx 1.30 (Port 80/443)</text>
    <text x="15" y="38" font-size="10" fill="#334155">Static Web Serving (React 18)</text>
    <text x="15" y="50" font-size="10" fill="#334155">Reverse Proxy (/api/ → :5000)</text>
  </g>
  <g transform="translate(300, 370)">
    <rect width="210" height="60" rx="4" fill="#f8fafc" stroke="#94a3b8"/>
    <text x="15" y="22" font-size="12" font-weight="bold" fill="#0f172a">Node.js Express API (Port 5000)</text>
    <text x="15" y="38" font-size="10" fill="#334155">JWT Auth &amp; Role-based Middleware</text>
    <text x="15" y="50" font-size="10" fill="#334155">Controllers: Auth, Complaint, Admin</text>
  </g>
  <g transform="translate(530, 370)">
    <rect width="150" height="60" rx="4" fill="#fef3c7" stroke="#f59e0b"/>
    <text x="10" y="22" font-size="12" font-weight="bold" fill="#b45309">Haversine SQL</text>
    <text x="10" y="38" font-size="10" fill="#334155">Nearest Ward Search</text>
    <text x="10" y="50" font-size="10" fill="#334155">Nearest Truck Dispatch</text>
  </g>

  <rect x="60" y="480" width="660" height="225" rx="8" fill="#fff7ed" stroke="#fb923c" stroke-width="1.5"/>
  <text x="80" y="505" font-size="13" font-weight="bold" fill="#c2410c">Private DB Subnet Group (No Public Route, Isolated VPC Subnets)</text>
  <text x="80" y="522" font-size="11" fill="#78716c">Security Group: swachhnet-db-sg | Strictly allows Port 5432 Inbound from swachhnet-app-sg ONLY</text>

  <rect x="80" y="535" width="310" height="155" rx="6" fill="#ffffff" stroke="#f97316" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="95" y="557" font-size="13" font-weight="bold" fill="#9a3412">Private Subnet 1 (10.0.10.0/24) [ap-south-1a]</text>
  <rect x="95" y="570" width="280" height="105" rx="4" fill="#ffedd5" stroke="#fdba74"/>
  <text x="110" y="592" font-size="13" font-weight="bold" fill="#7c2d12">Amazon RDS for PostgreSQL 16.10</text>
  <text x="110" y="610" font-size="11" fill="#431407">Endpoint: swachhnet-postgres.cdc8mesu8z3p...</text>
  <text x="110" y="626" font-size="11" fill="#431407">Instance: db.t3.micro (20GB gp2 Encrypted)</text>
  <text x="110" y="642" font-size="11" fill="#431407">Multi-AZ: False | Publicly Accessible: No</text>
  <text x="110" y="658" font-size="10" fill="#15803d">Tables: users, complaints, workers, wards</text>

  <rect x="410" y="535" width="290" height="155" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="425" y="557" font-size="13" font-weight="bold" fill="#475569">Private Subnet 2 (10.0.11.0/24) [ap-south-1b]</text>
  <rect x="425" y="570" width="260" height="105" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
  <text x="440" y="605" font-size="12" fill="#64748b">Required by RDS DB Subnet Group</text>
  <text x="440" y="625" font-size="11" fill="#94a3b8">Multi-AZ failover target standby zone</text>
  <text x="440" y="645" font-size="11" fill="#94a3b8">(Cost-optimized single-instance mode)</text>

  <rect x="760" y="170" width="300" height="550" rx="10" fill="#f8fafc" stroke="#64748b" stroke-width="1.5"/>
  <text x="780" y="195" font-size="15" font-weight="bold" fill="#0f172a">Managed Cloud Services &amp; AI</text>

  <rect x="780" y="215" width="260" height="85" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="795" y="238" font-size="13" font-weight="bold" fill="#15803d">Amazon S3 (Private Bucket)</text>
  <text x="795" y="255" font-size="11" fill="#334155">swachhnet-evidence-078601217335-ap-south-1</text>
  <text x="795" y="270" font-size="11" fill="#334155">AES-256 Server-Side Encryption (SSE-S3)</text>
  <text x="795" y="285" font-size="11" fill="#166534">Presigned URLs (60-minute TTL expiry)</text>

  <rect x="780" y="315" width="260" height="85" rx="6" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="795" y="338" font-size="13" font-weight="bold" fill="#6b21a8">Amazon SQS (Decoupled Queue)</text>
  <text x="795" y="355" font-size="11" fill="#334155">swachhnet-jobs-queue (Async job buffer)</text>
  <text x="795" y="370" font-size="11" fill="#334155">swachhnet-jobs-dlq (Dead Letter Queue)</text>
  <text x="795" y="385" font-size="11" fill="#7e22ce">Long-polling consumer with 5-retry limit</text>

  <rect x="780" y="415" width="260" height="75" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="795" y="438" font-size="13" font-weight="bold" fill="#b91c1c">AWS SSM Parameter Store</text>
  <text x="795" y="455" font-size="11" fill="#334155">Path: /swachhnet/prod/*</text>
  <text x="795" y="470" font-size="11" fill="#334155">SecureString for DB URI, JWT, Gemini API</text>

  <rect x="780" y="505" width="260" height="95" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="795" y="528" font-size="13" font-weight="bold" fill="#1d4ed8">CloudWatch &amp; AWS Budgets</text>
  <text x="795" y="545" font-size="11" fill="#334155">Log Group: /swachhnet/backend</text>
  <text x="795" y="560" font-size="11" fill="#334155">Alarm: swachhnet-ec2-high-cpu-alarm</text>
  <text x="795" y="575" font-size="11" fill="#1e40af">AWS Budget: $10.00 / month limit</text>

  <rect x="780" y="615" width="260" height="85" rx="6" fill="#fdf4ff" stroke="#d946ef" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="795" y="638" font-size="13" font-weight="bold" fill="#a21caf">Google Gemini Flash AI (External)</text>
  <text x="795" y="655" font-size="11" fill="#334155">1. Garbage validation &amp; spam rejection</text>
  <text x="795" y="670" font-size="11" fill="#334155">2. Before / After cleanup photo verification</text>
  <text x="795" y="685" font-size="11" fill="#86198f">Multimodal vision prompt analysis</text>

  <path d="M 390 150 L 390 205" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 390 245 L 390 315" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 230 445 L 230 565" fill="none" stroke="#ea580c" stroke-width="2.5" marker-end="url(#arrow-orange)"/>
  <text x="238" y="495" font-size="11" font-weight="bold" fill="#ea580c">TCP:5432 (SSL)</text>

  <path d="M 700 340 L 775 255" fill="none" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arrow-green)"/>
  <path d="M 700 370 L 775 355" fill="none" stroke="#7e22ce" stroke-width="1.8"/>
  <path d="M 700 410 L 775 440" fill="none" stroke="#dc2626" stroke-width="1.8"/>
  <path d="M 700 430 L 775 530" fill="none" stroke="#2563eb" stroke-width="1.8"/>
  <path d="M 700 440 L 775 640" fill="none" stroke="#c026d3" stroke-width="1.8"/>
</svg>"""

mmd_01 = """graph TD
    subgraph Clients["Clients"]
        Citizen["Citizen Web Client"]
        Admin["Ward Admin Portal"]
        Worker["Sanitation Worker View"]
        Super["Central Superadmin"]
    end

    subgraph VPC["Amazon VPC (10.0.0.0/16) - ap-south-1"]
        IGW["Internet Gateway"]
        
        subgraph PublicSubnet["Public Subnet (10.0.1.0/24)"]
            EC2["Amazon EC2 (t3.micro - 65.2.180.175)<br/>Nginx + Express API"]
        end
        
        subgraph PrivateSubnet["Private DB Subnets (10.0.10.0/24, 10.0.11.0/24)"]
            RDS["Amazon RDS PostgreSQL 16.10<br/>Port 5432 Isolated"]
        end
    end

    subgraph AWS_Managed["AWS Managed Services"]
        S3["Amazon S3 Evidence Bucket<br/>(Private, AES-256)"]
        SQS["Amazon SQS Queue + DLQ"]
        SSM["AWS SSM Parameter Store"]
        CW["Amazon CloudWatch Logs & Alarms"]
        Budget["AWS Budgets ($10 Limit)"]
    end

    subgraph External["External AI"]
        Gemini["Google Gemini Flash AI"]
    end

    Clients -->|HTTP/HTTPS 80/443| IGW
    IGW --> EC2
    EC2 -->|TCP 5432 Private| RDS
    EC2 -->|SDK Presigned URLs| S3
    EC2 -->|Async Jobs| SQS
    EC2 -->|Fetch Credentials| SSM
    EC2 -->|Stream Logs & Metrics| CW
    EC2 -->|Validate Garbage Photos| Gemini
"""
save_and_render("Figure_4_1_Overall_Architecture", svg_01, mmd_01)

# -------------------------------------------------------------
# 2. AWS VPC Network Architecture
# -------------------------------------------------------------
svg_02 = """<svg width="1000" height="650" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <defs>
    <filter id="shadow2" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.15"/>
    </filter>
    <marker id="arr2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e40af"/>
    </marker>
  </defs>

  <rect width="1000" height="650" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="950" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.2: Amazon VPC Network &amp; Security Group Isolation Architecture</text>

  <!-- VPC Outer Box -->
  <rect x="40" y="80" width="920" height="540" rx="10" fill="#eff6ff" stroke="#3b82f6" stroke-width="2.5"/>
  <text x="60" y="110" font-size="16" font-weight="bold" fill="#1e3a8a">Custom VPC: swachhnet-vpc (CIDR: 10.0.0.0/16)</text>

  <!-- Internet Gateway -->
  <rect x="380" y="125" width="240" height="40" rx="6" fill="#2563eb" filter="url(#shadow2)"/>
  <text x="415" y="150" fill="#ffffff" font-size="14" font-weight="bold">Internet Gateway (IGW)</text>

  <!-- Public Subnet Area -->
  <rect x="65" y="180" width="870" height="190" rx="8" fill="#ffffff" stroke="#60a5fa" stroke-width="1.8"/>
  <text x="85" y="205" font-size="14" font-weight="bold" fill="#1d4ed8">Public Subnet: swachhnet-public-subnet-1 (10.0.1.0/24) - Availability Zone: ap-south-1a</text>
  <text x="85" y="223" font-size="12" fill="#475569">Associated Route Table: swachhnet-public-rt | Route Entry: 0.0.0.0/0 → swachhnet-igw</text>

  <!-- Security Group App -->
  <rect x="85" y="235" width="830" height="120" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="100" y="258" font-size="13" font-weight="bold" fill="#15803d">Security Group: swachhnet-app-sg</text>
  <text x="100" y="278" font-size="11" fill="#166534">Inbound Rules: TCP 80 (HTTP) from 0.0.0.0/0 | TCP 443 (HTTPS) from 0.0.0.0/0</text>
  <text x="100" y="294" font-size="11" fill="#166534">Outbound Rules: All Traffic (0.0.0.0/0) to internet for Gemini AI &amp; AWS APIs</text>
  <rect x="620" y="245" width="280" height="95" rx="4" fill="#ffffff" stroke="#86efac"/>
  <text x="635" y="270" font-size="12" font-weight="bold" fill="#0f172a">Amazon EC2 Web Server</text>
  <text x="635" y="290" font-size="11" fill="#334155">IP: 65.2.180.175 (Public) / 10.0.1.x</text>
  <text x="635" y="308" font-size="11" fill="#334155">Nginx (80) → Node Express (5000)</text>
  <text x="635" y="326" font-size="10" fill="#16a34a">Attached: swachhnet-unified-role</text>

  <!-- Private Subnet Area -->
  <rect x="65" y="390" width="870" height="215" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="1.8"/>
  <text x="85" y="415" font-size="14" font-weight="bold" fill="#c2410c">Private Subnets: DB Subnet Group (Isolated - NO Internet Route Table Association)</text>
  
  <rect x="85" y="425" width="410" height="165" rx="6" fill="#ffffff" stroke="#fdba74"/>
  <text x="100" y="445" font-size="12" font-weight="bold" fill="#9a3412">swachhnet-private-subnet-1 (10.0.10.0/24) [ap-south-1a]</text>
  <text x="100" y="462" font-size="11" fill="#78716c">Security Group: swachhnet-db-sg</text>
  <text x="100" y="478" font-size="10" fill="#dc2626">Inbound: TCP 5432 strictly from swachhnet-app-sg ONLY</text>
  <text x="100" y="492" font-size="10" fill="#dc2626">Public Access: NO (0.0.0.0/0 Inbound Rejected)</text>
  
  <rect x="100" y="505" width="380" height="70" rx="4" fill="#ffedd5" stroke="#ea580c"/>
  <text x="115" y="528" font-size="12" font-weight="bold" fill="#7c2d12">Amazon RDS PostgreSQL 16.10 Primary</text>
  <text x="115" y="546" font-size="11" fill="#431407">Endpoint: swachhnet-postgres.cdc8mesu8z3p...</text>
  <text x="115" y="562" font-size="10" fill="#15803d">Status: Available | Encrypted: AES-256 (gp2)</text>

  <rect x="515" y="425" width="400" height="165" rx="6" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="530" y="445" font-size="12" font-weight="bold" fill="#475569">swachhnet-private-subnet-2 (10.0.11.0/24) [ap-south-1b]</text>
  <text x="530" y="465" font-size="11" fill="#64748b">Route Table: swachhnet-private-rt (Local 10.0.0.0/16 only)</text>
  <text x="530" y="510" font-size="12" fill="#94a3b8">Secondary AZ reservation for AWS RDS</text>
  <text x="530" y="530" font-size="11" fill="#94a3b8">DB Subnet Group compliance (Min 2 AZs)</text>
  <text x="530" y="550" font-size="11" fill="#94a3b8">Zero ongoing charges in Single-AZ mode</text>

  <!-- Connectors -->
  <path d="M 500 80 L 500 125" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr2)"/>
  <path d="M 500 165 L 500 235" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arr2)"/>
  <path d="M 700 340 L 700 380 L 300 380 L 300 505" fill="none" stroke="#ea580c" stroke-width="2.5" marker-end="url(#arr2)"/>
  <text x="310" y="375" font-size="11" font-weight="bold" fill="#ea580c">PostgreSQL Wire Protocol (5432)</text>
</svg>"""

mmd_02 = """graph TD
    Internet((Public Internet)) -->|TCP 80/443| IGW[Internet Gateway]
    
    subgraph VPC [Custom VPC: swachhnet-vpc 10.0.0.0/16]
        IGW -->|Route: 0.0.0.0/0| PublicSubnet
        
        subgraph PublicSubnet [Public Subnet: 10.0.1.0/24 - ap-south-1a]
            subgraph AppSG [Security Group: swachhnet-app-sg]
                EC2[EC2 Instance: 65.2.180.175<br/>Nginx + Node API]
            end
        end
        
        subgraph PrivateSubnets [Private DB Subnets: No Internet Route]
            subgraph Subnet1 [Private Subnet 1: 10.0.10.0/24 - ap-south-1a]
                subgraph DBSG [Security Group: swachhnet-db-sg]
                    RDS[Amazon RDS PostgreSQL<br/>Port 5432 Encrypted]
                end
            end
            
            subgraph Subnet2 [Private Subnet 2: 10.0.11.0/24 - ap-south-1b]
                Standby[RDS Standby Subnet<br/>Multi-AZ Compliance]
            end
        end
    end
    
    EC2 -->|TCP 5432 Inbound Allowed| DBSG
"""
save_and_render("Figure_4_2_VPC_Network", svg_02, mmd_02)

# -------------------------------------------------------------
# 3. Application Layer Architecture
# -------------------------------------------------------------
svg_03 = """<svg width="900" height="600" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <rect width="900" height="600" fill="#f8fafc" rx="10"/>
  <rect x="20" y="15" width="860" height="45" rx="6" fill="#1e293b"/>
  <text x="35" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.3: SwachhNet Multi-Tier Layered Software Architecture</text>

  <!-- Layer 1: Presentation -->
  <rect x="40" y="80" width="820" height="100" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.8"/>
  <text x="60" y="105" font-size="14" font-weight="bold" fill="#1d4ed8">1. Presentation Layer (Client Tier - React 18 SPA)</text>
  <g transform="translate(60, 115)">
    <rect width="180" height="50" rx="4" fill="#ffffff" stroke="#93c5fd"/>
    <text x="15" y="22" font-size="12" font-weight="bold" fill="#0f172a">Citizen Portal</text>
    <text x="15" y="40" font-size="10" fill="#475569">Photo capture, GPS map</text>
  </g>
  <g transform="translate(260, 115)">
    <rect width="180" height="50" rx="4" fill="#ffffff" stroke="#93c5fd"/>
    <text x="15" y="22" font-size="12" font-weight="bold" fill="#0f172a">Ward Admin Portal</text>
    <text x="15" y="40" font-size="10" fill="#475569">Dispatch &amp; Transfer tools</text>
  </g>
  <g transform="translate(460, 115)">
    <rect width="180" height="50" rx="4" fill="#ffffff" stroke="#93c5fd"/>
    <text x="15" y="22" font-size="12" font-weight="bold" fill="#0f172a">Worker Portal</text>
    <text x="15" y="40" font-size="10" fill="#475569">Task view, cleanup proof</text>
  </g>
  <g transform="translate(660, 115)">
    <rect width="180" height="50" rx="4" fill="#ffffff" stroke="#93c5fd"/>
    <text x="15" y="22" font-size="12" font-weight="bold" fill="#0f172a">Central Superadmin</text>
    <text x="15" y="40" font-size="10" fill="#475569">SLA analytics, 48h breaches</text>
  </g>

  <!-- Layer 2: Web Server & Gateway -->
  <rect x="40" y="195" width="820" height="75" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.8"/>
  <text x="60" y="220" font-size="14" font-weight="bold" fill="#15803d">2. Web Server &amp; Gateway Layer (Nginx Reverse Proxy on EC2)</text>
  <text x="60" y="242" font-size="12" fill="#334155">Static Content: Serves bundled React SPA from /var/www/swachhnet/frontend/dist</text>
  <text x="60" y="258" font-size="12" fill="#334155">API Routing: Proxies /api/* requests to internal Node.js backend on http://127.0.0.1:5000</text>

  <!-- Layer 3: Application & Business Logic -->
  <rect x="40" y="285" width="820" height="150" rx="8" fill="#fff7ed" stroke="#f97316" stroke-width="1.8"/>
  <text x="60" y="310" font-size="14" font-weight="bold" fill="#c2410c">3. Application Business Logic Layer (Node.js &amp; Express.js / PM2)</text>
  
  <g transform="translate(60, 325)">
    <rect width="180" height="95" rx="4" fill="#ffffff" stroke="#fdba74"/>
    <text x="12" y="20" font-size="12" font-weight="bold" fill="#0f172a">Auth Controller</text>
    <text x="12" y="38" font-size="10" fill="#475569">• User Registration</text>
    <text x="12" y="52" font-size="10" fill="#475569">• Bcrypt Password Hash</text>
    <text x="12" y="66" font-size="10" fill="#475569">• JWT Generation &amp; Role</text>
    <text x="12" y="80" font-size="10" fill="#475569">• Dual-DB Fallback</text>
  </g>
  <g transform="translate(260, 325)">
    <rect width="180" height="95" rx="4" fill="#ffffff" stroke="#fdba74"/>
    <text x="12" y="20" font-size="12" font-weight="bold" fill="#0f172a">Complaint Controller</text>
    <text x="12" y="38" font-size="10" fill="#475569">• Multer Memory Upload</text>
    <text x="12" y="52" font-size="10" fill="#475569">• Gemini AI Spam Check</text>
    <text x="12" y="66" font-size="10" fill="#475569">• S3 Direct Buffer Put</text>
    <text x="12" y="80" font-size="10" fill="#475569">• SQS Async Enqueue</text>
  </g>
  <g transform="translate(460, 325)">
    <rect width="180" height="95" rx="4" fill="#ffffff" stroke="#fdba74"/>
    <text x="12" y="20" font-size="12" font-weight="bold" fill="#0f172a">Authority Controller</text>
    <text x="12" y="38" font-size="10" fill="#475569">• Haversine Nearest Ward</text>
    <text x="12" y="52" font-size="10" fill="#475569">• Nearest Idle Truck SQL</text>
    <text x="12" y="66" font-size="10" fill="#475569">• Ward Transfers</text>
    <text x="12" y="80" font-size="10" fill="#475569">• Status Transition</text>
  </g>
  <g transform="translate(660, 325)">
    <rect width="180" height="95" rx="4" fill="#ffffff" stroke="#fdba74"/>
    <text x="12" y="20" font-size="12" font-weight="bold" fill="#0f172a">Central &amp; SLA</text>
    <text x="12" y="38" font-size="10" fill="#475569">• City-wide Metrics</text>
    <text x="12" y="52" font-size="10" fill="#475569">• 48-Hour SLA Breach SQL</text>
    <text x="12" y="66" font-size="10" fill="#475569">• CloudWatch Structured Log</text>
    <text x="12" y="80" font-size="10" fill="#475569">• Leaderboard &amp; Badges</text>
  </g>

  <!-- Layer 4: Persistence & Cloud Services -->
  <rect x="40" y="450" width="820" height="125" rx="8" fill="#faf5ff" stroke="#a855f7" stroke-width="1.8"/>
  <text x="60" y="475" font-size="14" font-weight="bold" fill="#6b21a8">4. Persistence, Cloud Services &amp; AI Integration Layer</text>
  
  <g transform="translate(60, 485)">
    <rect width="180" height="75" rx="4" fill="#ffffff" stroke="#d8b4fe"/>
    <text x="12" y="20" font-size="12" font-weight="bold" fill="#0f172a">Amazon RDS</text>
    <text x="12" y="38" font-size="10" fill="#475569">PostgreSQL 16.10 Database</text>
    <text x="12" y="52" font-size="10" fill="#475569">Relational Schema &amp; FKs</text>
    <text x="12" y="66" font-size="10" fill="#475569">Encrypted 20GB Storage</text>
  </g>
  <g transform="translate(260, 485)">
    <rect width="180" height="75" rx="4" fill="#ffffff" stroke="#d8b4fe"/>
    <text x="12" y="20" font-size="12" font-weight="bold" fill="#0f172a">Amazon S3 Storage</text>
    <text x="12" y="38" font-size="10" fill="#475569">Private Evidence Bucket</text>
    <text x="12" y="52" font-size="10" fill="#475569">Presigned Download URLs</text>
    <text x="12" y="66" font-size="10" fill="#475569">Server-side AES-256</text>
  </g>
  <g transform="translate(460, 485)">
    <rect width="180" height="75" rx="4" fill="#ffffff" stroke="#d8b4fe"/>
    <text x="12" y="20" font-size="12" font-weight="bold" fill="#0f172a">Amazon SQS &amp; SSM</text>
    <text x="12" y="38" font-size="10" fill="#475569">Job Queue + DLQ Buffer</text>
    <text x="12" y="52" font-size="10" fill="#475569">SecureString Parameters</text>
    <text x="12" y="66" font-size="10" fill="#475569">Zero Hardcoded Secrets</text>
  </g>
  <g transform="translate(660, 485)">
    <rect width="180" height="75" rx="4" fill="#ffffff" stroke="#d8b4fe"/>
    <text x="12" y="20" font-size="12" font-weight="bold" fill="#0f172a">Gemini AI &amp; Logs</text>
    <text x="12" y="38" font-size="10" fill="#475569">Multimodal Vision Check</text>
    <text x="12" y="52" font-size="10" fill="#475569">Before/After Comparison</text>
    <text x="12" y="66" font-size="10" fill="#475569">CloudWatch Log Streams</text>
  </g>
</svg>"""

mmd_03 = """graph TD
    subgraph Layer1 [1. Presentation Layer - React 18 SPA]
        CitizenUI[Citizen Portal]
        AdminUI[Ward Admin Portal]
        WorkerUI[Sanitation Worker Portal]
        SuperUI[Central Superadmin Dashboard]
    end

    subgraph Layer2 [2. Web Gateway Layer - Nginx on EC2]
        NginxStatic[Static Files Server /var/www/swachhnet/frontend/dist]
        NginxProxy[Reverse Proxy /api/ to 127.0.0.1:5000]
    end

    subgraph Layer3 [3. Business Logic Layer - Node.js Express & PM2]
        AuthCtrl[Auth Controller & JWT Middleware]
        ComplaintCtrl[Complaint Controller & S3 Multer]
        AuthorityCtrl[Authority Controller & Haversine Dispatch]
        CentralCtrl[Central Metrics & SLA 48h Monitor]
    end

    subgraph Layer4 [4. Cloud Persistence & External AI Layer]
        RDS[(Amazon RDS PostgreSQL 16.10)]
        S3[(Amazon S3 Evidence Bucket)]
        SQS[Amazon SQS Jobs Queue & DLQ]
        SSM[AWS SSM Parameter Store]
        CW[Amazon CloudWatch Logs]
        Gemini[Google Gemini Flash AI]
    end

    CitizenUI & AdminUI & WorkerUI & SuperUI --> NginxStatic
    CitizenUI & AdminUI & WorkerUI & SuperUI --> NginxProxy
    NginxProxy --> AuthCtrl & ComplaintCtrl & AuthorityCtrl & CentralCtrl
    
    AuthCtrl --> RDS
    AuthCtrl --> SSM
    ComplaintCtrl --> S3
    ComplaintCtrl --> Gemini
    ComplaintCtrl --> SQS
    AuthorityCtrl --> RDS
    CentralCtrl --> RDS
    CentralCtrl --> CW
"""
save_and_render("Figure_4_3_App_Architecture", svg_03, mmd_03)

# -------------------------------------------------------------
# 4. Database ER Diagram
# -------------------------------------------------------------
svg_04 = """<svg width="1050" height="650" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <rect width="1050" height="650" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="1000" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.4: Relational PostgreSQL Database Entity-Relationship Diagram (ERD)</text>

  <!-- Table 1: users -->
  <g transform="translate(40, 80)">
    <rect width="260" height="230" rx="6" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
    <rect width="260" height="35" rx="6" fill="#2563eb"/>
    <text x="15" y="24" fill="#ffffff" font-size="14" font-weight="bold">users (Table)</text>
    <text x="15" y="55" font-size="11" font-weight="bold" fill="#b91c1c">PK  id : UUID (DEFAULT gen_random_uuid())</text>
    <text x="15" y="75" font-size="11" fill="#334155">    name : VARCHAR(255) NOT NULL</text>
    <text x="15" y="95" font-size="11" fill="#334155">    email : VARCHAR(255) UNIQUE NOT NULL</text>
    <text x="15" y="115" font-size="11" fill="#334155">    password : VARCHAR(255) (Bcrypt)</text>
    <text x="15" y="135" font-size="11" fill="#334155">    role : VARCHAR(32) CHECK IN</text>
    <text x="25" y="152" font-size="10" fill="#64748b">('user','admin','worker','superadmin')</text>
    <text x="15" y="172" font-size="11" fill="#334155">    created_at : TIMESTAMPTZ</text>
    <text x="15" y="192" font-size="11" fill="#334155">    updated_at : TIMESTAMPTZ</text>
    <text x="15" y="215" font-size="10" fill="#15803d">Indexes: idx_users_email, idx_users_role</text>
  </g>

  <!-- Table 2: ward_authorities -->
  <g transform="translate(40, 360)">
    <rect width="260" height="230" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2"/>
    <rect width="260" height="35" rx="6" fill="#059669"/>
    <text x="15" y="24" fill="#ffffff" font-size="14" font-weight="bold">ward_authorities (Table)</text>
    <text x="15" y="55" font-size="11" font-weight="bold" fill="#b91c1c">PK,FK user_id : UUID → users(id)</text>
    <text x="15" y="75" font-size="11" fill="#334155">    name : VARCHAR(255) NOT NULL</text>
    <text x="15" y="95" font-size="11" fill="#334155">    address : TEXT</text>
    <text x="15" y="115" font-size="11" fill="#334155">    latitude : DOUBLE PRECISION</text>
    <text x="15" y="135" font-size="11" fill="#334155">    longitude : DOUBLE PRECISION</text>
    <text x="15" y="155" font-size="11" fill="#334155">    rating_score : NUMERIC(3,2)</text>
    <text x="15" y="175" font-size="11" fill="#334155">    rating_count : INT DEFAULT 0</text>
    <text x="15" y="210" font-size="10" fill="#64748b">8 Official BMC Wards Seeded</text>
  </g>

  <!-- Table 3: complaints -->
  <g transform="translate(390, 80)">
    <rect width="320" height="420" rx="6" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
    <rect width="320" height="35" rx="6" fill="#ea580c"/>
    <text x="15" y="24" fill="#ffffff" font-size="14" font-weight="bold">complaints (Core Transaction Table)</text>
    <text x="15" y="55" font-size="11" font-weight="bold" fill="#b91c1c">PK  id : UUID (DEFAULT gen_random_uuid())</text>
    <text x="15" y="75" font-size="11" font-weight="bold" fill="#2563eb">FK  user_id : UUID → users(id)</text>
    <text x="15" y="95" font-size="11" fill="#334155">    user_name : VARCHAR(255)</text>
    <text x="15" y="115" font-size="11" font-weight="bold" fill="#2563eb">FK  authority_id : UUID → users(id)</text>
    <text x="15" y="135" font-size="11" font-weight="bold" fill="#2563eb">FK  worker_id : UUID (Nullable) → users(id)</text>
    <text x="15" y="155" font-size="11" fill="#334155">    s3_key : VARCHAR(512) NOT NULL</text>
    <text x="15" y="175" font-size="11" fill="#334155">    image_url : TEXT (Presigned)</text>
    <text x="15" y="195" font-size="11" fill="#334155">    after_s3_key : VARCHAR(512)</text>
    <text x="15" y="215" font-size="11" fill="#334155">    after_image_url : TEXT (Presigned)</text>
    <text x="15" y="235" font-size="11" fill="#334155">    latitude : DOUBLE PRECISION NOT NULL</text>
    <text x="15" y="255" font-size="11" fill="#334155">    longitude : DOUBLE PRECISION NOT NULL</text>
    <text x="15" y="275" font-size="11" fill="#334155">    address : TEXT</text>
    <text x="15" y="295" font-size="11" fill="#334155">    status : VARCHAR(32) CHECK IN</text>
    <text x="25" y="310" font-size="10" fill="#64748b">('open','assigned','pending_verification','resolved','rejected')</text>
    <text x="15" y="330" font-size="11" fill="#334155">    description : TEXT</text>
    <text x="15" y="350" font-size="11" fill="#334155">    rating : INT (1 to 5)</text>
    <text x="15" y="370" font-size="11" fill="#334155">    created_at : TIMESTAMPTZ DEFAULT NOW()</text>
    <text x="15" y="390" font-size="11" fill="#334155">    updated_at : TIMESTAMPTZ DEFAULT NOW()</text>
    <text x="15" y="410" font-size="10" fill="#15803d">Indexes: user, authority, worker, status, created_at</text>
  </g>

  <!-- Table 4: workers -->
  <g transform="translate(750, 80)">
    <rect width="260" height="220" rx="6" fill="#ffffff" stroke="#7c3aed" stroke-width="2"/>
    <rect width="260" height="35" rx="6" fill="#7c3aed"/>
    <text x="15" y="24" fill="#ffffff" font-size="14" font-weight="bold">workers (Truck Fleet Table)</text>
    <text x="15" y="55" font-size="11" font-weight="bold" fill="#b91c1c">PK,FK user_id : UUID → users(id)</text>
    <text x="15" y="75" font-size="11" fill="#334155">    truck_number : VARCHAR(64) NOT NULL</text>
    <text x="15" y="95" font-size="11" font-weight="bold" fill="#2563eb">FK  assigned_ward_id : UUID → users(id)</text>
    <text x="15" y="115" font-size="11" fill="#334155">    latitude : DOUBLE PRECISION</text>
    <text x="15" y="135" font-size="11" fill="#334155">    longitude : DOUBLE PRECISION</text>
    <text x="15" y="155" font-size="11" fill="#334155">    status : VARCHAR(32) ('idle','busy')</text>
    <text x="15" y="195" font-size="10" fill="#15803d">Index: idx_workers_ward_status</text>
    <text x="15" y="210" font-size="10" fill="#64748b">32 Trucks Seeded across Mumbai</text>
  </g>

  <!-- Table 5: complaint_transfers -->
  <g transform="translate(390, 520)">
    <rect width="320" height="110" rx="6" fill="#ffffff" stroke="#64748b" stroke-width="2"/>
    <rect width="320" height="30" rx="6" fill="#64748b"/>
    <text x="15" y="21" fill="#ffffff" font-size="13" font-weight="bold">complaint_transfers (Audit Log)</text>
    <text x="15" y="48" font-size="11" font-weight="bold" fill="#b91c1c">PK  id : BIGSERIAL</text>
    <text x="15" y="65" font-size="11" font-weight="bold" fill="#2563eb">FK  complaint_id : UUID → complaints(id)</text>
    <text x="15" y="82" font-size="11" fill="#334155">    from_authority_name / to_authority_name</text>
    <text x="15" y="98" font-size="11" fill="#334155">    timestamp : TIMESTAMPTZ DEFAULT NOW()</text>
  </g>

  <!-- Relationship Lines -->
  <line x1="300" y1="140" x2="390" y2="140" stroke="#2563eb" stroke-width="2"/>
  <circle cx="390" cy="140" r="4" fill="#2563eb"/>
  
  <line x1="170" y1="310" x2="170" y2="360" stroke="#059669" stroke-width="2"/>
  <circle cx="170" cy="360" r="4" fill="#059669"/>

  <line x1="710" y1="160" x2="750" y2="160" stroke="#7c3aed" stroke-width="2"/>
  <circle cx="710" cy="160" r="4" fill="#7c3aed"/>

  <line x1="550" y1="500" x2="550" y2="520" stroke="#64748b" stroke-width="2"/>
  <circle cx="550" cy="520" r="4" fill="#64748b"/>
</svg>"""

mmd_04 = """erDiagram
    users ||--o| ward_authorities : "has profile"
    users ||--o| workers : "has truck details"
    users ||--o{ complaints : "files"
    users ||--o{ complaints : "oversees as authority"
    users ||--o{ complaints : "assigned as worker"
    complaints ||--o{ complaint_transfers : "tracked in audit"

    users {
        UUID id PK
        VARCHAR name
        VARCHAR email UK
        VARCHAR password
        VARCHAR role
        TIMESTAMPTZ created_at
    }

    ward_authorities {
        UUID user_id PK,FK
        VARCHAR name
        TEXT address
        DOUBLE latitude
        DOUBLE longitude
        NUMERIC rating_score
    }

    workers {
        UUID user_id PK,FK
        VARCHAR truck_number
        UUID assigned_ward_id FK
        DOUBLE latitude
        DOUBLE longitude
        VARCHAR status
    }

    complaints {
        UUID id PK
        UUID user_id FK
        UUID authority_id FK
        UUID worker_id FK
        VARCHAR s3_key
        VARCHAR after_s3_key
        DOUBLE latitude
        DOUBLE longitude
        VARCHAR status
        INT rating
        TIMESTAMPTZ created_at
    }

    complaint_transfers {
        BIGSERIAL id PK
        UUID complaint_id FK
        VARCHAR from_authority_name
        VARCHAR to_authority_name
        TIMESTAMPTZ timestamp
    }
"""
save_and_render("Figure_4_4_Database_ERD", svg_04, mmd_04)

# -------------------------------------------------------------
# 5. Use Case Diagram
# -------------------------------------------------------------
svg_05 = """<svg width="950" height="650" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <rect width="950" height="650" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="900" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.5: UML Use Case Diagram for SwachhNet Municipal Roles</text>

  <!-- System Boundary -->
  <rect x="200" y="80" width="550" height="540" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
  <text x="380" y="105" font-size="16" font-weight="bold" fill="#0369a1">SwachhNet Municipal System</text>

  <!-- Left Actor: Citizen -->
  <g transform="translate(60, 160)">
    <circle cx="30" cy="20" r="15" fill="#3b82f6"/>
    <line x1="30" y1="35" x2="30" y2="70" stroke="#3b82f6" stroke-width="3"/>
    <line x1="10" y1="50" x2="50" y2="50" stroke="#3b82f6" stroke-width="3"/>
    <line x1="30" y1="70" x2="15" y2="100" stroke="#3b82f6" stroke-width="3"/>
    <line x1="30" y1="70" x2="45" y2="100" stroke="#3b82f6" stroke-width="3"/>
    <text x="10" y="125" font-size="13" font-weight="bold" fill="#1e40af">Citizen</text>
  </g>

  <!-- Left Actor: Sanitation Worker -->
  <g transform="translate(60, 420)">
    <circle cx="30" cy="20" r="15" fill="#eab308"/>
    <line x1="30" y1="35" x2="30" y2="70" stroke="#eab308" stroke-width="3"/>
    <line x1="10" y1="50" x2="50" y2="50" stroke="#eab308" stroke-width="3"/>
    <line x1="30" y1="70" x2="15" y2="100" stroke="#eab308" stroke-width="3"/>
    <line x1="30" y1="70" x2="45" y2="100" stroke="#eab308" stroke-width="3"/>
    <text x="-5" y="125" font-size="13" font-weight="bold" fill="#854d0e">Sanitation Worker</text>
  </g>

  <!-- Right Actor: Ward Admin -->
  <g transform="translate(820, 160)">
    <circle cx="30" cy="20" r="15" fill="#10b981"/>
    <line x1="30" y1="35" x2="30" y2="70" stroke="#10b981" stroke-width="3"/>
    <line x1="10" y1="50" x2="50" y2="50" stroke="#10b981" stroke-width="3"/>
    <line x1="30" y1="70" x2="15" y2="100" stroke="#10b981" stroke-width="3"/>
    <line x1="30" y1="70" x2="45" y2="100" stroke="#10b981" stroke-width="3"/>
    <text x="-5" y="125" font-size="13" font-weight="bold" fill="#065f46">Ward Admin</text>
  </g>

  <!-- Right Actor: Central Superadmin -->
  <g transform="translate(820, 420)">
    <circle cx="30" cy="20" r="15" fill="#8b5cf6"/>
    <line x1="30" y1="35" x2="30" y2="70" stroke="#8b5cf6" stroke-width="3"/>
    <line x1="10" y1="50" x2="50" y2="50" stroke="#8b5cf6" stroke-width="3"/>
    <line x1="30" y1="70" x2="15" y2="100" stroke="#8b5cf6" stroke-width="3"/>
    <line x1="30" y1="70" x2="45" y2="100" stroke="#8b5cf6" stroke-width="3"/>
    <text x="-15" y="125" font-size="13" font-weight="bold" fill="#5b21b6">Central Superadmin</text>
  </g>

  <!-- Use Cases (Ovals) -->
  <g transform="translate(240, 130)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#f0f9ff" stroke="#0284c7"/>
    <text x="35" y="27" font-size="12" fill="#0369a1">UC1: Register &amp; Login</text>
  </g>
  <g transform="translate(240, 185)">
    <ellipse cx="110" cy="22" rx="105" ry="20" fill="#f0f9ff" stroke="#0284c7"/>
    <text x="25" y="27" font-size="12" fill="#0369a1">UC2: Report Garbage (GPS &amp; S3)</text>
  </g>
  <g transform="translate(240, 240)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#f0f9ff" stroke="#0284c7"/>
    <text x="25" y="27" font-size="12" fill="#0369a1">UC3: View Complaint Status</text>
  </g>
  <g transform="translate(240, 295)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#f0f9ff" stroke="#0284c7"/>
    <text x="20" y="27" font-size="12" fill="#0369a1">UC4: Earn Badges &amp; Give Rating</text>
  </g>

  <g transform="translate(500, 130)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#ecfdf5" stroke="#10b981"/>
    <text x="30" y="27" font-size="12" fill="#047857">UC5: View Ward Complaints</text>
  </g>
  <g transform="translate(500, 185)">
    <ellipse cx="110" cy="22" rx="105" ry="20" fill="#ecfdf5" stroke="#10b981"/>
    <text x="15" y="27" font-size="12" fill="#047857">UC6: Dispatch Nearest Truck</text>
  </g>
  <g transform="translate(500, 240)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#ecfdf5" stroke="#10b981"/>
    <text x="25" y="27" font-size="12" fill="#047857">UC7: Transfer Ward Boundary</text>
  </g>

  <g transform="translate(240, 390)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#fefce8" stroke="#ca8a04"/>
    <text x="35" y="27" font-size="12" fill="#854d0e">UC8: View Assigned Jobs</text>
  </g>
  <g transform="translate(240, 445)">
    <ellipse cx="110" cy="22" rx="105" ry="20" fill="#fefce8" stroke="#ca8a04"/>
    <text x="20" y="27" font-size="12" fill="#854d0e">UC9: Upload Cleanup Proof (S3)</text>
  </g>
  <g transform="translate(240, 500)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#fefce8" stroke="#ca8a04"/>
    <text x="25" y="27" font-size="12" fill="#854d0e">UC10: Update Truck Availability</text>
  </g>

  <g transform="translate(500, 390)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#f5f3ff" stroke="#8b5cf6"/>
    <text x="25" y="27" font-size="12" fill="#6d28d9">UC11: Monitor 48h SLA Breaches</text>
  </g>
  <g transform="translate(500, 445)">
    <ellipse cx="110" cy="22" rx="105" ry="20" fill="#f5f3ff" stroke="#8b5cf6"/>
    <text x="15" y="27" font-size="12" fill="#6d28d9">UC12: City-Wide Ward Analytics</text>
  </g>
  <g transform="translate(500, 500)">
    <ellipse cx="110" cy="22" rx="100" ry="20" fill="#f5f3ff" stroke="#8b5cf6"/>
    <text x="30" y="27" font-size="12" fill="#6d28d9">UC13: View CloudWatch Audit</text>
  </g>

  <!-- Connectors -->
  <line x1="100" y1="210" x2="240" y2="152" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="100" y1="210" x2="240" y2="207" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="100" y1="210" x2="240" y2="262" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="100" y1="210" x2="240" y2="317" stroke="#94a3b8" stroke-width="1.2"/>

  <line x1="820" y1="210" x2="710" y2="152" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="820" y1="210" x2="710" y2="207" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="820" y1="210" x2="710" y2="262" stroke="#94a3b8" stroke-width="1.2"/>

  <line x1="100" y1="470" x2="240" y2="412" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="100" y1="470" x2="240" y2="467" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="100" y1="470" x2="240" y2="522" stroke="#94a3b8" stroke-width="1.2"/>

  <line x1="820" y1="470" x2="710" y2="412" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="820" y1="470" x2="710" y2="467" stroke="#94a3b8" stroke-width="1.2"/>
  <line x1="820" y1="470" x2="710" y2="522" stroke="#94a3b8" stroke-width="1.2"/>
</svg>"""

mmd_05 = """graph LR
    Citizen((Citizen))
    Worker((Sanitation Worker))
    Admin((Ward Admin))
    Super((Central Superadmin))

    subgraph System [SwachhNet Municipal System]
        UC1([UC1: Register & Login])
        UC2([UC2: Report Garbage Photo & GPS])
        UC3([UC3: Track Complaint Status])
        UC4([UC4: Give Feedback & Earn Points])

        UC5([UC5: View Ward Complaints])
        UC6([UC6: Dispatch Nearest Truck])
        UC7([UC7: Transfer Complaint Ward])

        UC8([UC8: View Assigned Jobs])
        UC9([UC9: Upload Cleanup Photo])
        UC10([UC10: Update Truck Availability])

        UC11([UC11: Monitor 48h SLA Breaches])
        UC12([UC12: View City-wide Analytics])
    end

    Citizen --> UC1
    Citizen --> UC2
    Citizen --> UC3
    Citizen --> UC4

    Admin --> UC5
    Admin --> UC6
    Admin --> UC7

    Worker --> UC8
    Worker --> UC9
    Worker --> UC10

    Super --> UC11
    Super --> UC12
"""
save_and_render("Figure_4_5_Use_Case", svg_05, mmd_05)

# -------------------------------------------------------------
# 6. DFD Level 0 (Context Diagram)
# -------------------------------------------------------------
svg_06 = """<svg width="900" height="550" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <defs>
    <marker id="dfdArr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
  </defs>

  <rect width="900" height="550" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="850" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.6: Level 0 Data Flow Diagram (Context Diagram)</text>

  <!-- Central Process -->
  <circle cx="450" cy="280" r="85" fill="#eff6ff" stroke="#2563eb" stroke-width="3"/>
  <text x="415" y="265" font-size="14" font-weight="bold" fill="#1e40af">0.0</text>
  <text x="390" y="285" font-size="14" font-weight="bold" fill="#1e40af">SwachhNet</text>
  <text x="392" y="303" font-size="12" fill="#3b82f6">Cloud Platform</text>

  <!-- Entity 1: Citizen (Top Left) -->
  <rect x="60" y="100" width="160" height="60" rx="6" fill="#ffffff" stroke="#334155" stroke-width="2"/>
  <text x="110" y="135" font-size="14" font-weight="bold" fill="#0f172a">Citizen</text>

  <!-- Entity 2: Ward Admin (Top Right) -->
  <rect x="680" y="100" width="160" height="60" rx="6" fill="#ffffff" stroke="#334155" stroke-width="2"/>
  <text x="715" y="135" font-size="14" font-weight="bold" fill="#0f172a">Ward Admin</text>

  <!-- Entity 3: Sanitation Worker (Bottom Left) -->
  <rect x="60" y="400" width="160" height="60" rx="6" fill="#ffffff" stroke="#334155" stroke-width="2"/>
  <text x="80" y="435" font-size="13" font-weight="bold" fill="#0f172a">Sanitation Worker</text>

  <!-- Entity 4: Central Superadmin (Bottom Right) -->
  <rect x="680" y="400" width="160" height="60" rx="6" fill="#ffffff" stroke="#334155" stroke-width="2"/>
  <text x="700" y="435" font-size="13" font-weight="bold" fill="#0f172a">Central Authority</text>

  <!-- Entity 5: AWS Services & Gemini AI (Bottom Center) -->
  <rect x="350" y="460" width="200" height="50" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="4,3"/>
  <text x="365" y="490" font-size="12" fill="#64748b">AWS (RDS, S3, SQS) &amp; Gemini AI</text>

  <!-- Flows -->
  <!-- Citizen to System -->
  <path d="M 220 120 L 375 235" fill="none" stroke="#2563eb" stroke-width="1.8" marker-end="url(#dfdArr)"/>
  <text x="180" y="180" font-size="11" fill="#1e40af">Garbage Report (Photo + GPS)</text>

  <path d="M 370 260 L 220 145" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#dfdArr)"/>
  <text x="230" y="215" font-size="11" fill="#475569">Status &amp; Points</text>

  <!-- System to Admin -->
  <path d="M 525 235 L 680 120" fill="none" stroke="#2563eb" stroke-width="1.8" marker-end="url(#dfdArr)"/>
  <text x="560" y="165" font-size="11" fill="#1e40af">Ward Complaints &amp; Breaches</text>

  <path d="M 680 145 L 530 260" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#dfdArr)"/>
  <text x="610" y="215" font-size="11" fill="#475569">Dispatch &amp; Transfer Orders</text>

  <!-- System to Worker -->
  <path d="M 375 325 L 220 410" fill="none" stroke="#2563eb" stroke-width="1.8" marker-end="url(#dfdArr)"/>
  <text x="170" y="360" font-size="11" fill="#1e40af">Assigned Task Location</text>

  <path d="M 220 435 L 375 345" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#dfdArr)"/>
  <text x="210" y="405" font-size="11" fill="#475569">Cleanup Proof &amp; Status</text>

  <!-- System to Central -->
  <path d="M 525 325 L 680 410" fill="none" stroke="#2563eb" stroke-width="1.8" marker-end="url(#dfdArr)"/>
  <text x="565" y="360" font-size="11" fill="#1e40af">SLA Breaches &amp; Ward KPIs</text>

  <!-- System to External Cloud -->
  <path d="M 450 365 L 450 460" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#dfdArr)"/>
</svg>"""

mmd_06 = """graph TD
    Citizen[Citizen] -->|Report: Photo + GPS| System((0.0 SwachhNet Cloud Platform))
    System -->|Status Updates & Badges| Citizen

    System -->|Assigned Ward Complaints| Admin[Ward Administrator]
    Admin -->|Truck Dispatch & Transfers| System

    System -->|Dispatch Task & Navigation| Worker[Sanitation Worker]
    Worker -->|Cleanup Proof & Status| System

    System -->|City-wide Analytics & 48h SLA| Superadmin[Central Authority]

    System <-->|Storage, DB & AI Verification| Cloud[AWS Cloud & Gemini AI]
"""
save_and_render("Figure_4_6_DFD_Level_0", svg_06, mmd_06)

# -------------------------------------------------------------
# 7. Citizen Complaint Lifecycle Workflow
# -------------------------------------------------------------
svg_07 = """<svg width="1050" height="600" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <defs>
    <marker id="flowArr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7"/>
    </marker>
  </defs>

  <rect width="1050" height="600" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="1000" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.8: End-to-End Citizen Complaint Resolution Workflow</text>

  <!-- Step 1 -->
  <g transform="translate(40, 90)">
    <rect width="160" height="90" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#1e40af">1. Citizen Submission</text>
    <text x="15" y="45" font-size="11" fill="#334155">• Capture Photo</text>
    <text x="15" y="60" font-size="11" fill="#334155">• Extract GPS Location</text>
    <text x="15" y="75" font-size="11" fill="#334155">• Enter Description</text>
  </g>

  <!-- Step 2 -->
  <g transform="translate(240, 90)">
    <polygon points="80,0 160,45 80,90 0,45" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
    <text x="45" y="42" font-size="11" font-weight="bold" fill="#991b1b">2. Gemini AI</text>
    <text x="42" y="58" font-size="10" fill="#991b1b">Is Garbage?</text>
  </g>

  <!-- Step 3 -->
  <g transform="translate(440, 90)">
    <rect width="170" height="90" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#15803d">3. Cloud Ingestion</text>
    <text x="15" y="45" font-size="11" fill="#334155">• S3 Private Upload</text>
    <text x="15" y="60" font-size="11" fill="#334155">• SQS Async Job Enqueue</text>
    <text x="15" y="75" font-size="11" fill="#334155">• CloudWatch Audit Log</text>
  </g>

  <!-- Step 4 -->
  <g transform="translate(650, 90)">
    <rect width="170" height="90" rx="6" fill="#fff7ed" stroke="#f97316" stroke-width="1.5"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#c2410c">4. Ward Assignment</text>
    <text x="15" y="45" font-size="11" fill="#334155">• Haversine SQL Math</text>
    <text x="15" y="60" font-size="11" fill="#334155">• Match Nearest BMC Ward</text>
    <text x="15" y="75" font-size="11" fill="#334155">• INSERT to RDS (Open)</text>
  </g>

  <!-- Step 5 -->
  <g transform="translate(860, 90)">
    <rect width="150" height="90" rx="6" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
    <text x="12" y="25" font-size="12" font-weight="bold" fill="#6b21a8">5. Truck Dispatch</text>
    <text x="12" y="45" font-size="11" fill="#334155">• Haversine Idle Fleet</text>
    <text x="12" y="60" font-size="11" fill="#334155">• Assign Worker</text>
    <text x="12" y="75" font-size="11" fill="#334155">• Status: 'assigned'</text>
  </g>

  <!-- Step 6 -->
  <g transform="translate(860, 320)">
    <rect width="150" height="90" rx="6" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>
    <text x="12" y="25" font-size="12" font-weight="bold" fill="#854d0e">6. Field Cleanup</text>
    <text x="12" y="45" font-size="11" fill="#334155">• Worker Navigates</text>
    <text x="12" y="60" font-size="11" fill="#334155">• Collects Waste</text>
    <text x="12" y="75" font-size="11" fill="#334155">• Uploads 'After' Proof</text>
  </g>

  <!-- Step 7 -->
  <g transform="translate(650, 320)">
    <polygon points="80,0 160,45 80,90 0,45" fill="#fdf4ff" stroke="#d946ef" stroke-width="1.5"/>
    <text x="35" y="42" font-size="11" font-weight="bold" fill="#86198f">7. Gemini AI</text>
    <text x="32" y="58" font-size="10" fill="#86198f">Verify Clean?</text>
  </g>

  <!-- Step 8 -->
  <g transform="translate(440, 320)">
    <rect width="170" height="90" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#15803d">8. Resolution &amp; Points</text>
    <text x="15" y="45" font-size="11" fill="#334155">• Status: 'resolved'</text>
    <text x="15" y="60" font-size="11" fill="#334155">• Citizen Earns 10 Pts</text>
    <text x="15" y="75" font-size="11" fill="#334155">• Worker status: 'idle'</text>
  </g>

  <!-- Step 9 -->
  <g transform="translate(240, 320)">
    <rect width="160" height="90" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#1e40af">9. Citizen Feedback</text>
    <text x="15" y="45" font-size="11" fill="#334155">• Star Rating (1-5)</text>
    <text x="15" y="60" font-size="11" fill="#334155">• Feedback Comments</text>
    <text x="15" y="75" font-size="11" fill="#334155">• Ward Score Updated</text>
  </g>

  <!-- Rejection Path -->
  <g transform="translate(240, 220)">
    <rect width="160" height="50" rx="4" fill="#fee2e2" stroke="#f87171"/>
    <text x="15" y="22" font-size="11" font-weight="bold" fill="#991b1b">Rejection Notice</text>
    <text x="15" y="38" font-size="10" fill="#7f1d1d">Non-garbage image detected</text>
  </g>

  <!-- Connectors -->
  <path d="M 200 135 L 240 135" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#flowArr)"/>
  <path d="M 400 135 L 440 135" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#flowArr)"/>
  <text x="408" y="125" font-size="10" font-weight="bold" fill="#15803d">Yes</text>

  <path d="M 320 180 L 320 220" fill="none" stroke="#dc2626" stroke-width="1.8" marker-end="url(#flowArr)"/>
  <text x="325" y="205" font-size="10" font-weight="bold" fill="#dc2626">No</text>

  <path d="M 610 135 L 650 135" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#flowArr)"/>
  <path d="M 820 135 L 860 135" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#flowArr)"/>
  <path d="M 935 180 L 935 320" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#flowArr)"/>

  <path d="M 860 365 L 810 365" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#flowArr)"/>
  <path d="M 650 365 L 610 365" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#flowArr)"/>
  <text x="618" y="355" font-size="10" font-weight="bold" fill="#15803d">Yes</text>

  <path d="M 440 365 L 400 365" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#flowArr)"/>
</svg>"""

mmd_07 = """flowchart TD
    A[1. Citizen Captures Photo & GPS] --> B{2. Gemini AI Validates Garbage?}
    B -- No (Spam/Selfie) --> B1[Reject Report with Error]
    B -- Yes --> C[3. S3 Upload & SQS Job Enqueue]
    C --> D[4. Auto-Assign Nearest Ward via Haversine SQL]
    D --> E[5. Ward Admin Dispatches Nearest Idle Truck]
    E --> F[6. Worker Cleans Site & Uploads After Photo]
    F --> G{7. Gemini Compares Before vs After?}
    G -- Not Cleaned --> F
    G -- Verified Clean --> H[8. Mark Resolved & Award Citizen Points]
    H --> I[9. Citizen Submits Rating & Feedback]
"""
save_and_render("Figure_4_8_Citizen_Complaint_Workflow", svg_07, mmd_07)

# -------------------------------------------------------------
# 8. 48-Hour SLA Breach Monitoring Workflow
# -------------------------------------------------------------
svg_08 = """<svg width="950" height="520" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <defs>
    <marker id="slaArr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
  </defs>

  <rect width="950" height="520" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="900" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.11: 48-Hour Municipal Service Level Agreement (SLA) Monitoring</text>

  <!-- Box 1 -->
  <g transform="translate(40, 90)">
    <rect width="200" height="90" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.8"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#1e40af">1. Periodic SLA Engine</text>
    <text x="15" y="48" font-size="11" fill="#334155">• Cron / Lambda Trigger</text>
    <text x="15" y="65" font-size="11" fill="#334155">• Executes check-sla.js</text>
    <text x="15" y="80" font-size="11" fill="#334155">• Runs every 15 minutes</text>
  </g>

  <!-- Box 2 -->
  <g transform="translate(300, 90)">
    <rect width="270" height="90" rx="6" fill="#fff7ed" stroke="#f97316" stroke-width="1.8"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#c2410c">2. PostgreSQL Query Evaluation</text>
    <text x="15" y="45" font-size="10" font-family="'Courier New', monospace" fill="#7c2d12">SELECT * FROM complaints</text>
    <text x="15" y="60" font-size="10" font-family="'Courier New', monospace" fill="#7c2d12">WHERE status != 'resolved'</text>
    <text x="15" y="75" font-size="10" font-family="'Courier New', monospace" fill="#7c2d12">AND created_at &lt; NOW() - INTERVAL '48h'</text>
  </g>

  <!-- Decision -->
  <g transform="translate(640, 85)">
    <polygon points="80,0 160,50 80,100 0,50" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>
    <text x="35" y="47" font-size="11" font-weight="bold" fill="#991b1b">Breaches</text>
    <text x="38" y="62" font-size="11" font-weight="bold" fill="#991b1b">Found?</text>
  </g>

  <!-- Compliant Path -->
  <g transform="translate(630, 240)">
    <rect width="180" height="70" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#15803d">SLA Compliant (0 Breaches)</text>
    <text x="15" y="45" font-size="11" fill="#334155">• Normal status maintained</text>
    <text x="15" y="60" font-size="11" fill="#334155">• Green indicators in UI</text>
  </g>

  <!-- Breach Escalation Path -->
  <g transform="translate(40, 240)">
    <rect width="530" height="230" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
    <text x="20" y="30" font-size="15" font-weight="bold" fill="#b91c1c">3. Multi-Tier Breach Escalation Workflow</text>
    
    <rect x="20" y="45" width="490" height="50" rx="4" fill="#ffffff" stroke="#fca5a5"/>
    <text x="35" y="68" font-size="12" font-weight="bold" fill="#991b1b">A. Central Dashboard Alert</text>
    <text x="35" y="85" font-size="11" fill="#475569">Municipal Commissioner sees city-wide breached complaint counter increment</text>

    <rect x="20" y="105" width="490" height="50" rx="4" fill="#ffffff" stroke="#fca5a5"/>
    <text x="35" y="128" font-size="12" font-weight="bold" fill="#991b1b">B. CloudWatch Audit Logging</text>
    <text x="35" y="145" font-size="11" fill="#475569">Structured JSON log pushed to /swachhnet/backend with [SLA_BREACH] tag</text>

    <rect x="20" y="165" width="490" height="50" rx="4" fill="#ffffff" stroke="#fca5a5"/>
    <text x="35" y="188" font-size="12" font-weight="bold" fill="#991b1b">C. Ward Admin Priority Escalation</text>
    <text x="35" y="205" font-size="11" fill="#475569">Flagged with red border on ward map; forces admin to re-dispatch or transfer</text>
  </g>

  <!-- Connectors -->
  <path d="M 240 135 L 300 135" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#slaArr)"/>
  <path d="M 570 135 L 640 135" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#slaArr)"/>

  <path d="M 720 185 L 720 240" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#slaArr)"/>
  <text x="730" y="215" font-size="11" font-weight="bold" fill="#16a34a">No</text>

  <path d="M 640 135 L 600 135 L 600 240 L 570 240" fill="none" stroke="#dc2626" stroke-width="2.5" marker-end="url(#slaArr)"/>
  <text x="605" y="190" font-size="11" font-weight="bold" fill="#dc2626">Yes (&gt; 48h)</text>
</svg>"""

mmd_08 = """flowchart TD
    Trigger[check-sla.js Periodic Evaluation] --> Query[Execute SQL Query on Amazon RDS]
    Query --> Condition{Unresolved Complaints &gt; 48 Hours?}
    Condition -- No --> Normal[Log SLA Normal - Green Dashboard Status]
    Condition -- Yes --> Escalation[Execute 3-Tier Escalation Workflow]
    
    Escalation --> Alert1[Central Dashboard: Increment City-Wide Breach Counter]
    Escalation --> Alert2[Amazon CloudWatch: Structured Audit Log Stream]
    Escalation --> Alert3[Ward Admin Portal: Red Highlight & Priority Dispatch]
"""
save_and_render("Figure_4_11_SLA_Monitoring_Workflow", svg_08, mmd_08)

print("All 6 primary architecture & workflow diagrams generated successfully!")

# -------------------------------------------------------------
# 9. DFD Level 1
# -------------------------------------------------------------
svg_09 = """<svg width="1050" height="650" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <defs>
    <marker id="dfd1Arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
  </defs>

  <rect width="1050" height="650" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="1000" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.7: Level 1 Data Flow Diagram (DFD) - Decomposed Subsystems</text>

  <!-- Process 1.0 Auth -->
  <circle cx="180" cy="150" r="60" fill="#eff6ff" stroke="#3b82f6" stroke-width="2.5"/>
  <text x="165" y="145" font-size="13" font-weight="bold" fill="#1e40af">1.0</text>
  <text x="135" y="165" font-size="12" fill="#1e40af">Auth &amp; RBAC</text>

  <!-- Process 2.0 Ingestion & AI -->
  <circle cx="480" cy="150" r="60" fill="#f0fdf4" stroke="#22c55e" stroke-width="2.5"/>
  <text x="465" y="145" font-size="13" font-weight="bold" fill="#15803d">2.0</text>
  <text x="430" y="165" font-size="12" fill="#15803d">Ingestion &amp; AI</text>

  <!-- Process 3.0 Dispatch & Haversine -->
  <circle cx="780" cy="150" r="60" fill="#fff7ed" stroke="#f97316" stroke-width="2.5"/>
  <text x="765" y="145" font-size="13" font-weight="bold" fill="#c2410c">3.0</text>
  <text x="735" y="165" font-size="12" fill="#c2410c">Dispatch Engine</text>

  <!-- Process 4.0 Cleanup Verification -->
  <circle cx="330" cy="400" r="60" fill="#faf5ff" stroke="#a855f7" stroke-width="2.5"/>
  <text x="315" y="395" font-size="13" font-weight="bold" fill="#6b21a8">4.0</text>
  <text x="280" y="415" font-size="12" fill="#6b21a8">Verification &amp; Pts</text>

  <!-- Process 5.0 SLA & Audit -->
  <circle cx="680" cy="400" r="60" fill="#fef2f2" stroke="#ef4444" stroke-width="2.5"/>
  <text x="665" y="395" font-size="13" font-weight="bold" fill="#b91c1c">5.0</text>
  <text x="635" y="415" font-size="12" fill="#b91c1c">SLA &amp; Monitoring</text>

  <!-- Data Stores -->
  <!-- D1: Users -->
  <g transform="translate(80, 290)">
    <line x1="0" y1="0" x2="160" y2="0" stroke="#0f172a" stroke-width="2"/>
    <line x1="0" y1="35" x2="160" y2="35" stroke="#0f172a" stroke-width="2"/>
    <text x="15" y="23" font-size="12" font-weight="bold" fill="#0f172a">D1: RDS Users Table</text>
  </g>

  <!-- D2: Complaints -->
  <g transform="translate(430, 290)">
    <line x1="0" y1="0" x2="190" y2="0" stroke="#0f172a" stroke-width="2"/>
    <line x1="0" y1="35" x2="190" y2="35" stroke="#0f172a" stroke-width="2"/>
    <text x="15" y="23" font-size="12" font-weight="bold" fill="#0f172a">D2: RDS Complaints Table</text>
  </g>

  <!-- D3: S3 Bucket -->
  <g transform="translate(430, 50)">
    <line x1="0" y1="0" x2="190" y2="0" stroke="#0f172a" stroke-width="2"/>
    <line x1="0" y1="35" x2="190" y2="35" stroke="#0f172a" stroke-width="2"/>
    <text x="15" y="23" font-size="12" font-weight="bold" fill="#0f172a">D3: Amazon S3 Evidence</text>
  </g>

  <!-- D4: CloudWatch Logs -->
  <g transform="translate(620, 520)">
    <line x1="0" y1="0" x2="220" y2="0" stroke="#0f172a" stroke-width="2"/>
    <line x1="0" y1="35" x2="220" y2="35" stroke="#0f172a" stroke-width="2"/>
    <text x="15" y="23" font-size="12" font-weight="bold" fill="#0f172a">D4: CloudWatch Log Streams</text>
  </g>

  <!-- Flows -->
  <path d="M 180 210 L 160 290" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
  <path d="M 240 150 L 420 150" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
  <path d="M 480 210 L 480 290" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
  <path d="M 480 90 L 480 85" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
  <path d="M 540 150 L 720 150" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
  <path d="M 780 210 L 600 295" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
  <path d="M 500 325 L 390 380" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
  <path d="M 680 340 L 590 325" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
  <path d="M 680 460 L 680 520" fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#dfd1Arr)"/>
</svg>"""

mmd_09 = """graph TD
    P1((1.0 Auth & RBAC)) <--> D1[(D1: RDS Users Table)]
    P1 -->|JWT Claims| P2((2.0 Photo Ingestion & AI))
    P2 -->|Save Photo Object| D3[(D3: Amazon S3 Evidence)]
    P2 -->|Create Record| D2[(D2: RDS Complaints Table)]
    P2 -->|Trigger Event| P3((3.0 Dispatch & Haversine))
    P3 -->|Update Assigned Worker| D2
    D2 -->|Fetch Task| P4((4.0 Cleanup Verification))
    P4 -->|Verify Before/After| D3
    P4 -->|Update Resolved| D2
    D2 -->|Evaluate 48h Age| P5((5.0 SLA & Audit))
    P5 -->|Push Events| D4[(D4: CloudWatch Logs)]
"""
save_and_render("Figure_4_7_DFD_Level_1", svg_09, mmd_09)

# -------------------------------------------------------------
# 10. Truck Dispatch Workflow
# -------------------------------------------------------------
svg_10 = """<svg width="900" height="500" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <defs>
    <marker id="tdArr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#c2410c"/>
    </marker>
  </defs>

  <rect width="900" height="500" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="850" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.9: Geospatial Haversine Nearest Truck Dispatch Workflow</text>

  <g transform="translate(40, 90)">
    <rect width="230" height="90" rx="6" fill="#fff7ed" stroke="#f97316" stroke-width="1.8"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#c2410c">1. Admin Opens Ward Portal</text>
    <text x="15" y="48" font-size="11" fill="#334155">• Receives open complaint</text>
    <text x="15" y="65" font-size="11" fill="#334155">• Coordinates: (lat, lng)</text>
    <text x="15" y="80" font-size="11" fill="#334155">• Clicks "Dispatch Nearest"</text>
  </g>

  <g transform="translate(330, 90)">
    <rect width="280" height="90" rx="6" fill="#ffedd5" stroke="#ea580c" stroke-width="1.8"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#7c2d12">2. Haversine SQL Execution</text>
    <text x="10" y="45" font-size="10" font-family="'Courier New', monospace" fill="#431407">SELECT w.user_id, w.truck_number,</text>
    <text x="10" y="60" font-size="10" font-family="'Courier New', monospace" fill="#431407">6371 * acos(...) AS distance_km</text>
    <text x="10" y="75" font-size="10" font-family="'Courier New', monospace" fill="#431407">FROM workers w WHERE status='idle'</text>
  </g>

  <g transform="translate(670, 90)">
    <polygon points="80,0 160,45 80,90 0,45" fill="#fef2f2" stroke="#ef4444" stroke-width="1.8"/>
    <text x="40" y="42" font-size="11" font-weight="bold" fill="#991b1b">Idle Truck</text>
    <text x="35" y="58" font-size="11" font-weight="bold" fill="#991b1b">Available?</text>
  </g>

  <g transform="translate(670, 240)">
    <rect width="180" height="70" rx="6" fill="#fee2e2" stroke="#fca5a5" stroke-width="1.5"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#991b1b">Fleet Busy Notice</text>
    <text x="15" y="45" font-size="11" fill="#7f1d1d">• Admin can queue job</text>
    <text x="15" y="60" font-size="11" fill="#7f1d1d">• Or transfer to adj. ward</text>
  </g>

  <g transform="translate(40, 240)">
    <rect width="570" height="180" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.8"/>
    <text x="20" y="30" font-size="14" font-weight="bold" fill="#15803d">3. Automated Atomic State Assignment</text>
    
    <rect x="20" y="45" width="530" height="50" rx="4" fill="#ffffff" stroke="#86efac"/>
    <text x="35" y="68" font-size="12" font-weight="bold" fill="#166534">A. PostgreSQL Transaction</text>
    <text x="35" y="85" font-size="11" fill="#475569">UPDATE complaints SET status='assigned', worker_id=X; UPDATE workers SET status='busy'</text>

    <rect x="20" y="105" width="530" height="50" rx="4" fill="#ffffff" stroke="#86efac"/>
    <text x="35" y="128" font-size="12" font-weight="bold" fill="#166534">B. Driver Notification &amp; Map Pin</text>
    <text x="35" y="145" font-size="11" fill="#475569">Assigned task appears on Driver Portal with turn-by-turn coordinate route</text>
  </g>

  <path d="M 270 135 L 330 135" fill="none" stroke="#c2410c" stroke-width="2" marker-end="url(#tdArr)"/>
  <path d="M 610 135 L 670 135" fill="none" stroke="#c2410c" stroke-width="2" marker-end="url(#tdArr)"/>

  <path d="M 750 180 L 750 240" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#tdArr)"/>
  <text x="760" y="210" font-size="11" font-weight="bold" fill="#ef4444">No</text>

  <path d="M 670 135 L 630 135 L 630 240 L 610 240" fill="none" stroke="#16a34a" stroke-width="2.5" marker-end="url(#tdArr)"/>
  <text x="635" y="190" font-size="11" font-weight="bold" fill="#16a34a">Yes</text>
</svg>"""

mmd_10 = """flowchart TD
    A[Admin Reviews Complaint Location] --> B[Execute Haversine Distance Formula via SQL]
    B --> C{Idle Trucks Found in Ward?}
    C -- No --> C1[Alert Admin: All Fleet Busy / Option to Transfer Ward]
    C -- Yes --> D[Select Truck with Minimum Distance km]
    D --> E[Execute Atomic DB Transaction: Set status='assigned' & worker status='busy']
    E --> F[Push Task to Sanitation Worker Mobile Dashboard]
"""
save_and_render("Figure_4_9_Truck_Dispatch_Workflow", svg_10, mmd_10)

# -------------------------------------------------------------
# 11. Cleanup Verification Workflow
# -------------------------------------------------------------
svg_11 = """<svg width="900" height="500" xmlns="http://www.w3.org/2000/svg" font-family="'Segoe UI', Helvetica, Arial, sans-serif">
  <defs>
    <marker id="cvArr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#15803d"/>
    </marker>
  </defs>

  <rect width="900" height="500" fill="#f8fafc" rx="10"/>
  <rect x="25" y="15" width="850" height="45" rx="6" fill="#1e293b"/>
  <text x="40" y="44" fill="#ffffff" font-size="18" font-weight="bold">Figure 4.10: Before &amp; After Photographic Cleanup Verification Workflow</text>

  <g transform="translate(40, 90)">
    <rect width="210" height="90" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.8"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#1e40af">1. Worker at Site</text>
    <text x="15" y="48" font-size="11" fill="#334155">• Cleans garbage heap</text>
    <text x="15" y="65" font-size="11" fill="#334155">• Takes cleanup photo</text>
    <text x="15" y="80" font-size="11" fill="#334155">• Submits to /api/worker</text>
  </g>

  <g transform="translate(290, 90)">
    <rect width="230" height="90" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.8"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#15803d">2. S3 Direct Upload</text>
    <text x="15" y="48" font-size="11" fill="#334155">• Saved to cleanup/ folder</text>
    <text x="15" y="65" font-size="11" fill="#334155">• Generates UUID key</text>
    <text x="15" y="80" font-size="11" fill="#334155">• Status: pending_verification</text>
  </g>

  <g transform="translate(560, 90)">
    <polygon points="80,0 160,45 80,90 0,45" fill="#fdf4ff" stroke="#d946ef" stroke-width="2"/>
    <text x="35" y="42" font-size="11" font-weight="bold" fill="#86198f">3. Gemini AI</text>
    <text x="35" y="58" font-size="11" font-weight="bold" fill="#86198f">Comparison</text>
  </g>

  <g transform="translate(560, 240)">
    <rect width="180" height="75" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
    <text x="15" y="25" font-size="12" font-weight="bold" fill="#b91c1c">Incomplete Cleanup</text>
    <text x="15" y="45" font-size="11" fill="#475569">• AI flags residual waste</text>
    <text x="15" y="60" font-size="11" fill="#475569">• Worker prompted to reclean</text>
  </g>

  <g transform="translate(40, 240)">
    <rect width="480" height="180" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8"/>
    <text x="20" y="30" font-size="14" font-weight="bold" fill="#166534">4. Verification Success &amp; Closure</text>

    <rect x="20" y="45" width="440" height="50" rx="4" fill="#ffffff" stroke="#86efac"/>
    <text x="35" y="68" font-size="12" font-weight="bold" fill="#15803d">A. State Update &amp; Fleet Release</text>
    <text x="35" y="85" font-size="11" fill="#475569">complaints.status='resolved'; workers.status='idle'</text>

    <rect x="20" y="105" width="440" height="50" rx="4" fill="#ffffff" stroke="#86efac"/>
    <text x="35" y="128" font-size="12" font-weight="bold" fill="#15803d">B. Gamification Reward</text>
    <text x="35" y="145" font-size="11" fill="#475569">Citizen receives +10 points; unlock level badges &amp; prompt rating</text>
  </g>

  <path d="M 250 135 L 290 135" fill="none" stroke="#15803d" stroke-width="2" marker-end="url(#cvArr)"/>
  <path d="M 520 135 L 560 135" fill="none" stroke="#15803d" stroke-width="2" marker-end="url(#cvArr)"/>

  <path d="M 640 180 L 640 240" fill="none" stroke="#ef4444" stroke-width="2" marker-end="url(#cvArr)"/>
  <text x="650" y="210" font-size="11" font-weight="bold" fill="#ef4444">Residual Waste</text>

  <path d="M 560 135 L 520 135 L 520 240 L 520 240" fill="none" stroke="#15803d" stroke-width="2.5" marker-end="url(#cvArr)"/>
  <text x="525" y="190" font-size="11" font-weight="bold" fill="#15803d">Clean</text>
</svg>"""

mmd_11 = """flowchart TD
    A[Worker Completes Waste Removal at Site] --> B[Upload After Cleanup Photo via App]
    B --> C[Private S3 Upload to cleanup/ Folder]
    C --> D[Retrieve S3 Buffers for Before and After Photos]
    D --> E{Google Gemini Vision: Compare Cleanliness?}
    E -- Residual Waste Detected --> F[Rejection: Worker Must Re-clean and Re-submit]
    E -- Site Verified Clean --> G[Mark Complaint Status 'resolved']
    G --> H[Set Worker Status back to 'idle']
    H --> I[Credit 10 Eco-Points & Badge to Citizen]
"""
save_and_render("Figure_4_10_Cleanup_Verification_Workflow", svg_11, mmd_11)

print("All diagrams generated successfully!")
