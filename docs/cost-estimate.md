# SwachhNet Cloud Cost Estimation & Budget Management

## 1. AWS Region & Pricing Context
* **Region:** Asia Pacific (Mumbai) — `ap-south-1`
* **Currency:** USD (\$)
* **Target Audience:** Engineering student / Academic mini-project with limited cloud credits.

---

## 2. Monthly Cost Breakdown by Service

| Service | Configuration / Specification | Free Tier Allowance | Estimated Monthly Cost (Free Tier Eligible) | Estimated Monthly Cost (Without Free Tier) |
|---|---|---|---|---|
| **Amazon EC2** | 1 × `t3.micro` Linux (2 vCPU, 1 GB RAM, 20 GB gp3 root) | 750 hrs/month `t2.micro` or `t3.micro` for 12 months | **\$0.00** | ~\$7.50 / month |
| **Amazon RDS** | 1 × `db.t3.micro` PostgreSQL (Single-AZ, 20 GB gp3) | 750 hrs/month Single-AZ `db.t3.micro` for 12 months | **\$0.00** | ~\$13.50 / month |
| **Amazon S3** | Standard Storage (~500 MB photo evidence) | 5 GB storage, 20,000 GET, 2,000 PUT for 12 months | **\$0.00** | ~\$0.02 / month |
| **Amazon SQS** | Standard Queue + DLQ (~5,000 messages) | 1,000,000 messages/month (Always Free) | **\$0.00** | **\$0.00** |
| **Amazon CloudWatch**| 1 Log Group (~200 MB logs) + 1 Alarm | 5 GB log ingestion + 10 metrics/alarms (Always Free) | **\$0.00** | ~\$0.10 / month |
| **AWS Systems Manager**| 5 Standard Parameters (SecureString) | Standard parameters are free (Always Free) | **\$0.00** | **\$0.00** |
| **Amazon VPC** | Custom VPC, Subnets, Route Tables, IGW | No hourly charge for standard VPC components | **\$0.00** | **\$0.00** |
| **Total Estimated Cost**| | | **\$0.00 / month** | **~\$21.12 / month** |

---

## 3. Potential Hidden or Idle Charges (Important Considerations)

1. **IPv4 Address Charges:** AWS charges \$0.005/hour per in-use public IPv4 address (~~\$3.60/month). To avoid this after your demonstration, stop or terminate the EC2 instance.
2. **NAT Gateway:** A NAT Gateway costs ~\$0.045/hour plus data processing (~~\$32.40/month). **SwachhNet intentionally avoids a NAT Gateway**, keeping PostgreSQL completely isolated in private subnets and running the web app on EC2 with direct public internet access.
3. **Multi-AZ RDS:** Multi-AZ doubles RDS hourly costs and storage charges. SwachhNet uses Single-AZ to strictly adhere to student budget constraints.

---

## 4. AWS Budget Configuration ($10 Alert Threshold)

To ensure no unexpected charges occur during your lab semester:

### Creating the Budget via AWS CLI
```bash
aws budgets create-budget \
  --account-id $(aws sts get-caller-identity --query "Account" --output text) \
  --budget '{
    "BudgetName": "SwachhNet-Monthly-Budget",
    "BudgetLimit": {
      "Amount": "10.00",
      "Unit": "USD"
    },
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[
    {
      "Notification": {
        "NotificationType": "ACTUAL",
        "ComparisonOperator": "GREATER_THAN",
        "Threshold": 80.0,
        "ThresholdType": "PERCENTAGE"
      },
      "Subscribers": [
        {
          "SubscriptionType": "EMAIL",
          "Address": "your-email@example.com"
        }
      ]
    }
  ]'
```

### Checking Actual Billing in Console
1. Log in to AWS Management Console.
2. Search for **Billing and Cost Management**.
3. View **Bills** &rarr; **Charges by service** to see exact hour-by-hour consumption.
4. Always shut down instances or delete CloudFormation stacks after completing your viva presentation.

