#init database connection
import os
import time
import pyodbc

def get_db_connection():
    # Create the database connection
    conn_str =(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=mssql_server,1433;"  
    "DATABASE=master;"         
    "UID=sa;"
    "PWD=VulcanP@ssw0rd!;"
    "TrustServerCertificate=yes"
    )

    for attempt in range(15):
        try:
            return pyodbc.connect(conn_str, timeout=5)
        except pyodbc.Error as e:
            print(f"DB not ready yet (attempt {attempt+1}/15)")
            time.sleep(2)
    raise RuntimeError("SQL Server never became ready")
