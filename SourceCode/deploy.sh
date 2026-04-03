#!/bin/bash
set -e
set -a
source .env
set +a

# -------------------------
# Config
# -------------------------
RG="vulcan-rg"
LOCATION="eastus"
ENV="vulcan-env"
MSSQL_APP="vulcan-mssql"
FLASK_APP="vulcan-flask"
ACR="vulcanacr"
FLASK_IMAGE="$ACR.azurecr.io/vulcan-platform-dev:latest"

# -------------------------
# Clean up old apps/env
# -------------------------
echo "=== Cleaning up old apps and environment ==="
for app in $MSSQL_APP $FLASK_APP; do
  if az containerapp show --name $app --resource-group $RG &> /dev/null; then
    echo "Deleting existing Container App $app..."
    az containerapp delete --name $app --resource-group $RG --yes
  fi
done

if az containerapp env show --name $ENV --resource-group $RG &> /dev/null; then
    echo "Deleting existing Container App environment $ENV..."
    az containerapp env delete --name $ENV --resource-group $RG --yes
fi

# -------------------------
# Create resource group if missing
# -------------------------
if ! az group show --name $RG &> /dev/null; then
    echo "=== Creating resource group $RG ==="
    az group create --name $RG --location $LOCATION
else
    echo "Resource group $RG already exists. Skipping creation."
fi

# -------------------------
# Create Container Apps environment
# -------------------------
echo "=== Creating Container Apps environment $ENV ==="
az containerapp env create \
  --name $ENV \
  --resource-group $RG \
  --location $LOCATION

# -------------------------
# Ensure ACR admin enabled
# -------------------------
echo "=== Ensuring ACR $ACR is enabled ==="
az acr update -n $ACR --admin-enabled true
ACR_USERNAME=$(az acr credential show -n $ACR --query username -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR --query passwords[0].value -o tsv)
az acr login -n $ACR

# -------------------------
# Build and push Flask image
# -------------------------
echo "=== Building and pushing Flask image to ACR ==="
docker build -t $FLASK_IMAGE .
docker push $FLASK_IMAGE

# -------------------------
# Deploy MSSQL (internal)
# -------------------------
echo "=== Deploying MSSQL Container App (internal) ==="
az containerapp create \
  --name $MSSQL_APP \
  --resource-group $RG \
  --environment $ENV \
  --image mcr.microsoft.com/azure-sql-edge \
  --cpu 1 --memory 2Gi \
  --ingress internal \
  --min-replicas 1 --max-replicas 1 \
  --env-vars SA_PASSWORD=$DB_PASS ACCEPT_EULA=Y MSSQL_PID=Developer

echo "Waiting for MSSQL to be running..."
while [[ "$(az containerapp show --name $MSSQL_APP --resource-group $RG --query properties.runningStatus -o tsv)" != "Running" ]]; do
  echo "MSSQL not ready yet, waiting 10s..."
  sleep 10
done

# -------------------------
# Deploy Flask (external)
# -------------------------
echo "=== Deploying Flask Container App (external) ==="
az containerapp create \
  --name $FLASK_APP \
  --resource-group $RG \
  --environment $ENV \
  --image $FLASK_IMAGE \
  --cpu 0.5 --memory 1Gi \
  --ingress external \
  --target-port 8000 \
  --env-vars DB_SERVER=$MSSQL_APP DB_USER=$DB_USER DB_PASS=$DB_PASS DB_NAME=$DB_NAME \
  --registry-login-server $ACR.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD

# -------------------------
# Fetch Flask URL
# -------------------------
URL=$(az containerapp show \
  --name $FLASK_APP \
  --resource-group $RG \
  --query properties.configuration.ingress.fqdn -o tsv)

echo "----------------------------------------"
echo "🚀 Your Flask app is live at:"
echo "https://$URL"
echo "----------------------------------------"
echo "✅ MSSQL is running internally."
echo "To scale down MSSQL and save credits, run:"
echo "az containerapp update --name $MSSQL_APP --resource-group $RG --min-replicas 0 --max-replicas 1"