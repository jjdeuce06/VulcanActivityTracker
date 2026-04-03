#!/bin/bash
set -e
set -a
source .env
set +a

# Config
RG="vulcan-rg"
LOCATION="eastus"
ENV="vulcan-env"
MSSQL_APP="vulcan-mssql"
FLASK_APP="vulcan-flask"
ACR="vulcanacr"
FLASK_IMAGE="$ACR.azurecr.io/vulcan-platform-dev:latest"

echo "=== Checking for existing resources and cleaning up ==="
# Delete apps if they exist
for app in $MSSQL_APP $FLASK_APP; do
  if az containerapp show --name $app --resource-group $RG &> /dev/null; then
    echo "Deleting existing Container App $app..."
    az containerapp delete --name $app --resource-group $RG --yes
  fi
done

# Delete environment if exists
if az containerapp env show --name $ENV --resource-group $RG &> /dev/null; then
    echo "Deleting existing Container App environment $ENV..."
    az containerapp env delete --name $ENV --resource-group $RG --yes
fi

# Delete resource group if exists
if az group show --name $RG &> /dev/null; then
    echo "Deleting existing resource group $RG..."
    az group delete --name $RG --yes --no-wait
    echo "Waiting for deletion to complete..."
    az group wait --name $RG --deleted
fi

echo "=== Creating resource group ==="
az group create --name $RG --location $LOCATION

echo "=== Creating Container Apps environment ==="
az containerapp env create \
  --name $ENV \
  --resource-group $RG \
  --location $LOCATION

echo "=== Enabling ACR Admin ==="
az acr update -n $ACR --admin-enabled true
ACR_USERNAME=$(az acr credential show -n $ACR --query username -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR --query passwords[0].value -o tsv)
az acr login -n $ACR

echo "=== Building and pushing Flask image ==="
docker build -t $FLASK_IMAGE .
docker push $FLASK_IMAGE

echo "=== Deploying MSSQL (internal) ==="
az containerapp create \
  --name $MSSQL_APP \
  --resource-group $RG \
  --environment $ENV \
  --image mcr.microsoft.com/azure-sql-edge \
  --cpu 1 --memory 2Gi \
  --ingress internal \
  --min-replicas 1 --max-replicas 1 \
  --env-vars SA_PASSWORD=$DB_PASS ACCEPT_EULA=Y MSSQL_PID=Developer

echo "Waiting for MSSQL to start..."
while [[ "$(az containerapp show --name $MSSQL_APP --resource-group $RG --query properties.runningStatus -o tsv)" != "Running" ]]; do
  echo "MSSQL not ready yet, waiting 10s..."
  sleep 10
done

echo "=== Deploying Flask (external) ==="
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

echo "=== Fetching Flask URL ==="
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