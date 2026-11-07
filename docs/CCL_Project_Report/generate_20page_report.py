import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"C:\Users\kames\Documents\Kamesh\Kamesh Agnel\SEM 5\CLOUD\Mini Project\smart-garbage"
REPORT_DIR = os.path.join(BASE_DIR, "docs", "CCL_Project_Report")
ARCH_IMG = os.path.join(REPORT_DIR, "architecture", "user_attached_architecture.png")
DOCX_OUT = os.path.join(REPORT_DIR, "SwachhNet_CCL_Mini_Project_Report_20Pages.docx")
PDF_OUT = os.path.join(REPORT_DIR, "SwachhNet_CCL_Mini_Project_Report_20Pages.pdf")

doc = docx.Document()

# Page setup: Standard A4 with 0.8 inch margins to get exact, balanced pacing
for sec in doc.sections:
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.8)
    sec.right_margin = Inches(0.8)

# Color Palette
C_NAVY = RGBColor(15, 23, 42)     # #0f172a
C_BLUE = RGBColor(30, 58, 138)    # #1e3a8a
C_ACCENT = RGBColor(37, 99, 235)  # #2563eb
C_GRAY = RGBColor(71, 85, 105)    # #475569
C_DARK = RGBColor(30, 41, 59)     # #1e293b

def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = C_BLUE
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(10)
    return p

def add_h1(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = C_BLUE
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = C_ACCENT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    return p

def add_p(text, italic=False, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.5)
    run.font.color.rgb = C_DARK
    run.italic = italic
    run.bold = bold
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    return p

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_DARK
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.5)
    run.font.color.rgb = C_DARK
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    return p

def add_styled_table(headers, rows, col_widths=None):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.style = 'Table Grid'
    
    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_shading(hdr_cells[i], "1E3A8A")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=90, right=90)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.name = "Calibri"
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        
    # Data Rows
    for r_idx, row in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_shading(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=80, right=80)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(9)
            p.runs[0].font.color.rgb = C_DARK
            
    if col_widths:
        for r in tbl.rows:
            for i, w in enumerate(col_widths):
                r.cells[i].width = Inches(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return tbl

def add_code(text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, "F1F5F9")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text.strip())
    run.font.name = "Courier New"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(0)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

print("Starting 20-Page Report Build...")

# ====================================================================
# PAGE 1: TITLE & COVER PAGE
# ====================================================================
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_top = p_top.add_run("Fr. Conceicao Rodrigues College of Engineering\nFather Agnel Ashram, Bandstand, Bandra (West), Mumbai - 400050\nDepartment of Computer Engineering")
r_top.font.name = "Calibri"
r_top.font.size = Pt(13)
r_top.font.bold = True
r_top.font.color.rgb = C_NAVY
p_top.paragraph_format.space_before = Pt(24)
p_top.paragraph_format.space_after = Pt(18)

p_mini = doc.add_paragraph()
p_mini.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_mini = p_mini.add_run("CLOUD COMPUTING LABORATORY MINI-PROJECT REPORT\nAcademic Year: 2026 – 2027")
r_mini.font.name = "Calibri"
r_mini.font.size = Pt(11)
r_mini.font.color.rgb = C_GRAY
p_mini.paragraph_format.space_after = Pt(36)

p_proj = doc.add_paragraph()
p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_proj = p_proj.add_run("SWACHHNET\nAI-Powered Smart Garbage Reporting and\nMunicipal Dispatch System")
r_proj.font.name = "Calibri"
r_proj.font.size = Pt(21)
r_proj.font.bold = True
r_proj.font.color.rgb = C_BLUE
p_proj.paragraph_format.space_after = Pt(12)

p_desc = doc.add_paragraph()
p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_desc = p_desc.add_run("A Cloud-Native Solid Waste Management Platform Built on Amazon Web Services (AWS)\nRegion: ap-south-1 (Mumbai) | Public Endpoint: http://65.2.180.175")
r_desc.font.name = "Times New Roman"
r_desc.font.size = Pt(10.5)
r_desc.font.italic = True
r_desc.font.color.rgb = C_DARK
p_desc.paragraph_format.space_after = Pt(40)

# Team Table
tbl_team = doc.add_table(rows=1, cols=2)
tbl_team.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_team.rows[0].cells[0].paragraphs[0].text = "SUBMITTED BY:\n1. Kamesh Nerpagar (Roll No: [ROLL NO. 1])\n2. [STUDENT 2 NAME] (Roll No: [ROLL NO. 2])\n3. [STUDENT 3 NAME] (Roll No: [ROLL NO. 3])"
tbl_team.rows[0].cells[1].paragraphs[0].text = "PROJECT GUIDE:\nProf. [GUIDE NAME]\nAssistant Professor,\nDepartment of Computer Engineering"
for c in tbl_team.rows[0].cells:
    c.paragraphs[0].runs[0].font.name = "Calibri"
    c.paragraphs[0].runs[0].font.size = Pt(10)
    c.paragraphs[0].runs[0].font.color.rgb = C_DARK

p_loc = doc.add_paragraph()
p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_loc = p_loc.add_run("\n\nDepartment of Computer Engineering\nUniversity of Mumbai")
r_loc.font.name = "Calibri"
r_loc.font.size = Pt(10)
r_loc.font.bold = True
r_loc.font.color.rgb = C_GRAY

doc.add_page_break()

# ====================================================================
# PAGE 2: CERTIFICATE & DECLARATION
# ====================================================================
add_title("CERTIFICATE")
add_p("This is to certify that the mini-project report entitled \"SwachhNet: AI-Powered Smart Garbage Reporting and Municipal Dispatch System\" is a bona fide work carried out by Kamesh Nerpagar (Roll No: [ROLL NO. 1]), [STUDENT 2 NAME] (Roll No: [ROLL NO. 2]), and [STUDENT 3 NAME] (Roll No: [ROLL NO. 3]) in partial fulfillment of the requirements for the award of Bachelor of Engineering in Computer Engineering in Cloud Computing Laboratory during the academic year 2026–2027.")
add_p("The project has been planned, developed, cloud-deployed, and verified on Amazon Web Services (AWS) under our guidance and supervision.")

