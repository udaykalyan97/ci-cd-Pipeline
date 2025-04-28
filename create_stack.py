# create_stack.py

import boto3
from botocore.exceptions import ClientError, WaiterError

# Import color functions
from utils.colors import print_success, print_info, print_warning, print_error, print_bold

print_bold("\n🚀 Starting CloudFormation Stack Creation Script...\n")

# Create a CloudFormation client
cf = boto3.client('cloudformation')

# Read the CloudFormation template
try:
    with open('pipeline.yml', 'r') as file:
        template_body = file.read()
    print_success("✅ Successfully read 'pipeline.yml'.")
except FileNotFoundError:
    print_error("❌ Error: 'pipeline.yml' file not found.")
    exit(1)

try:
    # Try to create the stack
    print_info("📦 Creating stack 'frontend-pipeline'...")
    response = cf.create_stack(
        StackName='frontend-pipeline',
        TemplateBody=template_body,
        Parameters=[
            {
                'ParameterKey': 'GitHubOAuthToken',
                'ParameterValue': 'your-github-oauth-token'
            },
        ],
        Capabilities=['CAPABILITY_NAMED_IAM']  # Needed if your template creates IAM roles
    )
    print_success("✅ Stack creation initiated.")

    # Wait for the stack to complete
    print_info("⏳ Waiting for stack creation to complete (this may take a few minutes)...")
    waiter = cf.get_waiter('stack_create_complete')
    waiter.wait(StackName='frontend-pipeline')

    print_success("\n🎉 Stack created successfully!")

except ClientError as e:
    print_error("\n❌ ClientError occurred during stack creation:")
    print_warning(e.response['Error']['Message'])
    exit(1)

except WaiterError as e:
    print_error("\n❌ Stack creation failed or timed out:")
    print_warning(str(e))
    exit(1)

except Exception as e:
    print_error("\n❗ Unexpected error occurred:")
    print_warning(str(e))
    exit(1)
