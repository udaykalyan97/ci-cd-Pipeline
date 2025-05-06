#!/bin/bash

# Set the LocalStack endpoint URL
awslocal_ENDPOINT=http://localhost:4566  

# Start LocalStack if it's not running
if ! docker ps | grep -q "localstack/localstack"; then
  echo "Starting LocalStack..."
  docker run -d -p 4566:4566 localstack/localstack
  sleep 10  # Wait for LocalStack to start up
else
  echo "LocalStack is already running."
fi

# Create an S3 bucket in LocalStack
BUCKET_NAME="hosted-bucket"
echo "Creating S3 bucket '$BUCKET_NAME'..."
awslocal s3 mb s3://$BUCKET_NAME

# List of YAML files to upload
YAML_FILES=("main.yaml" "ec2.yaml" "s3.yaml" "rds-postgres.yaml" "cloudfront.yaml" "route53.yaml" "lambda.yaml")

# Upload all the YAML files to the S3 bucket
for FILE in "${YAML_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo "Uploading '$FILE' to the bucket '$BUCKET_NAME'..."
    awslocal s3 cp "$FILE" s3://$BUCKET_NAME/
  else
    echo "File '$FILE' not found, skipping upload."
  fi
done

# Verify the upload
echo "Verifying the upload..."
awslocal s3 ls s3://$BUCKET_NAME/

# Output the S3 URLs for the uploaded YAML files
echo "The following files have been uploaded to S3://$BUCKET_NAME/:"
for FILE in "${YAML_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo "s3://$BUCKET_NAME/$FILE"
  fi
done


# Create CloudFormation Stack
for env in dev staging uat prod; do
  awslocal cloudformation create-stack \
    --stack-name "my-main-stack-${env}" \
    --template-url "http://hosted-bucket.s3.localhost.localstack.cloud:4566/main.yaml" \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
    --parameters ParameterKey=Environment,ParameterValue=${env}
done


echo "CloudFormation stack creation initiated."
sleep 8  # Allow time for stack creation

# Describe stacks and show created resources
for env in dev staging uat prod; do
  echo -e "\nResources for 'my-main-stack-${env}':"
  awslocal cloudformation describe-stack-resources --stack-name "my-main-stack-${env}" | jq
done