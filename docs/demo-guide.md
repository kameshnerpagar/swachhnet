# SwachhNet End-to-End Demonstration Script

Follow this step-by-step demonstration script to present SwachhNet to faculty, lab evaluators, and external examiners.

---

## 1. Demo Credentials Reference

All test accounts use the universal password: **`password123`**

| Role | Email | Demonstration Purpose |
|---|---|---|
| **Citizen** | `user@test.com` | Report garbage, test AI spam rejection, view map, earn points & badges. |
| **Ward Admin (Malad)** | `p_north@bmc.gov.in` | View ward tickets, auto-assign nearest truck, inspect cleanup evidence. |
| **Ward Admin (Borivali)** | `r_central@bmc.gov.in` | Receive inter-ward transferred complaints. |
| **Sanitation Worker** | `driver1@test.com` | View assigned route, upload "After" cleanup photo, verify with AI. |
| **Central Authority** | `central@swachhnet.com` | Monitor 8 BMC wards, city-wide resolution rate, and 48-hour SLA breaches. |

---

## 2. Step-by-Step Live Demo Flow

### Step 1: Citizen Complaint Submission & AI Validation
1. Open the application URL in your browser (`http://<EC2_PUBLIC_IP>`).
2. Log in as Citizen: `user@test.com` / `password123`.
3. Click **"File a Report"**:
   * Allow geolocation or click on the interactive Leaflet map (e.g., select Malad at `19.1860, 72.8480`).
   * Notice that the system automatically detects the nearest ward office: **P/North Ward (Malad)** using spherical Haversine math.
4. **Test AI Spam Detection:**
   * Upload an arbitrary photo (e.g. a car, portrait, or classroom).
   * Submit &rarr; The application calls Google Gemini Flash vision.
   * **Result:** Alert appears: *"AI Validation Failed: No garbage or waste detected in this image. Please upload a valid photo."*
5. **Submit Valid Complaint:**
   * Upload an image showing trash/litter.
   * Submit &rarr; Complaint is uploaded to private S3, saved in RDS PostgreSQL, and +10 reward points are credited to the citizen.
   * Citizen dashboard displays the new ticket in **"Open"** status.

---

### Step 2: Ward Authority Review & Nearest Truck Dispatch
1. Log out and log in as Ward Admin: `p_north@bmc.gov.in` / `password123`.
2. Notice the dashboard shows only complaints within **P/North Ward (Malad)**.
3. Click **"Auto-Assign Truck"** on the new ticket:
   * Backend executes a PostgreSQL query calculating the spherical distance between the complaint and all idle trucks in the Malad garage fleet.
   * Assigns the closest idle driver (e.g., `MH-04-WD-1009`), updates status to **"Assigned"**, and marks the truck as **"Busy"**.
   * An asynchronous dispatch job is enqueued to Amazon SQS (`swachhnet-jobs-queue`).

---

### Step 3: Sanitation Worker Cleanup & AI Multi-Modal Verification
1. Log out and log in as Worker Driver: `driver1@test.com` / `password123`.
2. The driver dashboard displays the assigned complaint location and the citizen's "Before" photo.
3. Worker completes cleanup and clicks **"Upload Proof"**:
   * Selects an "After" photo showing the clean street.
   * **Multi-Modal AI Execution:** Gemini AI receives BOTH the Before and After image buffers, comparing them to verify the garbage has been cleared.
   * **Result:** Image is stored in S3, status updates to **"Pending Verification"**, and the truck status resets to **"Idle"**.

---

### Step 4: Admin Verification & Citizen Gamification
1. Switch back to Ward Admin (`p_north@bmc.gov.in`).
2. View the complaint card showing the side-by-side **Before** and **After** photos loaded securely via Amazon S3 presigned URLs.
3. Click **"Verify & Resolve"** &rarr; Ticket marked **"Resolved"**.
4. Log back in as Citizen (`user@test.com`):
   * Points increase to 80 pts.
   * Level progresses (e.g., from *Newcomer* to *Reporter*).
   * Badge unlocked: *"Impact Maker"* or *"City Cleaner"*.
   * Citizen submits a 5-star rating and feedback for the ward authority.

---

### Step 5: Central Authority & 48-Hour SLA Breach Monitoring
1. Log in as Central Commissioner: `central@swachhnet.com` / `password123`.
2. Navigate to **Central Authority Dashboard**:
   * Inspect city-wide totals: Total Wards (8), Total Complaints, Total Resolved.
   * View the **48-Hour SLA Breach Panel**: highlights the pre-seeded complaint filed 3 days ago that breached the municipal turnaround window.
   * Demonstrates municipal accountability and operational governance.

---

## 3. Showing AWS Cloud Architecture to Evaluators

Keep these AWS Console tabs open during your evaluation:

1. **Amazon EC2:**
   * Show running instance `swachhnet-web-server` with public IPv4.
   * Show Nginx listening on port 80 and PM2 process in terminal:
     ```bash
     pm2 list
     ```
2. **Amazon RDS:**
   * Show `swachhnet-postgres` in `Available` status.
   * Highlight **"Publicly Accessible: No"** and explain that the DB is safely secluded inside private subnets.
3. **Amazon S3:**
   * Open `swachhnet-evidence-...` bucket.
   * Show `complaints/` and `cleanup/` prefixes holding the uploaded photos.
   * Highlight **"Block all public access: On"** and demonstrate that clicking the raw object URL yields `403 Access Denied`.
4. **Amazon CloudWatch:**
   * Open `/swachhnet/backend` log group.
   * Show live log entries with timestamps, HTTP status codes, and sanitized credentials (`***REDACTED***`).
   * Show the `swachhnet-ec2-high-cpu-alarm` in `OK` state.
5. **Amazon SQS:**
   * Open `swachhnet-jobs-queue` and `swachhnet-jobs-dlq`.
   * Show the queue attributes and messages processed.

