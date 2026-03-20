# Azure Container Apps Setup for VulcanActivityTracker

This guide explains how to deploy the Flask + MSSQL Docker Compose project to Azure Container Apps using an Azure Student subscription.

---

## 1. Prerequisites

* Azure for Students subscription ($100 credits)
* Azure CLI installed
* Docker installed
* Working `docker-compose.yml`
* Optional: VSCode + Azure extensions

---

## 2. Create a Resource Group

```bash
az login
az group create --name vulcan-rg --location eastus
```

---

## 3. Create a Container Apps Environment

```bash
az containerapp env create \
    --name vulcan-env \
    --resource-group vulcan-rg \
    --location eastus
```

---

## 4. Push Docker Images to a Registry

### Using Azure Container Registry (ACR)

```bash
# Create ACR
az acr create --resource-group vulcan-rg --name vulcanacr --sku Basic

# Log in to ACR
az acr login --name vulcanacr

# Tag your images
docker tag vulcan-platform-dev vulcanacr.azurecr.io/vulcan-platform-dev:latest
docker tag mssql_server vulcanacr.azurecr.io/mssql_server:latest

# Push images
docker push vulcanacr.azurecr.io/vulcan-platform-dev:latest
docker push vulcanacr.azurecr.io/mssql_server:latest
```

---

## 5. Create the Container App with Flask

```bash
az containerapp create \
    --name vulcan-app \
    --resource-group vulcan-rg \
    --environment vulcan-env \
    --image vulcanacr.azurecr.io/vulcan-platform-dev:latest \
    --target-port 8000 \
    --ingress external \
    --cpu 0.5 --memory 1Gi
```

---

## 6. Add MSSQL Container

```bash
az containerapp container set \
    --name vulcan-app \
    --resource-group vulcan-rg \
    --container-name mssql \
    --image vulcanacr.azurecr.io/mssql_server:latest \
    --cpu 1 --memory 2Gi
```

---

## 7. Set Environment Variables

### Flask container

```bash
az containerapp env var set \
    --name vulcan-app \
    --resource-group vulcan-rg \
    --container-name platform-dev \
    --variables DB_SERVER=mssql DB_USER=sa DB_PASS=yourpassword DB_NAME=yourdb
```

### MSSQL container

```bash
az containerapp env var set \
    --name vulcan-app \
    --resource-group vulcan-rg \
    --container-name mssql \
    --variables SA_PASSWORD=yourpassword ACCEPT_EULA=Y
```

> Flask container can access MSSQL using `mssql` as the host.

---

## 8. Verify Deployment

```bash
az containerapp list --resource-group vulcan-rg -o table
az containerapp logs --name vulcan-app --resource-group vulcan-rg
```

Open the Flask container URL in your browser.

---

## 9. Notes / Tips

* Free-tier resources are limited; avoid heavy workloads
* Port exposed in Dockerfile must match target port (8000)
* Scale containers if needed:

```bash
az containerapp scale set --name vulcan-app --resource-group vulcan-rg --min-replicas 1 --max-replicas 2
```

* Use Gunicorn in Flask container for production-ready server

---

## 10. References

* [Azure Container Apps Documentation](https://learn.microsoft.com/en-us/azure/container-apps/)
* [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
* [Gunicorn WSGI Server](https://gunicorn.org/)
