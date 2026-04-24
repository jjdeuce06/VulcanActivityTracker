import pyodbc


# ---------------- CREATE MAPS TABLE ----------------
# Creates the maps table if it does not already exist
def create_maps_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'maps'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'maps' already exists. Skipping creation.")
    else:
        print("Table 'maps' does not exist. Creating table.")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
            CREATE TABLE [maps] (
                MapID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),   -- unique map/route ID
                UserID UNIQUEIDENTIFIER NOT NULL,                     -- user who created the route
                RouteName NVARCHAR(255) NOT NULL,                     -- name of the route
                DistanceMiles FLOAT NOT NULL,                         -- total distance of the route
                MapData NVARCHAR(MAX) NOT NULL                        -- JSON storing coordinates and route details
            )
        """)

        # Commit table creation
        conn.commit()

        print("Maps table created successfully.")

    # Close cursor
    cursor.close()