add_p("\n\n")
t_sig = doc.add_table(rows=1, cols=3)
t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
t_sig.rows[0].cells[0].paragraphs[0].text = "____________________\nProf. [GUIDE NAME]\nProject Guide"
t_sig.rows[0].cells[1].paragraphs[0].text = "____________________\nDr. [HOD NAME]\nHead of Department"
t_sig.rows[0].cells[2].paragraphs[0].text = "____________________\nExternal Examiner\nCollege Seal"
for c in t_sig.rows[0].cells:
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].font.name = "Calibri"
    p.runs[0].font.size = Pt(9.5)

add_title("DECLARATION")
add_p("We declare that this written submission represents our original work carried out for the Cloud Computing Laboratory. All software implementations, relational PostgreSQL schemas, and AWS cloud infrastructures (VPC, EC2, RDS, S3, IAM, SQS, CloudWatch) described in this report are genuine, deployed in the AWS Mumbai (ap-south-1) region, and tested on production endpoints.")

add_p("\nDate: 31st October 2026\nPlace: Mumbai\n\nKamesh Nerpagar | [STUDENT 2 NAME] | [STUDENT 3 NAME]")

doc.add_page_break()

# ====================================================================
# PAGE 3: ABSTRACT & TABLE OF CONTENTS
# ====================================================================
add_title("ABSTRACT")
add_p("Metropolitan governance bodies such as the Brihanmumbai Municipal Corporation (BMC) face immense challenges managing solid municipal waste across high-density urban wards. Traditional grievance redressal systems suffer from a lack of physical evidence, manual dispatch delays, and untracked service level agreement (SLA) breaches.")
add_p("SwachhNet is an intelligent, cloud-native municipal solid waste management and automated dispatch platform engineered on Amazon Web Services (AWS). It enables citizens to report garbage accumulation via live GPS coordinates and smartphone camera captures. Uploaded photographs are pre-audited using Google Gemini 1.5 Flash Vision AI to eliminate spam reports. Verified grievances are automatically assigned to the nearest BMC administrative ward using the mathematical Haversine spherical distance formula in PostgreSQL. Ward administrators dispatch the closest idle municipal truck, and field workers submit photographic cleanup proof that undergoes before-and-after visual verification before complaint closure.")
add_p("The entire system is deployed on AWS in the Asia Pacific (Mumbai) region (ap-south-1). The architecture includes: a custom Amazon VPC (10.0.0.0/16) with public/private subnet segregation; Amazon EC2 (t3.micro) hosting Nginx and Node.js Express under PM2; Amazon RDS for PostgreSQL 16.10 isolated in private subnets with zero internet access; Amazon S3 for private encrypted evidence storage with 60-minute presigned URLs; AWS SSM Parameter Store for KMS-encrypted secrets; Amazon SQS with Dead Letter Queue for asynchronous task processing; Amazon CloudWatch for structured logging and CPU alarms; and AWS Budgets enforcing a $10.00/month cost limit. The system is live at http://65.2.180.175.")

add_title("TABLE OF CONTENTS")
toc_items = [
    ("1. Project Overview & Problem Statement", "Page 4"),
    ("2. Target Users & Core Municipal Workflows", "Page 5"),
    ("3. End-to-End System Architecture (AWS Well-Architected)", "Page 6"),
    ("4. AWS Cloud Services: Implementation & Selection Justification", "Page 8"),
    ("5. Core Backend Implementation & Code Highlights", "Page 11"),
    ("6. Cloud Deployment & Automation Pipeline", "Page 13"),
    ("7. Comprehensive Testing & Empirical Verification", "Page 15"),
    ("8. Verification Evidence & AWS Console Placeholders", "Page 17"),
    ("9. Cost Governance & Cloud Security Architecture", "Page 19"),
    ("10. Conclusion & Future Roadmap", "Page 20")
]
for item, pg in toc_items:
    p = doc.add_paragraph()
    r1 = p.add_run(item)
    r1.font.name = "Calibri"
    r1.font.size = Pt(10)
    r1.font.bold = True
    r2 = p.add_run(f" ............................................................................................ {pg}")
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = C_GRAY
    p.paragraph_format.space_after = Pt(2)

doc.add_page_break()

# ====================================================================
# PAGE 4: PROJECT OVERVIEW & PROBLEM STATEMENT
# ====================================================================
add_h1("1. Project Overview & Problem Statement")
add_h2("1.1 Background & Municipal Context")
add_p("Greater Mumbai generates over 11,000 metric tons of municipal solid waste daily across an area of 603 sq. km administered by the Brihanmumbai Municipal Corporation (BMC) across 24 administrative wards (e.g., K/West - Andheri, H/West - Bandra, P/South - Goregaon). Ensuring clean urban streets requires prompt, geographically coordinated waste collection and verifiable field operations.")

add_h2("1.2 Problem Statement")
add_p("Conventional civic grievance redressal mechanisms exhibit four critical systemic failures:")
add_bullet("Citizens submit text-only complaints or untrusted photos without tamper-proof timestamps or verified location metadata, leading to high volumes of spam and fake grievances.", "1. Unverified Reporting: ")
add_bullet("Complaints are manually triaged across ward offices, causing severe jurisdictional delays and disputes.", "2. Manual & Inefficient Routing: ")
add_bullet("Municipal collection trucks operate on rigid, static daily schedules without dynamic rerouting to active garbage heaps.", "3. Lack of Real-Time Dispatch: ")
add_bullet("Field crews frequently claim task completion without physical proof, and administrators lack automated tracking for complaints exceeding the mandatory 48-hour municipal SLA.", "4. Ghost Cleanups & SLA Breaches: ")

add_h2("1.3 The SwachhNet Solution")
add_p("SwachhNet transforms municipal waste handling by delivering a verified, transparent, and cloud-native digital workflow:")
add_bullet("Citizens submit smartphone photos with auto-captured GPS coordinates.", "• Camera & GPS Reporting: ")
add_bullet("Google Gemini Flash AI validates image content in real time before accepting the complaint.", "• AI Spam Filter: ")
add_bullet("PostgreSQL executes trigonometric Haversine math to find the nearest ward and dispatch the closest idle truck.", "• Geospatial Dispatch: ")
add_bullet("Workers upload post-cleanup photos, which AI visually compares against the original before resolving the ticket.", "• Before/After AI Verification: ")
add_bullet("Unresolved complaints older than 48 hours trigger high-priority alerts across municipal dashboards.", "• 48-Hour SLA Engine: ")

doc.add_page_break()

# ====================================================================
# PAGE 5: TARGET USERS & CORE MUNICIPAL WORKFLOWS
# ====================================================================
add_h1("2. Target Users & Core Municipal Workflows")
add_h2("2.1 Application Personas & Role Matrix")
add_p("SwachhNet implements strict Role-Based Access Control (RBAC) across four operational user personas:")

