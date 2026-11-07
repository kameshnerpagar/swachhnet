# SwachhNet Cloud Deployment Guide

This guide describes how to deploy the **SwachhNet** platform to Amazon Web Services (AWS) using either the all-in-one CloudFormation template or modular templates.

---

## 1. Prerequisites

1. **AWS CLI v2** installed and configured:
   ```bash
   aws sts get-caller-identity
   ```
2. **Node.js 18+ and npm** installed locally for frontend builds and local testing.
3. **Google Gemini Flash API Key** (for vision validation).
4. **AWS Region:** Default region is `ap-south-1` (Mumbai).

---

## 2. Infrastructure Deployment (CloudFormation)

### Option A: Unified All-in-One Deployment (Recommended)
You can deploy the complete infrastructure (VPC, Subnets, SGs, IAM, S3, SQS, RDS, EC2, and CloudWatch) with a single command:

```bash
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/swachhnet-all-in-one.yaml \
  --stack-name swachhnet-prod-stack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
      EnvironmentName=swachhnet \
      DBMasterUserPassword=YourStrongPassword123! \
      InstanceType=t3.micro \
      DBInstanceClass=db.t3.micro \
  --region ap-south-1
```

### Option B: Modular Multi-Stack Deployment
If you prefer deploying step by step:

1. **Network Stack:**
   ```bash
   aws cloudformation deploy \
     --template-file infrastructure/cloudformation/01-networking.yaml \
     --stack-name swachhnet-network \
     --parameter-overrides EnvironmentName=swachhnet \
     --region ap-south-1
   ```
2. **Security & IAM Stack:**
   ```bash
   VPC_ID=$(aws cloudformation describe-stacks --stack-name swachhnet-network --query "Stacks[0].Outputs[?OutputKey=='VpcId'].OutputValue" --output text --region ap-south-1)

   aws cloudformation deploy \
     --template-file infrastructure/cloudformation/02-security-iam.yaml \
     --stack-name swachhnet-security \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameter-overrides EnvironmentName=swachhnet VpcId=$VPC_ID \
     --region ap-south-1
   ```
3. **Storage & SQS Stack:**
   ```bash
   aws cloudformation deploy \
     --template-file infrastructure/cloudformation/03-storage-sqs.yaml \
     --stack-name swachhnet-storage \
     --parameter-overrides EnvironmentName=swachhnet \
     --region ap-south-1
   ```
4. **Database Stack:**
   ```bash
   PRIV1=$(aws cloudformation describe-stacks --stack-name swachhnet-network --query "Stacks[0].Outputs[?OutputKey=='PrivateSubnet1Id'].OutputValue" --output text --region ap-south-1)
   PRIV2=$(aws cloudformation describe-stacks --stack-name swachhnet-network --query "Stacks[0].Outputs[?OutputKey=='PrivateSubnet2Id'].OutputValue" --output text --region ap-south-1)
   DBSG=$(aws cloudformation describe-stacks --stack-name swachhnet-security --query "Stacks[0].Outputs[?OutputKey=='DatabaseSecurityGroupId'].OutputValue" --output text --region ap-south-1)

   aws cloudformation deploy \
     --template-file infrastructure/cloudformation/04-database.yaml \
     --stack-name swachhnet-database \
     --parameter-overrides \
         EnvironmentName=swachhnet \
         PrivateSubnet1Id=$PRIV1 \
         PrivateSubnet2Id=$PRIV2 \
         DatabaseSecurityGroupId=$DBSG \
         DBMasterUserPassword=YourStrongPassword123! \
     --region ap-south-1
   ```
5. **Compute & Monitoring Stack:**
   ```bash
   PUBSUB=$(aws cloudformation describe-stacks --stack-name swachhnet-network --query "Stacks[0].Outputs[?OutputKey=='PublicSubnetId'].OutputValue" --output text --region ap-south-1)
   APPSG=$(aws cloudformation describe-stacks --stack-name swachhnet-security --query "Stacks[0].Outputs[?OutputKey=='AppSecurityGroupId'].OutputValue" --output text --region ap-south-1)
   PROFILE=$(aws cloudformation describe-stacks --stack-name swachhnet-security --query "Stacks[0].Outputs[?OutputKey=='EC2InstanceProfileName'].OutputValue" --output text --region ap-south-1)

   aws cloudformation deploy \
     --template-file infrastructure/cloudformation/05-compute.yaml \
     --stack-name swachhnet-compute \
     --parameter-overrides \
         EnvironmentName=swachhnet \
         PublicSubnetId=$PUBSUB \
         AppSecurityGroupId=$APPSG \
         EC2InstanceProfileName=$PROFILE \
     --region ap-south-1
   ```

