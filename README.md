
# AWS Resource Automation with CloudFormation

This repository automates the creation of AWS resources using **AWS CloudFormation**. It includes steps for:
1. Creating an **S3 bucket** to host the CloudFormation templates.
2. Uploading the YAML files to the S3 bucket.
3. Triggering a CloudFormation stack creation that will provision the following resources:
   - **EC2**
   - **S3**
   - **RDS**
   - **Lambda**
   - **CloudFront**
   - **Route53**

## Prerequisites

Before running the script, make sure you have the following installed:

- **AWS CLI**: Make sure it's configured with access to your AWS account.
  - To install, follow the [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
  - Configure AWS CLI with `aws configure`.

- **IAM Permissions**: Ensure that your AWS IAM user has the necessary permissions to create S3 buckets, CloudFormation stacks, and the resources listed above.

---

## Steps

1. **Clone this repository** to your local machine:
   ```bash
   git clone https://github.com/udaykalyan97/ci-cd-Pipeline.git
   cd ci-cd-Pipeline/cloud-formation/
   ```

2. **Prepare YAML Files**:
   Make sure that the following YAML files are present in the directory:
   - `s3.yaml` – Template for creating S3 resources.
   - `ec2.yaml` – Template for creating EC2 resources.
   - `rds-postgres.yaml` – Template for creating RDS (PostgreSQL) resources.
   - `lambda.yaml` – Template for creating Lambda resources.
   - `cloudfront.yaml` – Template for creating CloudFront resources.
   - `route53.yaml` – Template for creating Route53 resources.
   - `main.yaml` – Master template that references all other templates from the S3 bucket.

3. **Make the Script Executable**:
   The script `deploy_resources.sh` automates the entire process. Make sure it's executable:
   ```bash
   chmod +x deploy_resources.sh
   ```

4. **Run the Script**:
   Run the script to create the S3 bucket, upload YAML files to it, and trigger the CloudFormation stack creation:
   ```bash
   ./deploy_resources.sh
   ```

---

## What the Script Does

The script performs the following tasks:

1. **Creates an S3 Bucket** (`hosted-bucket`) to host the YAML files for CloudFormation stacks:
   ```bash
   aws s3api create-bucket --bucket hosted-bucket --region us-east-1 --create-bucket-configuration LocationConstraint=us-east-1
   ```

2. **Uploads YAML Files** to the `hosted-bucket`:
   ```bash
   aws s3 cp ./s3.yaml s3://hosted-bucket/
   aws s3 cp ./ec2.yaml s3://hosted-bucket/
   aws s3 cp ./rds-postgres.yaml s3://hosted-bucket/
   aws s3 cp ./lambda.yaml s3://hosted-bucket/
   aws s3 cp ./cloudfront.yaml s3://hosted-bucket/
   aws s3 cp ./route53.yaml s3://hosted-bucket/
   ```

3. **Creates the CloudFormation Stack** using `main.yaml`, which references the uploaded templates to provision the resources:
   ```bash
   aws cloudformation create-stack --stack-name my-main-stack --template-url https://hosted-bucket.s3.amazonaws.com/main.yaml --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
   ```

---

## CloudFormation Resources Created

- **S3 Bucket**: hosted-bucket (for YAML file hosting).
- **EC2 Instances**: Defined in `ec2.yaml`.
- **RDS**: PostgreSQL RDS instance as defined in `rds-postgres.yaml`.
- **Lambda Functions**: Defined in `lambda.yaml`.
- **CloudFront Distribution**: As defined in `cloudfront.yaml`.
- **Route 53**: Hosted Zones and DNS records defined in `route53.yaml`.

The `main.yaml` file is the master template that creates these resources by referencing the other templates hosted in the S3 bucket.

---

## Verifying the Stack

To verify that the stack and resources were created successfully:

### Check CloudFormation Stack:
Run the following command to see the status of the stack:
```bash
aws cloudformation describe-stacks --stack-name my-main-stack
```

### Verify Individual Resources:
- **EC2**: `aws ec2 describe-instances`
- **S3**: `aws s3 ls`
- **RDS**: `aws rds describe-db-instances`
- **Lambda**: `aws lambda list-functions`
- **CloudFront**: `aws cloudfront list-distributions`
- **Route53**: `aws route53 list-hosted-zones`

---

## Cleanup

To clean up the resources created by the CloudFormation stack, you can delete the stack:
```bash
aws cloudformation delete-stack --stack-name my-main-stack
```
This will delete all the resources associated with the stack.

---

## Troubleshooting

- If the `aws s3api create-bucket` command fails, ensure that the S3 bucket name is globally unique.
- If CloudFormation stack creation fails, check the error message for resource-specific issues. You can describe the stack to get more details:
  ```bash
  aws cloudformation describe-stack-events --stack-name my-main-stack
  ```

---

## License
This project is licensed under the MIT License – see the LICENSE file for details.
