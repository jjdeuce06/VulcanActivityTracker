#!/bin/bash

# Load environment variables
set -a
source .env
set +a

RG="vulcan-rg"
ACR="vulcanacr"
LOCATION="eastus"

echo "Checking if ACR '$ACR' exists..."
EXISTS=$(az acr show --name $ACR --resource-group $RG --query "name" -o tsv 2>/dev/null)

if [ "$EXISTS" == "$ACR" ]; then
    echo "✅ ACR '$ACR' already exists."
else
    echo "Creating Azure Container Registry '$ACR'..."
    az acr create --resource-group $RG --name $ACR --sku Basic --location $LOCATION
    echo "✅ ACR created."
fi

echo "Enabling admin access for ACR..."
az acr update -n $ACR --admin-enabled true

# Fetch credentials
ACR_USERNAME=$(az acr credential show -n $ACR --query username -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR --query passwords[0].value -o tsv)

echo "----------------------------------------"
echo "Use the following to login Docker to ACR:"
echo "docker login $ACR.azurecr.io -u $ACR_USERNAME -p <password>"
echo "Password: $ACR_PASSWORD"
echo "----------------------------------------"
echo "✅ ACR setup complete. You can now run deploy.sh."