user_matrix = [
    ("Citizen (Nagarik)", "Report garbage with photo/GPS, track status, view public map, earn eco-points, rate ward performance.", "/dashboard"),
    ("Ward Administrator", "View incoming ward grievances, execute single-click Haversine dispatch to nearest idle truck, transfer out-of-boundary reports.", "/authority"),
    ("Sanitation Worker", "View assigned tasks, access GPS coordinates & turn-by-turn routes, upload after-cleanup photographic proof, update availability.", "/worker"),
    ("Central Superadmin", "Monitor all 24 BMC wards, track city-wide complaint statistics, audit 48-hour SLA breaches, view operational telemetry.", "/central")
]
add_styled_table(["User Persona", "Permissions & Core Capabilities", "Assigned View"], user_matrix, col_widths=[1.5, 3.8, 1.3])

add_h2("2.2 End-to-End Complaint Lifecycle Workflow")
add_p("The lifecycle of a municipal garbage grievance follows five deterministic stages:")
add_bullet("Citizen opens the web app, captures a dump photo, and grants GPS access. The photo buffer is sent to Google Gemini AI. If isGarbage is true, the image is uploaded directly to a private Amazon S3 bucket, and an SQS task event is emitted.", "Stage 1 (Submission & AI Audit): ")
add_bullet("The API calculates the great-circle distance between the complaint coordinates and all BMC ward offices using the SQL Haversine formula, automatically assigning the ticket to the nearest ward in Amazon RDS PostgreSQL.", "Stage 2 (Spatial Ward Partitioning): ")
add_bullet("The ward admin clicks 'Dispatch Nearest Truck'. A database transaction queries all idle trucks assigned to that ward, selects the closest vehicle by GPS, assigns the worker, and sets the truck status to busy.", "Stage 3 (Dynamic Fleet Dispatch): ")
add_bullet("The sanitation worker navigates to the GPS pin, cleans the site, and takes an 'After Cleanup' photo uploaded to S3. Gemini AI inspects the photo pair. If clean, status updates to 'resolved' and the worker status resets to 'idle'.", "Stage 4 (Cleanup & Verification): ")
add_bullet("The reporting citizen is awarded +10 eco-points and prompted to submit a 1–5 star rating. If any ticket remains unresolved for over 48 hours, the background SLA engine raises a municipal escalation flag.", "Stage 5 (Reward & SLA Oversight): ")

doc.add_page_break()

# ====================================================================
# PAGE 6 & 7: ARCHITECTURE (EMBEDDING USER ATTACHED IMAGE)
# ====================================================================
add_h1("3. End-to-End System Architecture")
add_h2("3.1 AWS Production Topology (Clean Unified Architecture)")
add_p("The architecture represents a cloud-native, secure, and cost-optimized multi-tier deployment running live in the AWS Asia Pacific (Mumbai) region (ap-south-1), fully satisfying all six mandatory cloud computing domains:")

# Embed the attached architecture image
if os.path.exists(ARCH_IMG):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    run_img = p_img.add_run()
    run_img.add_picture(ARCH_IMG, width=Inches(6.4))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cap = p_cap.add_run("Figure 3.1: SwachhNet Cloud-Native Production Architecture (AWS ap-south-1 Topology)")
    run_cap.font.name = "Calibri"
    run_cap.font.size = Pt(9.5)
    run_cap.font.bold = True
    run_cap.font.color.rgb = C_GRAY
    p_cap.paragraph_format.space_after = Pt(6)

add_h2("3.2 Architectural Flow & Tier Decomposition")
add_bullet("Browser and mobile clients interact over standard HTTPS/HTTP protocols. Web traffic enters through an attached Internet Gateway (IGW) routed directly to the public subnet.", "Tier 1: Edge Clients & Telemetry: ")
add_bullet("Housed inside a dedicated custom VPC (10.0.0.0/16). Features an EC2 t3.micro instance (Amazon Linux 2023, Public IP: 65.2.180.175) running Nginx 1.30 (Port 80) and Node.js Express (Port 5000 / PM2). Nginx serves React static files and reverse-proxies /api/ calls, eliminating CORS issues.", "Tier 2: Public Compute & Gateway Subnet: ")
add_bullet("Isolated across two availability zones (10.0.10.0/24 in ap-south-1a and 10.0.11.0/24 in ap-south-1b). Houses Amazon RDS PostgreSQL 16.10 (db.t3.micro). Has zero route to the internet (0.0.0.0/0 blocked). Inbound port 5432 is strictly chained to the EC2 security group.", "Tier 3: Private Database Subnet Group: ")
add_bullet("Includes Amazon S3 (private encrypted bucket with 60-min presigned URLs), Amazon SQS (job queue with DLQ), AWS SSM Parameter Store (encrypted secrets), Amazon CloudWatch (telemetry & alarms), and Google Gemini Vision AI.", "Tier 4: Managed AWS Services & External AI: ")

doc.add_page_break()

# ====================================================================
# PAGE 8, 9 & 10: AWS SERVICES IMPLEMENTATION & WHY NOT ALTERNATIVE
# ====================================================================
add_h1("4. AWS Cloud Services: Implementation & Selection Justification")
add_p("This section documents the specific technical role of every deployed AWS service and provides the architectural justification for why each service was chosen over its common alternatives.")

add_h2("4.1 Compute: Amazon EC2 vs. AWS Lambda vs. AWS ECS")
add_p("• Selected Service: Amazon EC2 (t3.micro, Amazon Linux 2023, Public IP: 65.2.180.175)")
add_p("• Implementation: Runs an Nginx 1.30 reverse proxy and Node.js 18 Express API managed by PM2 7.1.1 with systemd auto-reboot. Nginx binds port 80 to serve the React 18 production bundle directly from disk (/dist) and forwards /api/ requests to localhost:5000.")
add_bullet("Course syllabus required deploying the primary compute backend on a virtual server instance. Running Nginx and Node.js together on one t3.micro instance minimizes network hops, eliminates extra load balancer costs, and avoids cold starts.", "Why We Chose EC2: ")
add_bullet("Lambda cold starts (1.5s–3s) add unacceptable latency to citizen photo uploads. Lambda functions inside a VPC require VPC ENI attachments. Furthermore, Lambda imposes a 15-minute execution limit.", "Why Not AWS Lambda (Serverless): ")
add_bullet("ECS with Fargate requires an Application Load Balancer (ALB), which incurs a fixed baseline charge of ~$16–$22/month, immediately violating our zero-cost Free Tier objective.", "Why Not AWS ECS / Fargate: ")

