#!/bin/bash

# Step 1: Create the S3 Bucket
aws s3api create-bucket --bucket hosted-bucket --region us-east-1 --create-bucket-configuration LocationConstraint=us-east-1

# Step 2: Upload YAML Files to S3 Bucket
aws s3 cp ./s3.yaml s3://hosted-bucket/
aws s3 cp ./ec2.yaml s3://hosted-bucket/
aws s3 cp ./rds-postgres.yaml s3://hosted-bucket/
aws s3 cp ./lambda.yaml s3://hosted-bucket/
aws s3 cp ./cloudfront.yaml s3://hosted-bucket/
aws s3 cp ./route53.yaml s3://hosted-bucket/

# Step 3: Create CloudFormation Stack
aws cloudformation create-stack --stack-name my-main-stack --template-url https://hosted-bucket.s3.amazonaws.com/main.yaml --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND

echo "CloudFormation Stack creation initiated."