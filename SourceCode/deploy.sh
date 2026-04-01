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
  --target-port 8000 \
  --ingress external \
  --cpu 0.5 --memory 1Gi \
  --env-vars DB_SERVER=$DB_SERVER DB_USER=$DB_USER DB_PASS=$DB_PASS DB_NAME=$DB_NAME

echo "Adding MSSQL container..."
az containerapp container set \
  --name $APP \
  --resource-group $RG \
  --container-name mssql \
  --image mcr.microsoft.com/azure-sql-edge \
  --cpu 1 --memory 2Gi \
  --env-vars SA_PASSWORD=$DB_PASS ACCEPT_EULA=Y MSSQL_PID=Developer

echo "Done! Your app is deploying..."