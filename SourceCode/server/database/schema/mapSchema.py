import pyodbc

def create_maps_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    # Check if maps table exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'maps'")
    if cursor.fetchone():
        print("Table 'maps' already exists. Skipping creation.")
    else:
        print("Table 'maps' does not exist. Creating table.")
        cursor.execute("""
            CREATE TABLE [maps] (
                MapID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                UserID UNIQUEIDENTIFIER NOT NULL,
                RouteName NVARCHAR(255) NOT NULL,
                DistanceMiles FLOAT NOT NULL,
                MapData NVARCHAR(MAX) NOT NULL -- JSON for map routes and details
            )
        """)
        conn.commit()
        print("Maps table created successfully.")

    cursor.close()