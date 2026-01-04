#init database connection
import pyodbc

def get_db_connection():
    # Create the database connection
    return pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=mssql_server,1433;"  
    "DATABASE=master;"         
    "UID=sa;"
    "PWD=VulcanP@ssw0rd!;"
    "TrustServerCertificate=yes"
)