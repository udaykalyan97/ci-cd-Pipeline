import boto3
import json
import time
import os

# AWS Credentials
def set_aws_credentials(access_key, secret_key, region):
    os.environ["AWS_ACCESS_KEY_ID"] = access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key
    os.environ["AWS_DEFAULT_REGION"] = region
    print("✅ AWS credentials set for this session.")


# AWS Configurations
AWS_REGION = "us-east-1"
BUCKET_NAME = "bucket-name"
CLOUDFRONT_COMMENT = "Static Website CloudFront Distribution"

# Create AWS clients
s3_client = boto3.client('s3', region_name=AWS_REGION)
cf_client = boto3.client('cloudfront', region_name=AWS_REGION)

def create_s3_bucket():
    print(f"Creating S3 bucket: {BUCKET_NAME}")
    s3_client.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
    )
    print("Bucket created successfully.")

def configure_static_website():
    print(f"Configuring {BUCKET_NAME} for static website hosting...")
    s3_client.put_bucket_website(
        Bucket=BUCKET_NAME,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'index.html'}
        }
    )
    print("Static website hosting configured.")

def set_bucket_policy_public():
    print("Setting bucket policy to allow public read access...")
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
        }]
    }
    s3_client.put_bucket_policy(
        Bucket=BUCKET_NAME,
        Policy=json.dumps(policy)
    )
    print("Bucket policy applied.")

def create_cloudfront_distribution():
    print("Creating CloudFront distribution...")
    response = cf_client.create_distribution(
        DistributionConfig={
            'CallerReference': str(time.time()),
            'Comment': CLOUDFRONT_COMMENT,
            'Enabled': True,
            'Origins': [{
                'Id': BUCKET_NAME,
                'DomainName': f"{BUCKET_NAME}.s3.amazonaws.com",
                'S3OriginConfig': {
                    'OriginAccessIdentity': ''
                }
            }],
            'DefaultCacheBehavior': {
                'TargetOriginId': BUCKET_NAME,
                'ViewerProtocolPolicy': 'redirect-to-https',
                'AllowedMethods': {
                    'Quantity': 2,
                    'Items': ['GET', 'HEAD']
                },
                'ForwardedValues': {
                    'QueryString': False,
                    'Cookies': {'Forward': 'none'}
                }
            },
            'ViewerCertificate': {
                'CloudFrontDefaultCertificate': True
            },
            'DefaultRootObject': 'index.html'
        }
    )
    distribution_id = response['Distribution']['Id']
    domain_name = response['Distribution']['DomainName']
    print(f"CloudFront Distribution created!\nID: {distribution_id}\nDomain Name: {domain_name}")
    return distribution_id, domain_name

if __name__ == "__main__":

    # Set credentials before making any boto3 calls
    set_aws_credentials(
        access_key="YOUR_ACCESS_KEY",
        secret_key="YOUR_SECRET_KEY",
        region=AWS_REGION
    )

    create_s3_bucket()
    configure_static_website()
    set_bucket_policy_public()
    distribution_id, domain_name = create_cloudfront_distribution()
    print("\n\n✅ Setup complete!")
    print(f"👉 CloudFront Domain: https://{domain_name}")
    print(f"👉 S3 Bucket Static Website URL: http://{BUCKET_NAME}.s3-website-{AWS_REGION}.amazonaws.com/")
