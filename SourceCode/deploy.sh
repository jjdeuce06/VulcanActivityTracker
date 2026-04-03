#!/bin/bash

# Load environment variables from .env
set -a
source .env
set +a

RG="vulcan-rg"
LOCATION="eastus"
ACR="vulcanacr"
FLASK_APP="vulcan-flask"
MSSQL_APP="vulcan-mssql"
ENV="vulcan-env"

# Create resource group
echo "Creating resource group..."
az group create --name $RG --location $LOCATION

# Create Container Apps environment
echo "Creating container app environment..."
az containerapp env create \
  --name $ENV \
  --resource-group $RG \
  --location $LOCATION

# Enable ACR admin for login
echo "Enabling ACR admin..."
az acr update -n $ACR --admin-enabled true

# Get ACR credentials
ACR_USERNAME=$(az acr credential show -n $ACR --query username -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR --query passwords[0].value -o tsv)

# Login to ACR
echo "Logging into ACR..."
az acr login --name $ACR

# Build and push Flask image
echo "Building Flask image..."
docker build -t $ACR.azurecr.io/vulcan-platform-dev:latest .
echo "Pushing Flask image..."
docker push $ACR.azurecr.io/vulcan-platform-dev:latest

# Deploy MSSQL container first
echo "Deploying MSSQL container..."
az containerapp create \
  --name $MSSQL_APP \
  --resource-group $RG \
  --environment $ENV \
  --image mcr.microsoft.com/azure-sql-edge \
  --cpu 1 --memory 2Gi \
  --env-vars SA_PASSWORD=$DB_PASS ACCEPT_EULA=Y MSSQL_PID=Developer \
  --ingress internal

# Wait for MSSQL to be ready
echo "Waiting for MSSQL to start (this may take 1-2 minutes)..."
until az containerapp show \
  --name $MSSQL_APP \
  --resource-group $RG \
  --query "properties.provisioningState" -o tsv | grep -q "Succeeded"; do
    echo "MSSQL not ready yet. Waiting 10 seconds..."
    sleep 10
done

echo "MSSQL is ready. Deploying Flask container..."
az containerapp create \
  --name $FLASK_APP \
  --resource-group $RG \
  --environment $ENV \
  --image $ACR.azurecr.io/vulcan-platform-dev:latest \
  --cpu 0.5 --memory 1Gi \
  --ingress external \
  --target-port 8000 \
  --registry-server $ACR.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --env-vars DB_SERVER=$MSSQL_APP DB_USER=$DB_USER DB_PASS=$DB_PASS DB_NAME=$DB_NAME

# Get Flask URL
URL=$(az containerapp show \
  --name $FLASK_APP \
  --resource-group $RG \
  --query properties.configuration.ingress.fqdn -o tsv)

echo "----------------------------------------"
echo "🚀 Your app is live at:"
echo "https://$URL"
echo "----------------------------------------"