# Hosting Flask + MSSQL on Azure for Students

This guide explains how to host a Python Flask app with an existing SQL Server database using **Azure for Students**—completely free for educational purposes.

---

## 1️⃣ Sign Up for Azure for Students

1. Go to: [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
2. Sign up using your `.edu` email.
3. Benefits include:
   - $100 in free credits
   - Access to **App Service** (Linux hosting for Flask)
   - Access to **Azure SQL Database** (fully managed SQL Server)
   - No credit card required

---

## 2️⃣ Hosting Architecture

For your existing Flask app and MSSQL database:

```
Flask App Service  <->  Azure SQL Database
```

- **Flask App Service**: Runs your Python backend
- **Azure SQL Database**: Hosts your existing database schema (no changes needed)

> Note: You no longer need a SQL Server container for production.

---

## 3️⃣ Prepare Flask App for Azure

### a) Remove local SQL Server container dependency

- Delete `mssql:` service from your `docker-compose.yml` (production deployment does not need it).

### b) Install required packages

Ensure `requirements.txt` includes:

```txt
flask
pyodbc
pymssql
gunicorn
```

### c) Update connection string

1. Create an Azure SQL Database in the portal.
2. Get the **connection string**, which looks like:

```txt
Driver={ODBC Driver 18 for SQL Server};Server=tcp:yourserver.database.windows.net,1433;Database=yourdb;Uid=youruser;Pwd=yourpassword;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
```

3. Store it in `.env`:

```env
SQL_CONNECTION_STRING=Driver={ODBC Driver 18 for SQL Server};Server=tcp:yourserver.database.windows.net,1433;Database=yourdb;Uid=youruser;Pwd=yourpassword;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
FLASK_ENV=production
```

4. Use it in Python:

```python
import os
import pyodbc

conn = pyodbc.connect(os.getenv("SQL_CONNECTION_STRING"))
```

### d) Update Dockerfile for Azure

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Start app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

> Optional: You can deploy without Docker using App Service's built-in Python support.

---

## 4️⃣ Deploy to Azure App Service

### Step 1: Create Web App

- In Azure Portal → **Create a resource → Web App**
- Configure:
  - Runtime: Python 3.11
  - OS: Linux
  - Optionally: Docker

### Step 2: Set Environment Variables

- In **App Service → Configuration → Application Settings**
  - `SQL_CONNECTION_STRING` → Azure SQL Database connection
  - `FLASK_ENV` → `production`

### Step 3: Deploy Flask App

Three options:

1. **GitHub Actions** (recommended) → auto-deploy from GitHub
2. **Azure CLI**:

```bash
az webapp up --name <app-name> --resource-group <resource-group>
```

3. **VSCode Azure Extension** → Right-click project → Deploy

### Step 4: Test

Visit:

```
https://yourapp.azurewebsites.net
```

---

## 5️⃣ Optional: Free Domain & HTTPS

- Azure App Service provides a free default domain: `yourapp.azurewebsites.net` with HTTPS.
- Custom domain free options available via **GitHub Student Pack**.

---

## ✅ Summary

1. Keep Flask app as-is.
2. Replace local SQL Server container with **Azure SQL Database**.
3. Update `.env` with Azure connection string.
4. Deploy Flask to **Azure App Service**.
5. Optional: use Docker + Gunicorn for production-grade deployment.

> Advantages:
>
> - No changes to your database schema
> - Completely free for students
> - Fully production-ready deployment
