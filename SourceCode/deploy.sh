#!/bin/bash

# Load environment variables from .env
set -a
source .env
set +a

RG="vulcan-rg"
LOCATION="eastus"
ACR="vulcanacr"
APP="vulcan-app"
ENV="vulcan-env"

echo "Creating resource group..."
az group create --name $RG --location $LOCATION

echo "Creating container app environment..."
az containerapp env create \
  --name $ENV \
  --resource-group $RG \
  --location $LOCATION

# Enable ACR admin for authentication
echo "Enabling ACR admin..."
az acr update -n $ACR --admin-enabled true

# Get ACR credentials
ACR_USERNAME=$(az acr credential show -n $ACR --query username -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR --query passwords[0].value -o tsv)

echo "Logging into ACR..."
az acr login --name $ACR

echo "Building Flask image..."
docker build -t $ACR.azurecr.io/vulcan-platform-dev:latest .

echo "Pushing Flask image..."
docker push $ACR.azurecr.io/vulcan-platform-dev:latest

echo "Deploying Flask container..."
az containerapp create \
  --name $APP \
  --resource-group $RG \
  --environment $ENV \
  --image $ACR.azurecr.io/vulcan-platform-dev:latest \
  --registry-login-server $ACR.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 --memory 1Gi \
  --env-vars DB_SERVER=mssql DB_USER=$DB_USER DB_PASS=$DB_PASS DB_NAME=$DB_NAME

echo "Adding MSSQL container..."
az containerapp revision set \
  --name $APP \
  --resource-group $RG \
  --containers '[
    {
      "name": "mssql",
      "image": "mcr.microsoft.com/azure-sql-edge",
      "cpu": 1,
      "memory": "2Gi",
      "env": [
        {"name": "SA_PASSWORD", "value": "'"$DB_PASS"'"},
        {"name": "ACCEPT_EULA", "value": "Y"},
        {"name": "MSSQL_PID", "value": "Developer"}
      ]
    }
  ]'

echo "Waiting for containers to be ready..."
# Loop until the app has a URL and all containers are ready
while true; do
    STATUS=$(az containerapp show \
      --name $APP \
      --resource-group $RG \
      --query "properties.provisioningState" -o tsv)
    
    READY=$(az containerapp show \
      --name $APP \
      --resource-group $RG \
      --query "properties.latestRevisionName" -o tsv)

    URL=$(az containerapp show \
      --name $APP \
      --resource-group $RG \
      --query properties.configuration.ingress.fqdn \
      --output tsv)
    
    if [[ "$STATUS" == "Succeeded" && -n "$URL" ]]; then
        echo "Containers are ready!"
        break
    else
        echo "Waiting for containers to start..."
        sleep 10
    fi
done

echo "----------------------------------------"
echo "🚀 Your app is live at:"
echo "https://$URL"
echo "----------------------------------------"