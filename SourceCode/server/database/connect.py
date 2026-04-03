import os
import time
import pyodbc

#Connect to SQL Server using environment variables.
def get_db_connection():

    # Require all env variables
    server = os.environ.get("DB_SERVER")
    database = os.environ.get("DB_NAME")
    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")

    # see if missing
    missing = [var for var, val in [
        ("DB_SERVER", server),
        ("DB_NAME", database),
        ("DB_USER", username),
        ("DB_PASS", password)
    ] if not val]

    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server},1433;"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
    )

    # Retry logic
    for attempt in range(60):
        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            print("DB connection successful")
            return conn
        except pyodbc.Error as e:
            print(f"DB not ready yet (attempt {attempt+1}/60): {e}")
            time.sleep(3)

    raise RuntimeError("SQL Server never became ready")