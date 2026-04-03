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
ENV="vulcan-env2"
MSSQL_APP="vulcan-mssql"
FLASK_APP="vulcan-flask"
ACR="vulcanacr"
FLASK_IMAGE="$ACR.azurecr.io/vulcan-platform-dev:latest"

# -------------------------
# Create resource group
# -------------------------
if ! az group show --name $RG &> /dev/null; then
    echo "Creating resource group $RG..."
    az group create --name $RG --location $LOCATION
else
    echo "Resource group $RG exists."
fi

# -------------------------
# Create Container Apps environment
# -------------------------
if ! az containerapp env show --name $ENV --resource-group $RG &> /dev/null; then
    echo "Creating Container Apps environment $ENV..."
    az containerapp env create --name $ENV --resource-group $RG --location $LOCATION
else
    echo "Container Apps environment $ENV exists."
fi

# Wait for environment
echo "Waiting for environment $ENV..."
until [[ "$(az containerapp env show --name $ENV --resource-group $RG --query provisioningState -o tsv)" == "Succeeded" ]]; do
    echo "Environment not ready yet, sleeping 15s..."
    sleep 15
done
echo "✅ Environment ready"

# -------------------------
# Ensure ACR admin enabled
# -------------------------
az acr update -n $ACR --admin-enabled true
ACR_USERNAME=$(az acr credential show -n $ACR --query username -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR --query passwords[0].value -o tsv)
az acr login -n $ACR

# -------------------------
# Build & push Flask image
# -------------------------
echo "Building and pushing Flask image..."
docker build -t $FLASK_IMAGE .
docker push $FLASK_IMAGE

# -------------------------
# Deploy MSSQL (internal)
# -------------------------
if az containerapp show --name $MSSQL_APP --resource-group $RG &> /dev/null; then
    echo "Updating MSSQL container..."
    az containerapp update \
      --name $MSSQL_APP \
      --resource-group $RG \
      --cpu 1 --memory 2Gi \
      --env-vars SA_PASSWORD=$DB_PASS ACCEPT_EULA=Y MSSQL_PID=Developer \
      --environment $ENV
else
    echo "Creating MSSQL container..."
    az containerapp create \
      --name $MSSQL_APP \
      --resource-group $RG \
      --environment $ENV \
      --image mcr.microsoft.com/azure-sql-edge \
      --cpu 1 --memory 2Gi \
      --ingress internal \
      --min-replicas 1 --max-replicas 1 \
      --env-vars SA_PASSWORD=$DB_PASS ACCEPT_EULA=Y MSSQL_PID=Developer
fi

# Wait for MSSQL to be ready
echo "Waiting for MSSQL to be ready..."
until az containerapp exec --name $MSSQL_APP --resource-group $RG --command "echo ok" &> /dev/null; do
    echo "MSSQL not ready yet, sleeping 10s..."
    sleep 10
done
echo "✅ MSSQL ready"

# -------------------------
# Deploy Flask (external)
# -------------------------
DB_SERVER_INTERNAL="$MSSQL_APP" # internal DNS for MSSQL
if az containerapp show --name $FLASK_APP --resource-group $RG &> /dev/null; then
    echo "Updating Flask container..."
    az containerapp update \
      --name $FLASK_APP \
      --resource-group $RG \
      --image $FLASK_IMAGE \
      --cpu 0.5 --memory 1Gi \
      --ingress external \
      --target-port 8000 \
      --env-vars DB_SERVER=$DB_SERVER_INTERNAL DB_USER=$DB_USER DB_PASS=$DB_PASS DB_NAME=$DB_NAME \
      --registry-login-server $ACR.azurecr.io \
      --registry-username $ACR_USERNAME \
      --registry-password $ACR_PASSWORD \
      --environment $ENV
else
    echo "Creating Flask container..."
    az containerapp create \
      --name $FLASK_APP \
      --resource-group $RG \
      --environment $ENV \
      --image $FLASK_IMAGE \
      --cpu 0.5 --memory 1Gi \
      --ingress external \
      --target-port 8000 \
      --env-vars DB_SERVER=$DB_SERVER_INTERNAL DB_USER=$DB_USER DB_PASS=$DB_PASS DB_NAME=$DB_NAME \
      --registry-login-server $ACR.azurecr.io \
      --registry-username $ACR_USERNAME \
      --registry-password $ACR_PASSWORD
fi

# -------------------------
# Show Flask URL
# -------------------------
URL=$(az containerapp show --name $FLASK_APP --resource-group $RG --query properties.configuration.ingress.fqdn -o tsv)
echo "----------------------------------------"
echo "🚀 Flask app live at: https://$URL"
echo "✅ MSSQL is running internally"
echo "To scale down MSSQL and save credits:"
echo "az containerapp update --name $MSSQL_APP --resource-group $RG --min-replicas 0 --max-replicas 1"