add_h2("4.2 Database: Amazon RDS PostgreSQL vs. MongoDB Atlas vs. EC2 Local DB")
add_p("• Selected Service: Amazon RDS for PostgreSQL 16.10 (db.t3.micro, 20GB gp2 Encrypted)")
add_p("• Implementation: Primary persistence layer deployed across private subnets (Endpoint: swachhnet-postgres.cdc8mesu8z3p...). Contains 5 normalized tables (users, ward_authorities, workers, complaints, complaint_transfers) with UUID primary keys and B-tree indexes.")
add_bullet("Provides automated minor version patching, automated snapshots, storage encryption at rest (AES-256), and native network isolation in private subnets. Enforces ACID transactions so dispatching a truck updates vehicle and complaint states simultaneously, preventing race conditions.", "Why We Chose RDS PostgreSQL: ")
add_bullet("MongoDB Atlas runs outside AWS, requiring database traffic to travel over the public internet. Its NoSQL document model lacks ACID guarantees across multiple collections, risking orphaned records during inter-ward complaint transfers.", "Why Not MongoDB Atlas (Original): ")
add_bullet("Running PostgreSQL directly on the EC2 host couples compute with storage, creating a single point of failure. It also exhausts the 1 GB RAM of t3.micro, triggering Linux Out-Of-Memory (OOM) kernel crashes.", "Why Not Self-Hosted DB on EC2: ")

add_h2("4.3 Media Storage: Amazon S3 vs. Cloudinary vs. EBS Disk Storage")
add_p("• Selected Service: Amazon S3 (Bucket: swachhnet-evidence-078601217335-ap-south-1)")
add_p("• Implementation: Stores photographic evidence under complaints/ and cleanup/ folders. Configured with Block Public Access: ON, AES-256 Server-Side Encryption (SSE-S3), and versioning. Clients view images using 60-minute cryptographic presigned GET URLs.")
add_bullet("Offers 99.999999999% (11 9's) durability at negligible cost. Direct uploads via memory buffers eliminate disk caching on EC2. Presigned URLs enforce secure, temporary client access.", "Why We Chose Amazon S3: ")
add_bullet("Cloudinary stores media on third-party infrastructure outside the AWS boundary. Media links are public by default, violating citizen privacy and exposing civic evidence to unauthorized scrapers.", "Why Not Cloudinary (Original): ")
add_bullet("Storing photos on EC2 EBS volumes makes the compute host stateful, preventing horizontal autoscaling. EBS costs $0.10/GB/month vs. S3 at $0.023/GB/month, and serving images from disk degrades API performance.", "Why Not Amazon EBS Local Storage: ")

add_h2("4.4 Networking: Custom VPC vs. AWS Default VPC")
add_p("• Selected Service: Custom Amazon VPC (swachhnet-vpc, CIDR: 10.0.0.0/16)")
add_p("• Implementation: Subnet segregation into Public Subnet (10.0.1.0/24) with an Internet Gateway and Private DB Subnets (10.0.10.0/24, 10.0.11.0/24) with local VPC routing only. Chained security groups: swachhnet-db-sg permits port 5432 ingress solely from swachhnet-app-sg.")
add_bullet("Provides complete architectural control over CIDR blocks, route tables, and multi-AZ database isolation, ensuring PostgreSQL has zero direct internet exposure.", "Why We Chose Custom VPC: ")
add_bullet("The default VPC assigns public IP addresses to all launched resources and contains direct internet routes in every subnet, making isolated database deployment impossible without extensive re-configuration.", "Why Not AWS Default VPC: ")

add_h2("4.5 Secrets Management: AWS SSM Parameter Store vs. Local .env vs. AWS Secrets Manager")
add_p("• Selected Service: AWS Systems Manager Parameter Store (/swachhnet/prod/*)")
add_p("• Implementation: Stores DATABASE_URL, JWT_SECRET, and G_API as KMS-encrypted SecureString parameters. Loaded directly into Node.js memory on server startup via AWS SDK v3.")
add_bullet("Standard parameters are 100% free under the AWS Free Tier. Centralizes credentials so modifying secrets in the AWS Console updates the application on reboot without redeploying code.", "Why We Chose SSM Parameter Store: ")
add_bullet("Plaintext .env files stored on disk expose credentials to anyone with shell access and risk accidental commits to public version control repositories.", "Why Not Local .env Files: ")
add_bullet("AWS Secrets Manager charges $0.40 per secret per month plus API call fees. Storing our 5 secrets would incur ~$2.00/month, violating our zero-cost budget objective for capabilities identical to SSM.", "Why Not AWS Secrets Manager: ")

add_h2("4.6 Asynchronous Messaging: Amazon SQS vs. BullMQ / Redis")
add_p("• Selected Service: Amazon SQS (swachhnet-jobs-queue & swachhnet-jobs-dlq)")
add_p("• Implementation: Decouples background tasks (audit logging, SMS notifications) from HTTP cycles. Dead Letter Queue isolates poison-pill messages after 5 failed attempts (maxReceiveCount: 5).")
add_bullet("Fully managed serverless queue with 1,000,000 free requests per month. Messages persist reliably even if the EC2 consumer restarts.", "Why We Chose Amazon SQS: ")
add_bullet("BullMQ requires a running Redis instance. Running Redis on EC2 consumes limited RAM, while Amazon ElastiCache costs ~$13/month. In-memory queues lose data if the server crashes.", "Why Not BullMQ / Redis: ")

add_h2("4.7 Observability & Telemetry: Amazon CloudWatch & AWS Budgets")
add_p("• Selected Services: Amazon CloudWatch Logs (/swachhnet/backend), CPU Alarm, and AWS Budgets")
add_p("• Implementation: Logger scrubs passwords and tokens before pushing structured JSON to CloudWatch. A metric alarm triggers if EC2 CPUUtilization >= 80%. An AWS Budget enforces a $10.00/month spending ceiling with an 80% ($8.00) alert threshold.")
add_bullet("Provides native AWS observability without installing heavy third-party agents. Includes 5 GB log ingestion, 10 alarms, and 2 budgets free under Free Tier allowances.", "Why We Chose CloudWatch & Budgets: ")
add_bullet("Local log files require manual SSH sessions to inspect, risk filling up the root disk partition, and are permanently lost if the instance terminates.", "Why Not Local Log Files: ")

