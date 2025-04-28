# Full CI/CD Automation for AWS & Azure DevOps

This repository automates the process of creating AWS infrastructure (S3 + CloudFront) and setting up an Azure DevOps pipeline for continuous integration and deployment (CI/CD).

## Prerequisites

- Python 3.x
- AWS CLI configured
- Azure CLI logged in
- Python dependencies: `boto3`, `requests`

## File Structure

/main-folder/ 
    ├── create_aws_infra.py      
    ├── create_azure_pipeline.py
    ├── setup.sh # Bash script to run Python scripts 
    ├── templates/ # Folder with YAML template 
    │ └── azure-pipelines.yml 
    └── requirements.txt 

## Running the Scripts

1. Install dependencies:

```bash
pip install -r requirements.txt
```

Make setup.sh executable:

```bash
chmod +x setup.sh
```
Run the setup:

```bash
./setup.sh
```

This will:

Create the AWS infrastructure (S3 + CloudFront).

Set up the Azure DevOps pipeline.

Azure DevOps Pipeline YAML
The azure-pipelines.yml defines a CI/CD pipeline that:

Builds and tests a React app.

Uploads build artifacts to an AWS S3 bucket.