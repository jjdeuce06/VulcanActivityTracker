import os
import time
import pyodbc


# ---------------- GET DATABASE CONNECTION ----------------
# Connects to SQL Server using environment variables with retry logic
def get_db_connection():

    # ---------------- LOAD ENV VARIABLES ----------------
    # Retrieve required DB credentials from environment
    server = os.environ.get("DB_SERVER")
    database = os.environ.get("DB_NAME")
    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")

    # ---------------- VALIDATE ENV VARIABLES ----------------
    # Check if any required variables are missing
    missing = [var for var, val in [
        ("DB_SERVER", server),
        ("DB_NAME", database),
        ("DB_USER", username),
        ("DB_PASS", password)
    ] if not val]

    if missing:
        # Raise error listing missing variables
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    # ---------------- CONNECTION STRING ----------------
    # Build ODBC connection string for SQL Server
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server},1433;"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;" #no for hosting, yes for local 
    )

    # ---------------- RETRY LOGIC ----------------
    # Attempt to connect multiple times (useful for Docker startup timing)
    for attempt in range(60):
        try:
            # Try connecting to DB
            conn = pyodbc.connect(conn_str, timeout=5)

            print("DB connection successful")

            return conn

        except pyodbc.Error as e:
            # If connection fails, log and retry after delay
            print(f"DB not ready yet (attempt {attempt+1}/60): {e}")
            time.sleep(3)

    # If all retries fail, raise error
    raise RuntimeError("SQL Server never became ready")