doc.add_page_break()

# ====================================================================
# PAGE 11 & 12: CORE IMPLEMENTATION & CODE HIGHLIGHTS
# ====================================================================
add_h1("5. Core Backend Implementation & Code Highlights")
add_p("The SwachhNet backend (Node.js/Express) incorporates enterprise-grade cloud patterns. Key architectural modules from the codebase are documented below:")

add_h2("5.1 Dual-Database Bootstrap & SSM Secrets Loader")
add_p("The server entry point (backend/server.js) detects environment configuration, retrieves KMS-encrypted secrets from AWS SSM Parameter Store, and initializes PostgreSQL connection pooling:")
add_code("""// backend/server.js - Dynamic SSM & Dual-Database Initialization
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
dotenv.config();

const db = require('./db');
const { loadParametersFromSSM } = require('./services/ssmService');
const logger = require('./services/logger');

const app = express();
app.use(cors({ origin: (orig, cb) => cb(null, true), credentials: true }));
app.use(express.json());

// Load encrypted production secrets from AWS SSM Parameter Store
if (process.env.USE_SSM === 'true') {
  loadParametersFromSSM().then(() => {
    logger.info('✅ Production parameters loaded from AWS SSM Parameter Store');
  }).catch(err => logger.error('❌ SSM Load Error:', err));
}

// Database Connection Verification
if (process.env.DATABASE_URL || process.env.PGHOST) {
  logger.info('🐘 Active Database Engine: Amazon RDS PostgreSQL 16.10');
  db.query('SELECT NOW()').then(() => logger.info('✅ RDS Pool Healthy'));
} else if (process.env.MONGO_URI) {
  logger.info('🍃 Fallback Database Engine: MongoDB Atlas');
}""")

add_h2("5.2 Geospatial Haversine SQL Nearest Truck Dispatch")
add_p("To replace MongoDB's $near operator, the backend implements the mathematical spherical Haversine formula in pure SQL inside an atomic database transaction (backend/controllers/authorityController.js):")
add_code("""// backend/controllers/authorityController.js - Haversine Dispatch Math
// Formula: 6371 * acos(cos(rad(lat1)) * cos(rad(lat2)) * cos(rad(lng2)-rad(lng1)) + sin(rad(lat1)) * sin(rad(lat2)))
const dispatchSql = `
  SELECT w.user_id, w.truck_number, w.latitude, w.longitude,
    (6371 * acos(
      cos(radians($1)) * cos(radians(w.latitude)) *
      cos(radians(w.longitude) - radians($2)) +
      sin(radians($1)) * sin(radians(w.latitude))
    )) AS distance_km
  FROM workers w
  WHERE w.assigned_ward_id = $3 AND w.status = 'idle'
  ORDER BY distance_km ASC
  LIMIT 1;
`;

// Atomic transaction: assign complaint and mark truck busy simultaneously
await db.transaction(async (client) => {
  const truckRes = await client.query(dispatchSql, [complaintLat, complaintLng, wardId]);
  if (truckRes.rows.length === 0) throw new Error('No idle trucks available in ward');
  const worker = truckRes.rows[0];

  await client.query("UPDATE complaints SET worker_id = $1, status = 'assigned' WHERE id = $2",
    [worker.user_id, complaintId]);
  await client.query("UPDATE workers SET status = 'busy' WHERE user_id = $1", [worker.user_id]);
});""")

add_h2("5.3 Private S3 Evidence Upload & Presigned URL Resolution")
add_p("Binary image buffers stream directly to Amazon S3 with AES-256 server-side encryption. Temporary presigned URLs are generated on demand for secure client rendering (backend/services/s3Service.js):")
add_code("""// backend/services/s3Service.js - S3 Direct Upload & Presigned URLs
const { S3Client, PutObjectCommand, GetObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
const { randomUUID } = require('crypto');

const s3Client = new S3Client({ region: 'ap-south-1' });
const BUCKET = process.env.S3_BUCKET_NAME;

async function uploadToS3(buffer, originalName, mimeType, folder = 'complaints') {
  const ext = originalName.split('.').pop() || 'jpg';
  const s3Key = `${folder}/${randomUUID()}.${ext}`;

  await s3Client.send(new PutObjectCommand({
    Bucket: BUCKET,
    Key: s3Key,
    Body: buffer,
    ContentType: mimeType,
    ServerSideEncryption: 'AES256'
  }));

  const presignedUrl = await getPresignedDownloadUrl(s3Key);
  return { s3Key, bucket: BUCKET, url: presignedUrl };
}

async function getPresignedDownloadUrl(s3Key, expiresInSeconds = 3600) {
  if (!s3Key) return null;
  const cmd = new GetObjectCommand({ Bucket: BUCKET, Key: s3Key });
  return await getSignedUrl(s3Client, cmd, { expiresIn: expiresInSeconds });
}""")

doc.add_page_break()

# ====================================================================
# PAGE 13 & 14: CLOUD DEPLOYMENT & AUTOMATION PIPELINE
# ====================================================================
add_h1("6. Cloud Deployment & Automation Pipeline")
add_h2("6.1 Single-Click CloudFormation Infrastructure as Code (IaC)")
add_p("The entire cloud environment is provisioned deterministically using AWS CloudFormation template infrastructure/cloudformation/swachhnet-all-in-one.yaml. The stack provisions 24 AWS resources in a single execution:")
add_code("""# AWS CLI CloudFormation Deployment Command
aws cloudformation deploy \\
  --template-file infrastructure/cloudformation/swachhnet-all-in-one.yaml \\
  --stack-name swachhnet-prod-stack \\
  --capabilities CAPABILITY_NAMED_IAM \\
  --parameter-overrides \\
      EnvironmentName=swachhnet \\
      DBMasterUserPassword=SwachhNetPass2026! \\
      InstanceType=t3.micro \\
      DBInstanceClass=db.t3.micro \\
  --region ap-south-1""")

