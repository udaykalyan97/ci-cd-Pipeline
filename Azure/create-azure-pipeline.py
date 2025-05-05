import requests
import json
import base64

# ============ Configuration ============
# Azure DevOps organization URL
organization_url = 'https://dev.azure.com/{organization_name}/'  # Replace with your org name

# Personal Access Token (PAT) for Azure DevOps
pat_token = 'your_personal_access_token_here'

# Repository settings
repository_type = "AzureReposGit"   # or "GitHub" if using GitHub
repository_name = "your-project-name/your-repository-name"
repository_url = "https://dev.azure.com/{organization_name}/your-project-name/_git/your-repository-name"

branch_name = "refs/heads/main"  # default branch you want to trigger pipeline on
yaml_file_path = "templates/azure-pipelines.yml"  # path inside your repo

# Pipeline name
pipeline_name = "CI-CD-Pipeline"

# ========================================

# Encode the PAT for Basic Auth
encoded_pat = base64.b64encode(f":{pat_token}".encode()).decode()

# Define headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_pat}'
}

# Define pipeline body
pipeline_body = {
    "name": pipeline_name,
    "configuration": {
        "type": "yaml",
        "path": yaml_file_path,
        "repository": {
            "type": repository_type,
            "name": repository_name,
            "url": repository_url,
            "defaultBranch": branch_name
        }
    }
}

# Azure DevOps API URL to create pipeline
api_url = f'{organization_url}_apis/pipelines?api-version=7.0'

# Make POST request to create the pipeline
response = requests.post(api_url, headers=headers, data=json.dumps(pipeline_body))

# Check the response
if response.status_code in [200, 201]:
    pipeline_id = response.json()['id']
    print(f"✅ Pipeline created successfully! Pipeline ID: {pipeline_id}")
else:
    print(f"❌ Error creating pipeline: {response.status_code} - {response.text}")
