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
ARCH_DIR = os.path.join(REPORT_DIR, "architecture")
SHOTS_DIR = os.path.join(REPORT_DIR, "screenshots")
DOCX_PATH = os.path.join(REPORT_DIR, "SwachhNet_CCL_Project_Report.docx")
PDF_PATH = os.path.join(REPORT_DIR, "SwachhNet_CCL_Project_Report.pdf")

sys.path.append(REPORT_DIR)
import report_content as rc
import chapters_1_to_3 as c13
import chapters_4_to_6 as c46
import chapters_7_to_10 as c710

doc = docx.Document()

# -------------------------------------------------------------
# Page Setup: A4, 1-inch margins
# -------------------------------------------------------------
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colors
C_NAVY = RGBColor(30, 58, 138)      # #1e3a8a
C_DARK = RGBColor(15, 23, 42)      # #0f172a
C_GRAY = RGBColor(71, 85, 105)     # #475569
C_BLUE = RGBColor(37, 99, 235)     # #2563eb

def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
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
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = C_NAVY
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(12)
    return p

def add_h1(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = C_NAVY
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = C_BLUE
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    return p

def add_h3(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = C_DARK
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    return p

def add_p(text, italic=False, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11.5)
    run.font.color.rgb = C_DARK
    run.italic = italic
    run.bold = bold
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    return p

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = C_DARK
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.font.color.rgb = C_DARK
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    return p

def add_code(text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_shading(cell, "F1F5F9")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text.strip())
    run.font.name = "Courier New"
    run.font.size = Pt(9.0)
    run.font.color.rgb = RGBColor(15, 23, 42)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(0)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_figure(img_path, caption_text, width_inches=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(10)
        run_cap.font.bold = True
        run_cap.font.color.rgb = C_GRAY
        p_cap.paragraph_format.space_after = Pt(12)
    else:
        p = doc.add_paragraph(f"[Image: {caption_text}]")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def add_styled_table(headers, rows, col_widths=None):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.style = 'Table Grid'
    
    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_shading(hdr_cells[i], "1E3A8A")
        set_cell_margins(hdr_cells[i], top=90, bottom=90, left=100, right=100)
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
            set_cell_margins(row_cells[c_idx], top=70, bottom=70, left=90, right=90)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(9.0)
            p.runs[0].font.color.rgb = C_DARK
            
    if col_widths:
        for r in tbl.rows:
            for i, w in enumerate(col_widths):
                r.cells[i].width = Inches(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return tbl

print("Generating Document Structure...")

# =============================================================
# 1. COVER PAGE
# =============================================================
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_inst = p_inst.add_run(rc.COVER_PAGE_DATA["institution"] + "\n" + rc.COVER_PAGE_DATA["department"])
r_inst.font.name = "Calibri"
r_inst.font.size = Pt(14)
r_inst.font.bold = True
r_inst.font.color.rgb = C_DARK
p_inst.paragraph_format.space_before = Pt(36)
p_inst.paragraph_format.space_after = Pt(24)

p_crse = doc.add_paragraph()
p_crse.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_crse = p_crse.add_run("A MINI PROJECT REPORT ON\n" + rc.COVER_PAGE_DATA["course"])
r_crse.font.name = "Calibri"
r_crse.font.size = Pt(12)
r_crse.font.color.rgb = C_GRAY
p_crse.paragraph_format.space_after = Pt(36)

p_t = doc.add_paragraph()
p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_t = p_t.add_run(rc.COVER_PAGE_DATA["title"])
r_t.font.name = "Calibri"
r_t.font.size = Pt(24)
r_t.font.bold = True
r_t.font.color.rgb = C_NAVY
p_t.paragraph_format.space_after = Pt(12)

p_st = doc.add_paragraph()
p_st.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_st = p_st.add_run(rc.COVER_PAGE_DATA["subtitle"])
r_st.font.name = "Calibri"
r_st.font.size = Pt(13)
r_st.font.italic = True
r_st.font.color.rgb = C_BLUE
p_st.paragraph_format.space_after = Pt(48)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_sub = p_sub.add_run("Submitted in partial fulfillment of the requirements for the award of the degree of\n" + rc.COVER_PAGE_DATA["degree"])
r_sub.font.name = "Times New Roman"
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = C_DARK
p_sub.paragraph_format.space_after = Pt(36)

# Students Table
t_std = doc.add_table(rows=1, cols=2)
t_std.alignment = WD_TABLE_ALIGNMENT.CENTER
t_std.rows[0].cells[0].paragraphs[0].text = "SUBMITTED BY:\n" + rc.COVER_PAGE_DATA["students"][0]["name"] + " (" + rc.COVER_PAGE_DATA["students"][0]["roll"] + ")\n" + rc.COVER_PAGE_DATA["students"][1]["name"] + " (" + rc.COVER_PAGE_DATA["students"][1]["roll"] + ")"
t_std.rows[0].cells[1].paragraphs[0].text = "UNDER THE GUIDANCE OF:\n" + rc.COVER_PAGE_DATA["guide"] + "\n" + rc.COVER_PAGE_DATA["guide_desig"]
for c in t_std.rows[0].cells:
    c.paragraphs[0].runs[0].font.name = "Calibri"
    c.paragraphs[0].runs[0].font.size = Pt(10.5)
    c.paragraphs[0].runs[0].font.color.rgb = C_DARK

p_yr = doc.add_paragraph()
p_yr.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_yr = p_yr.add_run("\n\n" + rc.COVER_PAGE_DATA["academic_year"] + "\n" + rc.COVER_PAGE_DATA["location"])
r_yr.font.name = "Calibri"
r_yr.font.size = Pt(11)
r_yr.font.bold = True
r_yr.font.color.rgb = C_GRAY

doc.add_page_break()

# =============================================================
# 2. PRELIMINARY PAGES
# =============================================================
add_title("CERTIFICATE")
add_p(rc.CERTIFICATE_TEXT)
add_p("\n\n\n")

# Signatures Table
tbl_sig = doc.add_table(rows=1, cols=3)
tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_sig.rows[0].cells[0].paragraphs[0].text = "____________________\nProf. [GUIDE NAME]\nProject Guide"
tbl_sig.rows[0].cells[1].paragraphs[0].text = "____________________\nDr. [HOD NAME]\nHead of Department"
tbl_sig.rows[0].cells[2].paragraphs[0].text = "____________________\nExternal Examiner\nCollege Seal"
for c in tbl_sig.rows[0].cells:
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].font.name = "Calibri"
    p.runs[0].font.size = Pt(10)

doc.add_page_break()

add_title("DECLARATION")
add_p(rc.DECLARATION_TEXT)
add_p("\n\nDate: 30th October 2026\nPlace: Mumbai\n\n")
p_decl_sig = doc.add_paragraph()
p_decl_sig.add_run("Kamesh Nerpagar (Roll No: [ROLL NO. 1])\n[STUDENT 2 NAME] (Roll No: [ROLL NO. 2])")

doc.add_page_break()

add_title("ACKNOWLEDGEMENT")
add_p(rc.ACKNOWLEDGEMENT_TEXT)

doc.add_page_break()

add_title("ABSTRACT")
add_p(rc.ABSTRACT_TEXT)

doc.add_page_break()

add_title("TABLE OF CONTENTS")
for ch_title, sections in rc.TABLE_OF_CONTENTS:
    p_ch = doc.add_paragraph()
    r = p_ch.add_run(ch_title)
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = C_NAVY
    p_ch.paragraph_format.space_before = Pt(6)
    p_ch.paragraph_format.space_after = Pt(2)
    for sec in sections:
        p_sec = doc.add_paragraph()
        p_sec.paragraph_format.left_indent = Inches(0.25)
        p_sec.paragraph_format.space_after = Pt(2)
        r_sec = p_sec.add_run(sec)
        r_sec.font.name = "Times New Roman"
        r_sec.font.size = Pt(10.5)

doc.add_page_break()

add_title("LIST OF ABBREVIATIONS")
add_styled_table(["Abbreviation", "Expanded Description"], rc.ABBREVIATIONS, col_widths=[2.0, 4.2])

doc.add_page_break()

# =============================================================
# CHAPTER 1: INTRODUCTION
# =============================================================
add_h1("Chapter 1: Introduction")
for sec_title, paragraphs in c13.CH1_SECTIONS:
    add_h2(sec_title)
    for p in paragraphs:
        add_p(p)

doc.add_page_break()

# =============================================================
# CHAPTER 2: LITERATURE REVIEW & TECHNOLOGY OVERVIEW
# =============================================================
add_h1("Chapter 2: Literature Review & Technology Overview")
add_p("This chapter examines the state of modern cloud architectures and delivers an exhaustive evaluation of each technology component deployed within the SwachhNet platform.")
for tech in c13.CH2_TECH:
    add_h2(tech["name"])
    add_p(f"Description & Architecture: {tech['what']}")
    add_p(f"Justification for Selection: {tech['why']}")
    add_p(f"Specific Implementation Role in SwachhNet: {tech['role']}")

doc.add_page_break()

# =============================================================
# CHAPTER 3: SYSTEM ANALYSIS & REQUIREMENTS
# =============================================================
add_h1("Chapter 3: System Analysis & Requirements")
add_h2("3.1 Functional Requirements")
add_p("Table 3.1 enumerates the complete functional requirements implemented and verified within the SwachhNet cloud platform:")
add_styled_table(["Req ID", "Feature Area", "Specification & Behavioral Details", "Priority"], c13.FUNC_REQ_TABLE, col_widths=[0.8, 1.8, 3.2, 0.7])

add_h2("3.2 Non-Functional Requirements")
add_p("Table 3.2 outlines the quality attributes, performance targets, and cloud availability metrics:")
add_styled_table(["NFR ID", "Quality Dimension", "Engineering Specification", "Verification Mechanism"], c13.NON_FUNC_REQ_TABLE, col_widths=[0.8, 1.6, 2.6, 1.5])

add_h2("3.3 User Roles & Privilege Matrix")
add_p("Table 3.3 defines the four operational roles and their specific application privileges:")
add_styled_table(["User Persona / Role", "Permitted Operations & Administrative Capabilities", "Assigned View"], c13.USER_ROLES_TABLE, col_widths=[1.5, 3.3, 1.7])

add_h2("3.4 Feasibility Study")
add_bullet("Evaluated against AWS Free Tier services and Node.js/PostgreSQL open-source ecosystems. Verified zero-dependency hardware constraints and 100% cloud reproducibility.", "Technical Feasibility: ")
add_bullet("Project operates under a $0.00 estimated monthly run rate by remaining inside AWS Free Tier limits (750 hours t3.micro EC2, 750 hours db.t3.micro RDS, 5GB S3). Backed by an active $10.00 budget ceiling.", "Economic Feasibility: ")
add_bullet("Aligns directly with BMC's administrative 24-ward municipal workflow. No specialized training required for citizens; field drivers receive simple map navigation pins.", "Operational Feasibility: ")

doc.add_page_break()

# =============================================================
# CHAPTER 4: SYSTEM ARCHITECTURE & DESIGN
# =============================================================
add_h1("Chapter 4: System Architecture & Design")

for sec_title, paragraphs in c46.CH4_CONTENT.items():
    add_h2(sec_title)
    for p in paragraphs:
        add_p(p)
        
    # Embed appropriate diagrams
    if "4.1" in sec_title:
        add_figure(os.path.join(ARCH_DIR, "Figure_4_1_Overall_Architecture.png"), "Figure 4.1: SwachhNet - Comprehensive AWS Cloud Architecture")
    elif "4.2" in sec_title:
        add_figure(os.path.join(ARCH_DIR, "Figure_4_2_VPC_Network.png"), "Figure 4.2: Amazon VPC Network & Security Group Isolation Architecture")
    elif "4.3" in sec_title:
        add_figure(os.path.join(ARCH_DIR, "Figure_4_3_App_Architecture.png"), "Figure 4.3: SwachhNet Multi-Tier Layered Software Architecture")
    elif "4.4" in sec_title:
        add_figure(os.path.join(ARCH_DIR, "Figure_4_4_Database_ERD.png"), "Figure 4.4: Relational PostgreSQL Database Entity-Relationship Diagram (ERD)")
    elif "4.5" in sec_title:
        add_figure(os.path.join(ARCH_DIR, "Figure_4_5_Use_Case.png"), "Figure 4.5: UML Use Case Diagram for SwachhNet Municipal Roles")
    elif "4.6" in sec_title:
        add_figure(os.path.join(ARCH_DIR, "Figure_4_6_DFD_Level_0.png"), "Figure 4.6: Level 0 Data Flow Diagram (Context Diagram)")
        add_figure(os.path.join(ARCH_DIR, "Figure_4_7_DFD_Level_1.png"), "Figure 4.7: Level 1 Data Flow Diagram (DFD) - Decomposed Subsystems")
    elif "4.7" in sec_title:
        add_figure(os.path.join(ARCH_DIR, "Figure_4_8_Citizen_Complaint_Workflow.png"), "Figure 4.8: End-to-End Citizen Complaint Resolution Workflow")
        add_figure(os.path.join(ARCH_DIR, "Figure_4_9_Truck_Dispatch_Workflow.png"), "Figure 4.9: Geospatial Haversine Nearest Truck Dispatch Workflow")
        add_figure(os.path.join(ARCH_DIR, "Figure_4_10_Cleanup_Verification_Workflow.png"), "Figure 4.10: Before & After Photographic Cleanup Verification Workflow")
        add_figure(os.path.join(ARCH_DIR, "Figure_4_11_SLA_Monitoring_Workflow.png"), "Figure 4.11: 48-Hour Municipal Service Level Agreement (SLA) Monitoring")

doc.add_page_break()

# =============================================================
# CHAPTER 5: AWS CLOUD SERVICES INTEGRATION
# =============================================================
add_h1("Chapter 5: AWS Cloud Services Integration")
add_p("To fulfill the rigorous curriculum criteria established for the Cloud Computing Laboratory (CCL) mini-project, SwachhNet integrates ten distinct Amazon Web Services across all six mandatory infrastructure domains and implements two advanced cloud capabilities (Amazon SQS and AWS CloudFormation). Table 5.1 provides the comprehensive mapping:")

add_styled_table(["AWS Service", "Technical Role in SwachhNet", "Integration Points", "Infrastructure Domain", "Verification Source"], c46.AWS_SERVICES_TABLE, col_widths=[1.2, 1.8, 1.6, 1.1, 1.3])

add_h2("5.1 Compliance with the Mandatory Six Cloud Areas")
add_bullet("Amazon EC2 (t3.micro - Amazon Linux 2023) operating Nginx 1.30 and Node.js 18 under PM2. Fully integrated with systemd auto-restart and Elastic IP 65.2.180.175.", "1. Compute: ")
add_bullet("Custom Amazon VPC (10.0.0.0/16) featuring public subnets (10.0.1.0/24) with an Internet Gateway, private subnets (10.0.10.0/24, 10.0.11.0/24) across 2 AZs, and custom security groups.", "2. Networking: ")
add_bullet("Amazon RDS for PostgreSQL 16.10 (db.t3.micro, 20GB gp2 encrypted). Complete relational migration with UUID keys, B-tree indexes, and zero direct public internet exposure.", "3. Database: ")
add_bullet("Private Amazon S3 bucket (swachhnet-evidence-078601217335-ap-south-1) with AES-256 SSE encryption, versioning, and secure 60-minute presigned GET URLs.", "4. Storage: ")
add_bullet("AWS IAM EC2 Instance Profile (swachhnet-unified-profile) with least-privilege inline permissions; AWS Systems Manager Parameter Store SecureString encryption.", "5. Security & IAM: ")
add_bullet("Amazon CloudWatch log streaming (/swachhnet/backend) with structured PII redaction and EC2 CPU utilization alarm; AWS Budgets financial ceiling ($10.00/month).", "6. Monitoring & Budget: ")

add_h2("5.2 Implementation of Additional Cloud Capabilities")
add_bullet("Amazon SQS Standard Queue (swachhnet-jobs-queue) and Dead Letter Queue (swachhnet-jobs-dlq) with a 5-retry threshold for durable, decoupled background task execution.", "Capability 1 (Asynchronous Messaging): ")
add_bullet("AWS CloudFormation declarative master template (swachhnet-all-in-one.yaml) automating the deterministic creation of all 24 resources in a single command.", "Capability 2 (Infrastructure as Code): ")

doc.add_page_break()

# =============================================================
# CHAPTER 6: IMPLEMENTATION & WORKING
# =============================================================
add_h1("Chapter 6: Implementation & Working")
add_p("This chapter documents the actual source code implementations governing the SwachhNet platform, highlighting key controllers, services, and cloud integrations.")

add_h2("6.1 Application Entry Point & Dual-Database Bootstrap")
add_p("The backend bootstrap script (server.js) dynamically detects the database environment, loading credentials from AWS SSM Parameter Store and initializing PostgreSQL pool connections:")
add_code(c46.CODE_SNIPPETS["server_bootstrap"])

add_h2("6.2 Amazon S3 Direct Upload & Presigned URL Resolution")
add_p("Binary evidence images are uploaded directly from memory buffers to private S3 buckets using AWS SDK v3, generating cryptographic presigned URLs for client viewing:")
add_code(c46.CODE_SNIPPETS["s3_presigned"])

add_h2("6.3 Geospatial Haversine Nearest Truck Dispatch Engine")
add_p("Ward administrators dispatch the closest idle municipal truck through an atomic SQL transaction utilizing the Haversine trigonometric formula:")
add_code(c46.CODE_SNIPPETS["haversine_dispatch"])

add_h2("6.4 Google Gemini Multimodal AI Verification")
add_p("Uploaded camera captures undergo automated vision prompt analysis using Google Gemini Flash to eliminate non-garbage spam submissions:")
add_code(c46.CODE_SNIPPETS["gemini_verification"])

add_h2("6.5 CloudWatch Structured Logging & PII Sanitization")
add_p("All runtime operations are logged as structured JSON payloads to Amazon CloudWatch Logs with automated regex sanitization of passwords and tokens:")
add_code(c46.CODE_SNIPPETS["cloudwatch_logger"])

doc.add_page_break()

# =============================================================
# CHAPTER 7: DEPLOYMENT & CONFIGURATION
# =============================================================
add_h1("Chapter 7: Deployment & Configuration")
add_p("The deployment of SwachhNet was conducted using a reproducible, multi-phase cloud automation pipeline:")

for step_title, step_desc in c710.CH7_STEPS:
    add_h2(step_title)
    add_p(step_desc)

add_h2("7.1 Nginx Reverse Proxy Configuration")
add_p("The production Nginx configuration (/etc/nginx/conf.d/swachhnet.conf) routes web traffic and forwards API calls to the internal Node.js process:")
add_code("""server {
    listen 80 default_server;
    server_name _;

    # Serve built React Single Page Application
    location / {
        root /var/www/swachhnet/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to Node.js backend on port 5000
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
    }
}""")

doc.add_page_break()

# =============================================================
# CHAPTER 8: TESTING & RESULTS
# =============================================================
add_h1("Chapter 8: Testing & Results")
add_p("The deployed SwachhNet platform underwent comprehensive empirical verification across functional, security, database, and cloud infrastructure requirements. Table 8.1 documents the 20 verified test cases:")

add_styled_table(["Test ID", "Test Scenario", "Expected Result Specification", "Empirical Observed Result", "Status"], c710.TEST_CASES_TABLE, col_widths=[0.8, 1.8, 2.2, 1.9, 0.6])

add_h2("8.1 Cloud Evidence & Console Verification Gallery")
add_p("The following figures provide verified photographic evidence and AWS Console verification placeholders documenting the live production infrastructure:")

add_figure(os.path.join(SHOTS_DIR, "screenshot_01_user_registration_ui.png"), "Figure 8.1: Live Citizen Registration Interface (React 18 Frontend)")
add_figure(os.path.join(SHOTS_DIR, "screenshot_02_aws_vpc_console.png"), "Figure 8.2: Amazon VPC Console Verification (swachhnet-vpc 10.0.0.0/16)")
add_figure(os.path.join(SHOTS_DIR, "screenshot_03_aws_security_groups_console.png"), "Figure 8.3: Security Groups Ingress Rules Verification (App & DB SG)")
add_figure(os.path.join(SHOTS_DIR, "screenshot_04_aws_rds_console.png"), "Figure 8.4: Amazon RDS PostgreSQL Database Instance (Private Subnet)")
add_figure(os.path.join(SHOTS_DIR, "screenshot_05_aws_s3_console.png"), "Figure 8.5: Amazon S3 Private Evidence Storage Bucket")
add_figure(os.path.join(SHOTS_DIR, "screenshot_06_aws_cloudwatch_console.png"), "Figure 8.6: Amazon CloudWatch Log Group (/swachhnet/backend)")
add_figure(os.path.join(SHOTS_DIR, "screenshot_08_aws_budgets_console.png"), "Figure 8.7: AWS Budgets $10.00 Monthly Cost Governance Control")
add_figure(os.path.join(SHOTS_DIR, "screenshot_09_aws_cloudformation_console.png"), "Figure 8.8: AWS CloudFormation Master Stack (CREATE_COMPLETE)")

doc.add_page_break()

# =============================================================
# CHAPTER 9: COST ANALYSIS & CLOUD SECURITY
# =============================================================
add_h1("Chapter 9: Cost Analysis & Cloud Security")
add_h2("9.1 Monthly Cloud Cost Breakdown")
add_p("Table 9.1 details the estimated monthly operational expenditures across all deployed AWS services based on the AWS Asia Pacific (Mumbai) region pricing model:")

add_styled_table(["AWS Resource", "Provisioned Sizing & Specifications", "AWS Free Tier Eligibility", "Monthly Cost", "Operational Purpose"], c710.COST_TABLE, col_widths=[1.3, 2.0, 1.6, 0.8, 1.5])

add_h2("9.2 Defense-in-Depth Cloud Security Architecture")
add_bullet("The RDS database is physically isolated in private subnets with zero internet gateway associations. Port 5432 ingress is cryptographically restricted to packets arriving from the EC2 application security group.", "1. Network Segmentation: ")
add_bullet("All static access keys were eliminated from configuration files. The EC2 instance assumes an IAM role with scoped, least-privilege permissions limited to specific resource ARNs.", "2. IAM Least Privilege: ")
add_bullet("All S3 buckets enforce Block Public Access (Acls, Policies). Objects are encrypted at rest using AES-256 SSE. Images are accessed exclusively via 60-minute presigned URLs.", "3. Object Storage Security: ")
add_bullet("Sensitive credentials reside in AWS SSM Parameter Store as SecureString parameters encrypted with AWS KMS. Plain-text secrets never touch version control repositories.", "4. Secrets Encryption: ")
add_bullet("The application logger automatically scrubs passwords, JWT tokens, and database URIs before streaming logs to Amazon CloudWatch, preventing PII leaks in audit trails.", "5. Telemetry Sanitization: ")

doc.add_page_break()

# =============================================================
# CHAPTER 10: CONCLUSION & FUTURE SCOPE
# =============================================================
add_h1("Chapter 10: Conclusion & Future Scope")
add_h2("10.1 Project Summary & Achievements")
add_p("The SwachhNet Cloud Computing Laboratory mini-project successfully re-architected, migrated, and deployed a production-grade, cloud-native municipal waste management platform on Amazon Web Services (AWS). All primary academic and technical objectives were met with distinction:")
add_bullet("Provisioned an enterprise VPC with dual-AZ private subnet isolation and zero database public exposure in the Mumbai (ap-south-1) region.", "• Secure Networking: ")
add_bullet("Successfully migrated unstructured MongoDB collections into a robust, ACID-compliant relational schema on Amazon RDS PostgreSQL 16.10 with Haversine spatial math.", "• Relational Migration: ")
add_bullet("Achieved sub-second response times by co-locating the built React 18 SPA and Express API behind an optimized Nginx reverse proxy on Amazon EC2 (t3.micro) under PM2 daemonization.", "• High-Performance Compute: ")
add_bullet("Fully integrated Amazon S3 presigned URLs, AWS IAM instance profiles, AWS SSM encrypted secrets, Amazon SQS background queues, and CloudWatch log streaming.", "• Comprehensive Cloud Services: ")
add_bullet("Accomplished single-command infrastructure provisioning via AWS CloudFormation, ensuring 100% deterministic reproducibility under a $10.00/month budget ceiling.", "• Infrastructure as Code: ")

add_h2("10.2 Future Scope & Enhancements")
add_bullet("Develop cross-platform Flutter/React Native mobile applications with offline GPS caching for field sanitation drivers in low-connectivity zones.", "1. Native Mobile Apps: ")
add_bullet("Train specialized edge convolutional neural networks (CNNs) to classify waste into biodegradable, recyclable, and hazardous municipal categories.", "2. Automated Waste Segregation: ")
add_bullet("Integrate Amazon Location Service and graph route solvers to compute dynamic travelling salesperson problem (TSP) routes for collection fleets.", "3. Dynamic Fleet Route Optimization: ")
add_bullet("Integrate Amazon SNS and WhatsApp Business API webhooks to deliver instantaneous SMS and messaging updates to citizens upon complaint resolution.", "4. Automated Citizen Notifications: ")

doc.add_page_break()

# =============================================================
# REFERENCES
# =============================================================
add_title("REFERENCES")
add_p("The following authoritative academic and technical references were consulted and cited in the design, cloud deployment, and documentation of SwachhNet:")
for ref_id, citation in c710.REFERENCES:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(f"[{ref_id}]  {citation}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.color.rgb = C_DARK

# Save DOCX
doc.save(DOCX_PATH)
print(f"DOCX successfully generated at: {DOCX_PATH}")

# Convert to PDF via Word COM Automation
print("Converting DOCX to PDF via Microsoft Word COM automation...")
try:
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc_word = word.Documents.Open(os.path.abspath(DOCX_PATH))
    doc_word.SaveAs(os.path.abspath(PDF_PATH), FileFormat=17)
    doc_word.Close()
    word.Quit()
    print(f"PDF successfully generated at: {PDF_PATH}")
except Exception as e:
    print(f"Word COM error: {e}. Attempting PowerShell Word conversion...")
    import subprocess
    ps_cmd = f"""
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open('{os.path.abspath(DOCX_PATH)}')
    $doc.SaveAs('{os.path.abspath(PDF_PATH)}', 17)
    $doc.Close()
    $word.Quit()
    """
    res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"PowerShell Word COM PDF successfully generated at: {PDF_PATH}")
    else:
        print(f"PowerShell conversion output: {res.stdout}\nError: {res.stderr}")