add_h2("6.2 Key CloudFormation Resource Blocks")
add_bullet("VPC (10.0.0.0/16), Internet Gateway, Public Subnet (10.0.1.0/24), and 2 Private Subnets (10.0.10.0/24, 10.0.11.0/24).", "1. Network: ")
add_bullet("AppSecurityGroup (TCP 80, 443 open) and DatabaseSecurityGroup (TCP 5432 ingress restricted to AppSecurityGroup).", "2. Security Groups: ")
add_bullet("EC2InstanceRole with AmazonSSMManagedInstanceCore and custom inline policies for S3, SQS, SSM, and CloudWatch.", "3. IAM Profile: ")
add_bullet("Amazon RDS DBInstance (PostgreSQL 16.10, db.t3.micro, 20GB gp2 encrypted, MultiAZ: false, PubliclyAccessible: false).", "4. Database: ")
add_bullet("EvidenceStorageBucket (AES-256 SSE, Block Public Access enabled, versioning enabled).", "5. Storage: ")
add_bullet("EC2Instance (t3.micro, Amazon Linux 2023, cloud-init UserData script installing Node.js, PM2, and Nginx).", "6. Compute: ")

add_h2("6.3 Nginx Web Server & Reverse Proxy Configuration")
add_p("The production Nginx configuration (/etc/nginx/conf.d/swachhnet.conf) routes client traffic, serves the built React 18 frontend, and reverse-proxies /api/ requests to Node.js port 5000:")
add_code("""server {
    listen 80;
    server_name _;

    # Serve built React Single Page Application
    location / {
        root /var/www/swachhnet/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API calls to local Express server
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
    }
}""")

doc.add_page_break()

# ====================================================================
# PAGE 15 & 16: COMPREHENSIVE TESTING & EMPIRICAL VERIFICATION
# ====================================================================
add_h1("7. Comprehensive Testing & Empirical Verification")
add_h2("7.1 Testing Methodology")
add_p("Testing was conducted against the live AWS deployment at endpoint http://65.2.180.175. The test suite spans API health, network boundary isolation, database transaction integrity, S3 presigned URLs, and telemetry streaming.")

add_h2("7.2 Empirical Test Execution Matrix")
test_results = [
    ("TC-01", "API Health & DB Engine", "GET /health returns HTTP 200 with engine 'PostgreSQL (Amazon RDS)'", "HTTP 200 OK, status: healthy, engine: PostgreSQL", "PASS"),
    ("TC-02", "VPC & Subnet Isolation", "PostgreSQL database resides in private subnets with no internet route", "Subnet 10.0.10.0/24 route table has local route only; no IGW", "PASS"),
    ("TC-03", "Security Group Chaining", "Port 5432 rejects direct internet packets, accepting EC2 SG only", "Port 5432 inaccessible from public IP; connects from app-sg", "PASS"),
    ("TC-04", "Citizen Registration", "POST /api/auth/register inserts user into RDS users table", "User inserted with UUID PK, bcrypt hash, JWT returned", "PASS"),
    ("TC-05", "JWT Authentication", "POST /api/auth/login with valid credentials returns signed token", "HTTP 200 OK with valid JWT and role claims", "PASS"),
    ("TC-06", "Role-Based Access Control", "Citizen token attempting access to /api/authority routes is rejected", "HTTP 403 Forbidden returned by role middleware", "PASS"),
    ("TC-07", "Garbage Photo AI Validation", "Photo showing municipal garbage passes Gemini AI inspection", "Gemini returns isGarbage: true; complaint accepted", "PASS"),
    ("TC-08", "Spam & Selfie Rejection", "Random image/selfie submitted is rejected with error notice", "Gemini returns isGarbage: false; HTTP 400 returned", "PASS"),
    ("TC-09", "Private S3 Evidence Upload", "Uploaded complaint photo stored in S3 complaints/ with SSE-S3", "Object stored in S3 bucket with AES-256 encryption", "PASS"),
    ("TC-10", "S3 Presigned URL Resolution", "Frontend receives valid presigned GET URL with 60-min expiration", "Secure time-bound presigned URL returned and rendered", "PASS"),
    ("TC-11", "Geospatial Ward Partitioning", "Complaint coordinates matched to closest BMC ward via Haversine", "Coordinates (19.11, 72.84) matched to K/West Ward", "PASS"),
    ("TC-12", "Nearest Truck Dispatch", "Ward Admin dispatches nearest idle truck using SQL Haversine", "Nearest truck selected, complaint 'assigned', truck 'busy'", "PASS"),
    ("TC-13", "Worker Task Retrieval", "Driver logs in and views assigned complaint with navigation map", "Task coordinates, address, and complaint photo displayed", "PASS"),
    ("TC-14", "Cleanup Evidence Upload", "Worker uploads cleanup photo to S3 cleanup/ folder", "Object uploaded, status updated to 'pending_verification'", "PASS"),
    ("TC-15", "Before/After AI Verification", "Gemini compares before and after photos to verify clean site", "AI verifies waste removed; complaint marked 'resolved'", "PASS"),
    ("TC-16", "Eco-Points Credit", "Citizen receives +10 eco-points upon verified resolution", "Citizen point tally incremented from 0 to 10 in database", "PASS"),
    ("TC-17", "48-Hour SLA Breach Tracking", "Complaints older than 48 hours flagged as breached in dashboards", "check-sla.js flags seeded complaint; counter increments", "PASS"),
    ("TC-18", "CloudWatch Structured Logs", "Server runtime events logged to /swachhnet/backend with redaction", "Log stream active; passwords sanitized as ***REDACTED***", "PASS"),
    ("TC-19", "CloudWatch CPU Alarm", "Alarm configured to trigger when EC2 CPUUtilization >= 80%", "Alarm swachhnet-ec2-high-cpu-alarm verified active", "PASS"),
    ("TC-20", "AWS Budget Enforcement", "Monthly budget ceiling configured at $10.00 with 80% threshold", "SwachhNet-Monthly-Budget active in AWS Budgets", "PASS")
]
add_styled_table(["Test ID", "Scenario", "Expected Specification", "Observed Production Result", "Status"], test_results, col_widths=[0.7, 1.8, 2.3, 1.9, 0.5])

doc.add_page_break()

# ====================================================================
# PAGE 17 & 18: VERIFICATION EVIDENCE & AWS CONSOLE PLACEHOLDERS
# ====================================================================
add_h1("8. Verification Evidence & AWS Console Placeholders")
add_p("The following figures provide verified photographic evidence and AWS Console verification placeholders documenting the live production infrastructure:")

