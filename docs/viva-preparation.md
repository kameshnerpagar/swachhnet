# SwachhNet Viva Preparation & Technical Defense Guide

This guide equips you with simple, concise, and technically accurate answers to defend **SwachhNet** in your Cloud Computing Lab (CCL) oral examination and project review.

---

## 1. Project Summary Pitch (1-Minute Opening)
> *"Respected faculty, SwachhNet is an enterprise cloud-native municipal solid waste management and dispatch platform designed around Mumbai’s BMC administrative ward structure. 
> 
> Citizens submit photo evidence of garbage dumps with GPS coordinates, which are verified by Google Gemini AI and routed to the nearest ward office using spherical geospatial calculations. Ward admins dispatch the closest idle truck, and upon cleanup, sanitation workers upload proof verified by multi-modal AI. 
> 
> To demonstrate production cloud principles, the entire platform is deployed on AWS inside a custom VPC with public and private subnets. We host the application on Amazon EC2 with an Nginx reverse proxy, store relational data securely in an isolated Amazon RDS PostgreSQL instance, store photos in a private Amazon S3 bucket using short-lived presigned URLs, queue background events via Amazon SQS, manage secrets using AWS SSM Parameter Store, monitor system health with Amazon CloudWatch alarms, and automate all provisioning using AWS CloudFormation."*

---

## 2. Frequently Asked Technical Viva Questions

### Q1: Why did you use a custom VPC instead of the Default VPC?
**Answer:** The Default VPC places all subnets directly on the public internet with an Internet Gateway route. For production security, database instances must never be exposed to public IP addresses. Our custom VPC (`10.0.0.0/16`) creates:
1. A **Public Subnet** for the EC2 web server.
2. Two **Private Subnets** spanning two Availability Zones strictly for the Amazon RDS PostgreSQL instance, ensuring the database has zero public internet exposure.

---

### Q2: How did you implement database security without a NAT Gateway?
**Answer:** A NAT Gateway costs around \$32/month, which is unnecessarily expensive for a student lab. We designed a dual security group layer:
* `AppSecurityGroup` allows inbound HTTP/HTTPS (80/443) and outbound internet to reach external APIs.
* `DatabaseSecurityGroup` allows inbound port 5432 **strictly** from `AppSecurityGroup` by security group reference ID. `0.0.0.0/0` is completely blocked.
* The EC2 instance connects directly to the private RDS endpoint over internal VPC routing without needing a NAT Gateway.

---

### Q3: Why did you migrate from MongoDB to Amazon RDS PostgreSQL?
**Answer:** MongoDB Atlas was an external third-party NoSQL database. For an enterprise cloud project:
1. Municipal operations (users, wards, trucks, complaints, transfers) are inherently relational and require ACID transaction guarantees.
2. Amazon RDS provides automated backups, encryption at rest with AWS KMS, point-in-time recovery, and multi-AZ support.
3. We reimplemented MongoDB’s `$near` geospatial query using PostgreSQL’s spherical Haversine trigonometric formula, calculating accurate geodesic distances between complaints, ward offices, and garbage trucks directly in SQL.

---

### Q4: How does the Haversine formula work in PostgreSQL?
**Answer:** The Haversine formula determines the great-circle distance between two points on a sphere given their longitudes and latitudes:
$$\text{distance} = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$
In our SQL query, we compute this with Earth radius $R = 6371\text{ km}$, ordering by distance in ascending order to find the nearest ward or idle truck. This runs natively on any PostgreSQL instance without requiring external extensions.

---

### Q5: Why are citizen complaint photos stored in a private S3 bucket instead of being public?
**Answer:** Making S3 buckets public is a major security vulnerability that causes data leaks. 
* In SwachhNet, all public access is blocked (`BlockPublicAcls: true`, `IgnorePublicAcls: true`, etc.).
* Only the EC2 instance's IAM role has permission to read and write objects.
* When the client frontend needs to display an image, the backend generates an **Amazon S3 Presigned URL** valid for 1 hour. After 1 hour, the URL expires automatically, preventing unauthorized hotlinking or scraping.

---

### Q6: What is the purpose of AWS Systems Manager (SSM) Parameter Store?
**Answer:** Storing database passwords and JWT secrets in plaintext `.env` files or Git repositories is bad security practice. 
* We store configuration under the path `/swachhnet/prod/*` using **SecureString** encryption backed by AWS Key Management Service (KMS).
* On startup, the backend retrieves these parameters through its attached EC2 IAM instance profile (`AmazonSSMManagedInstanceCore`), keeping secrets out of the codebase.

---

### Q7: Why did you choose Amazon EC2 over a completely serverless (Lambda) architecture?
**Answer:** 
1. **Flat, Predictable Cost:** An EC2 `t3.micro` instance is 100% free under the AWS 12-month Free Tier (750 hours/month), avoiding unexpected request-based API Gateway and Lambda costs.
2. **Zero Cold Starts:** Lambda functions experience cold-start latency (1-3 seconds) on initial invocation, whereas Express with PM2 remains hot in memory.
3. **Nginx Reverse Proxy:** Nginx efficiently serves the pre-built React 18 production bundle from disk and proxies `/api` calls locally with sub-20ms latency.
4. **Integrated SQS Worker:** The background queue consumer runs alongside the backend on the same instance, reducing architectural overhead.

---

### Q8: What role does Amazon SQS play in SwachhNet?
**Answer:** Amazon SQS provides asynchronous message decoupling. When an admin dispatches a truck or resolves a ticket, downstream operations (such as simulated SMS notifications to the driver and SLA audit logging) are pushed to `swachhnet-jobs-queue`.
* This prevents slow downstream network calls from blocking the client’s HTTP response.
* If processing fails, the message visibility timeout expires, and after 5 failed attempts, the message moves to `swachhnet-jobs-dlq` (Dead-Letter Queue) for inspection.

---

### Q9: How is Amazon CloudWatch configured?
**Answer:** CloudWatch provides two critical operational capabilities:
1. **Application Logging:** Express and security events are sanitized (masking passwords and bearer tokens) and streamed to CloudWatch Log Group `/swachhnet/backend`.
2. **Infrastructure Alarms:** A CloudWatch Alarm (`swachhnet-ec2-high-cpu-alarm`) monitors instance `CPUUtilization`. If CPU usage exceeds 80% for two consecutive 5-minute evaluation periods, the alarm state changes to `ALARM`.

---

### Q10: How does AWS CloudFormation benefit this project?
**Answer:** CloudFormation provides **Infrastructure as Code (IaC)**. Instead of manually clicking through the AWS Console, the entire architecture (VPC, subnets, route tables, security groups, IAM roles, S3 buckets, SQS queues, RDS instance, and EC2 instance) is defined declaratively in YAML templates. 
* This prevents configuration drift.
* Allows one-click reproduction of the environment in any AWS region or account.
* Enables clean teardown via `aws cloudformation delete-stack` to avoid student cloud costs.

---

### Q11: How is the 48-hour SLA breach calculated?
**Answer:** In municipal operations, complaints must be resolved within 48 hours. Our backend runs a periodic check or query:
```sql
SELECT * FROM complaints 
WHERE status NOT IN ('resolved', 'rejected') 
AND created_at < NOW() - INTERVAL '48 HOURS';
```
Any complaint exceeding 48 hours is highlighted in red with an alert badge on both the Ward Admin and Central Superadmin dashboards.

