#!/bin/bash

set -e  # Exit immediately if a command exits with non-zero status
set -o pipefail  # Catch errors in piped commands

# === Step 0: Print starting message ===
echo "🚀 Starting full setup automation..."

# === Step 1: Create AWS Infrastructure ===
echo "🔧 Running AWS infrastructure creation script..."
python3 create_aws_infra.py

echo "✅ AWS infrastructure created successfully."

# === Step 2: Create Azure DevOps Pipeline ===
echo "🔧 Running Azure DevOps pipeline creation script..."
python3 create-azure-pipeline.py

echo "✅ Azure DevOps pipeline created successfully."

# === Step 3: Done ===
echo "🎉 All setup done successfully!"