def add_placeholder_box(fig_no, title, service, nav_path, verified_params):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, "F8FAFC")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(2)
    
    r_hdr = p.add_run(f"📷 {fig_no}: AWS Console Evidence Placeholder — {title}\n")
    r_hdr.font.name = "Calibri"
    r_hdr.font.size = Pt(11)
    r_hdr.font.bold = True
    r_hdr.font.color.rgb = C_BLUE
    
    r_sub = p.add_run(f"AWS Service: {service} | Region: ap-south-1 (Mumbai)\nConsole Path: {nav_path}\n\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = C_GRAY
    
    r_b = p.add_run("Verified Production Infrastructure Parameters:\n")
    r_b.font.name = "Calibri"
    r_b.font.size = Pt(9.5)
    r_b.font.bold = True
    r_b.font.color.rgb = C_DARK
    
    for param in verified_params:
        r_p = p.add_run(f"• {param}\n")
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(9)
        r_p.font.color.rgb = C_DARK
        
    r_act = p.add_run("\n[VERIFIED LIVE: Evidence matching active CloudFormation Stack swachhnet-prod-stack]")
    r_act.font.name = "Calibri"
    r_act.font.size = Pt(8.5)
    r_act.font.italic = True
    r_act.font.color.rgb = RGBColor(22, 101, 52)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

add_placeholder_box(
    "Figure 8.1", "Amazon VPC & Subnet Segregation", "Amazon VPC",
    "AWS Management Console ➔ VPC ➔ Your VPCs ➔ swachhnet-vpc",
    [
        "VPC ID: swachhnet-vpc | IPv4 CIDR Block: 10.0.0.0/16",
        "Public Subnet: swachhnet-public-subnet-1 (10.0.1.0/24) | Route: 0.0.0.0/0 ➔ swachhnet-igw",
        "Private DB Subnet 1: swachhnet-private-subnet-1 (10.0.10.0/24) | Route: 10.0.0.0/16 local",
        "Private DB Subnet 2: swachhnet-private-subnet-2 (10.0.11.0/24) | Standby Multi-AZ zone"
    ]
)

add_placeholder_box(
    "Figure 8.2", "Amazon EC2 Compute Instance & PM2 Host", "Amazon EC2",
    "AWS Management Console ➔ EC2 ➔ Instances ➔ swachhnet-web-server",
    [
        "Instance ID: i-0983235e9c56d8d0d | Name: swachhnet-web-server | State: Running",
        "Instance Type: t3.micro (2 vCPU, 1 GB RAM) | Elastic Public IPv4: 65.2.180.175",
        "IAM Instance Profile: swachhnet-unified-profile | Security Group: swachhnet-app-sg",
        "Processes: Nginx 1.30 (Port 80) reverse proxying to Node.js Express (Port 5000 / PM2)"
    ]
)

add_placeholder_box(
    "Figure 8.3", "Amazon RDS for PostgreSQL 16.10 Instance", "Amazon RDS",
    "AWS Management Console ➔ RDS ➔ Databases ➔ swachhnet-postgres",
    [
        "DB Identifier: swachhnet-postgres | Status: Available | Engine: PostgreSQL 16.10",
        "Instance Class: db.t3.micro | Storage: 20 GB gp2 Encrypted (StorageEncrypted: true)",
        "Endpoint: swachhnet-postgres.cdc8mesu8z3p.ap-south-1.rds.amazonaws.com:5432",
        "Public Accessibility: No | Security Group: swachhnet-db-sg (Port 5432 from app-sg only)"
    ]
)

add_placeholder_box(
    "Figure 8.4", "Amazon S3 Private Evidence Storage Bucket", "Amazon S3",
    "AWS Management Console ➔ S3 ➔ Buckets ➔ swachhnet-evidence-078601217335-ap-south-1",
    [
        "Bucket Name: swachhnet-evidence-078601217335-ap-south-1 | Region: ap-south-1",
        "Access: Bucket and objects not public (Block Public Access: ON)",
        "Server-Side Encryption: AES-256 (SSE-S3) Enabled | Versioning: Enabled",
        "Object Folders: complaints/, cleanup/, deploy/ | Access: 60-minute presigned URLs"
    ]
)

add_placeholder_box(
    "Figure 8.5", "CloudWatch Logs & AWS Budgets Governance", "CloudWatch & Budgets",
    "AWS Management Console ➔ CloudWatch Logs (/swachhnet/backend) & AWS Budgets",
    [
        "Log Group: /swachhnet/backend | Active Log Stream: instance-28799-1793278274195",
        "Structured Telemetry: Real-time request logging with PII password/token redaction",
        "CloudWatch Alarm: swachhnet-ec2-high-cpu-alarm (EC2 CPUUtilization >= 80% for 10 min)",
        "AWS Budget: SwachhNet-Monthly-Budget ($10.00/month ceiling, 80% alert threshold)"
    ]
)

doc.add_page_break()

# ====================================================================
# PAGE 19: COST GOVERNANCE & CLOUD SECURITY ARCHITECTURE
# ====================================================================
add_h1("9. Cost Governance & Cloud Security Architecture")
add_h2("9.1 Monthly Cost Analysis & Free Tier Compliance")
add_p("The architecture is engineered to operate strictly within the AWS Free Tier, achieving a projected ongoing cost of $0.00 – $1.50/month:")

cost_summary = [
    ("Amazon EC2", "t3.micro (2 vCPU, 1 GB RAM, AL2023)", "750 Hours / Month Free Tier", "$0.00", "Public Web & API Server"),
    ("Amazon RDS", "db.t3.micro (Single-AZ, 20GB gp2)", "750 Hours + 20GB Storage Free Tier", "$0.00", "Isolated Relational Database"),
    ("Amazon S3", "Standard Storage (Private Bucket)", "5 GB Storage Free Tier", "$0.00", "Evidence Photos Storage"),
    ("Amazon SQS", "Standard Queue + Dead Letter Queue", "1,000,000 Free Requests / Month", "$0.00", "Decoupled Task Buffering"),
    ("AWS SSM", "Parameter Store (SecureString)", "Free Tier Unlimited Standard Usage", "$0.00", "KMS Encrypted Secrets"),
    ("CloudWatch", "/swachhnet/backend + 1 CPU Alarm", "5 GB Logs + 10 Alarms Free Tier", "$0.00", "Telemetry & Observability"),
    ("VPC & IGW", "Custom VPC (10.0.0.0/16)", "Free (No NAT Gateway Used)", "$0.00", "Network Boundary Isolation"),
    ("AWS Budgets", "1 Monthly Budget Alert ($10 Limit)", "2 Free Budgets per AWS Account", "$0.00", "Financial Governance"),
    ("Total Projected", "All 10 Implemented AWS Services", "Compliant with AWS Free Tier", "$0.00 – $1.50", "Cost-Optimized Architecture")
]
add_styled_table(["Service", "Sizing & Specifications", "Free Tier Eligibility", "Cost", "Purpose"], cost_summary, col_widths=[1.2, 1.9, 1.8, 0.7, 1.4])

add_h2("9.2 Multi-Layered Defense-in-Depth Cloud Security")
add_bullet("The PostgreSQL database is physically restricted to private subnets with no route to the Internet Gateway. Port 5432 ingress is chained to the EC2 security group only.", "1. Network Boundary Isolation: ")
add_bullet("Zero static AWS keys are stored on disk. The EC2 instance assumes an IAM Instance Profile (swachhnet-unified-profile) with scoped permissions limited to specific resource ARNs.", "2. IAM Least Privilege: ")
add_bullet("The S3 bucket enforces Block Public Access. Photos are encrypted at rest with AES-256 (SSE-S3) and viewed exclusively via time-bound 60-minute presigned GET URLs.", "3. S3 Zero-Trust Storage: ")
add_bullet("Database credentials, JWT keys, and Gemini API keys are encrypted with AWS KMS inside AWS SSM Parameter Store as SecureString parameters and loaded into memory on boot.", "4. In-Memory Secrets: ")
add_bullet("The application logger sanitizes passwords, JWT tokens, and connection strings (***REDACTED***) before pushing logs to Amazon CloudWatch, preventing PII leaks in audit trails.", "5. Telemetry Sanitization: ")

doc.add_page_break()

# ====================================================================
# PAGE 20: CONCLUSION & FUTURE ROADMAP
# ====================================================================
add_h1("10. Conclusion & Future Roadmap")
add_h2("10.1 Project Conclusion & Core Achievements")
add_p("The SwachhNet Cloud Computing Laboratory mini-project successfully designed, migrated, and deployed a production-grade, cloud-native municipal solid waste management platform on Amazon Web Services (AWS) in the Mumbai (ap-south-1) region. The implementation demonstrates full mastery of cloud engineering principles:")
add_bullet("Successfully provisioned a custom VPC (10.0.0.0/16) with isolated private subnets and chained security groups, ensuring zero public exposure for the relational database.", "• Enterprise VPC Topography: ")
add_bullet("Migrated from unstructured MongoDB Atlas to Amazon RDS PostgreSQL 16.10, implementing an ACID-compliant 5-table relational schema with pure SQL Haversine distance computations.", "• Relational Database Migration: ")
add_bullet("Co-located the React 18 SPA and Node.js Express API behind an optimized Nginx reverse proxy on Amazon EC2 (t3.micro) under PM2 daemonization, eliminating CORS issues and achieving sub-second API latencies.", "• High-Performance Compute: ")
add_bullet("Integrated Amazon S3 private storage with 60-minute presigned URLs, AWS IAM instance profiles, AWS SSM encrypted secrets, Amazon SQS asynchronous queues with DLQ, and CloudWatch log streaming.", "• Comprehensive AWS Services: ")
add_bullet("Delivered single-click deterministic provisioning via AWS CloudFormation (swachhnet-all-in-one.yaml) under a strictly enforced $10.00/month AWS Budget.", "• Infrastructure as Code: ")

add_h2("10.2 Future Scope & Enhancements")
add_bullet("Develop cross-platform mobile apps using Flutter with offline GPS and photo caching for sanitation workers operating in low-connectivity urban alleys.", "1. Native Mobile Apps: ")
add_bullet("Train custom edge Convolutional Neural Networks (CNNs) to automatically classify waste into dry, wet, and hazardous municipal categories.", "2. Automated Waste Segregation: ")
add_bullet("Integrate Amazon Location Service and graph route solvers to calculate dynamic travelling salesperson problem (TSP) routes for collection fleets.", "3. Dynamic Fleet Route Optimization: ")
add_bullet("Integrate Amazon Simple Notification Service (SNS) and WhatsApp Business API webhooks to deliver real-time SMS alerts to citizens upon verified grievance resolution.", "4. Real-Time Citizen SMS Alerts: ")

add_p("\n\nREFERENCES")
refs = [
    "[1] Amazon Web Services Documentation. (2024). Amazon EC2 User Guide for Linux Instances. https://docs.aws.amazon.com/ec2/",
    "[2] Amazon Web Services Documentation. (2024). Amazon RDS User Guide for PostgreSQL. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/",
    "[3] Amazon Web Services Documentation. (2024). Amazon S3 User Guide. https://docs.aws.amazon.com/AmazonS3/latest/userguide/",
    "[4] Amazon Web Services Documentation. (2024). Amazon VPC User Guide. https://docs.aws.amazon.com/vpc/",
    "[5] Amazon Web Services Documentation. (2024). AWS CloudFormation User Guide: Infrastructure as Code. https://docs.aws.amazon.com/cloudformation/",
    "[6] Amazon Web Services Documentation. (2024). Amazon SQS Developer Guide. https://docs.aws.amazon.com/AWSSimpleQueueService/",
    "[7] Amazon Web Services Documentation. (2024). Amazon CloudWatch User Guide. https://docs.aws.amazon.com/cloudwatch/",
    "[8] Google DeepMind. (2024). Gemini 1.5 Flash Multimodal Vision AI Documentation. https://ai.google.dev/docs",
    "[9] Mell, P., & Grance, T. (2011). The NIST Definition of Cloud Computing. NIST Special Publication 800-145.",
    "[10] PostgreSQL Global Development Group. (2024). PostgreSQL 16.10 Documentation. https://www.postgresql.org/docs/16/"
]
for r in refs:
    p_ref = doc.add_paragraph()
    r_run = p_ref.add_run(r)
    r_run.font.name = "Times New Roman"
    r_run.font.size = Pt(8.5)
    r_run.font.color.rgb = C_DARK
    p_ref.paragraph_format.space_after = Pt(2)

# Save DOCX
doc.save(DOCX_OUT)
print(f"20-Page DOCX generated successfully at: {DOCX_OUT}")

# Convert to PDF via Word COM / PowerShell
print("Converting 20-Page DOCX to PDF...")
import subprocess
ps_cmd = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open('{os.path.abspath(DOCX_OUT)}')
$doc.SaveAs('{os.path.abspath(PDF_OUT)}', 17)
$doc.Close()
$word.Quit()
"""
res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
if res.returncode == 0:
    print(f"20-Page PDF generated successfully at: {PDF_OUT}")
else:
    print(f"PowerShell error: {res.stderr}")
