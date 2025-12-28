import pyodbc
def init_or_upgrade_schema(conn):
    print("Starting schema initialization...")

    from server.database.schema.loginSchema import create_user_table
    create_user_table(conn)
    print("user table schema initialized or updated.")