---

## 3. Configure Parameter Store Secrets

Populate the required secrets securely in AWS Systems Manager Parameter Store:

```bash
# 1. Database URL
aws ssm put-parameter \
  --name "/swachhnet/prod/DATABASE_URL" \
  --type "SecureString" \
  --value "postgresql://swachhnet_admin:YourStrongPassword123!@<RDS_ENDPOINT>:5432/swachhnet" \
  --overwrite \
  --region ap-south-1

# 2. JWT Secret
aws ssm put-parameter \
  --name "/swachhnet/prod/JWT_SECRET" \
  --type "SecureString" \
  --value "b3f71c45d2908f7e6514ac4592e3157b89d412e84c9876f103d29a47b192ec54" \
  --overwrite \
  --region ap-south-1

# 3. Google Gemini API Key
aws ssm put-parameter \
  --name "/swachhnet/prod/G_API" \
  --type "SecureString" \
  --value "AIzaSyYourGeminiApiKeyHere" \
  --overwrite \
  --region ap-south-1

# 4. S3 Bucket Name & SQS Queue URL
aws ssm put-parameter \
  --name "/swachhnet/prod/S3_BUCKET_NAME" \
  --type "String" \
  --value "<EVIDENCE_BUCKET_NAME>" \
  --overwrite \
  --region ap-south-1

aws ssm put-parameter \
  --name "/swachhnet/prod/SQS_QUEUE_URL" \
  --type "String" \
  --value "<JOBS_QUEUE_URL>" \
  --overwrite \
  --region ap-south-1
```

---

## 4. Application Deployment on EC2

1. **Connect to EC2 using AWS Systems Manager Session Manager:**
   ```bash
   aws ssm start-session --target <EC2_INSTANCE_ID> --region ap-south-1
   ```
2. **Switch to root and clone application code:**
   ```bash
   sudo su -
   mkdir -p /var/www/swachhnet
   cd /var/www/swachhnet
   git clone <YOUR_REPOSITORY_URL> .
   ```
3. **Build Frontend:**
   ```bash
   cd /var/www/swachhnet/frontend
   npm install
   npm run build
   # Assets output to /var/www/swachhnet/frontend/dist
   ```
4. **Setup Backend & Run Database Migrations/Seed:**
   ```bash
   cd /var/www/swachhnet/backend
   npm install --production

   # Configure production environment flag to use SSM
   cat << 'EOF' > .env
   PORT=5000
   NODE_ENV=production
   USE_SSM=true
   ENABLE_CLOUDWATCH_LOGS=true
   CLOUDWATCH_LOG_GROUP=/swachhnet/backend
   EOF

   # Run PostgreSQL schema migration & seed data
   node db/seed.js
   ```
5. **Start Application with PM2:**
   ```bash
   pm2 start server.js --name "swachhnet-api"
   pm2 startup systemd
   pm2 save
   ```
6. **Verify Nginx and Health Check:**
   ```bash
   curl http://localhost/health
   ```
   Open `http://<EC2_PUBLIC_IP>` in your web browser.

---

## 5. Rollback and Cleanup Instructions

To prevent ongoing AWS charges when the project evaluation is finished:

```bash
# Delete CloudFormation stack (deletes VPC, EC2, RDS, and SGs)
aws cloudformation delete-stack --stack-name swachhnet-prod-stack --region ap-south-1

# Empty and delete S3 bucket if objects were created
aws s3 rm s3://<EVIDENCE_BUCKET_NAME> --recursive
aws s3 rb s3://<EVIDENCE_BUCKET_NAME> --force

# Remove SSM parameters
aws ssm delete-parameters --names \
  "/swachhnet/prod/DATABASE_URL" \
  "/swachhnet/prod/JWT_SECRET" \
  "/swachhnet/prod/G_API" \
  "/swachhnet/prod/S3_BUCKET_NAME" \
  "/swachhnet/prod/SQS_QUEUE_URL" \
  --region ap-south-1
```

