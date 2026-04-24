# hold schema for each data field
# cross reference to user ID

import pyodbc


# ---------------- CREATE FRIEND TABLE ----------------
# Creates the friend table if it does not already exist
def create_friends_table(conn: pyodbc.Connection) -> None:

    # Use context manager for cursor (auto closes)
    with conn.cursor() as cursor:

        # ---------------- CHECK IF TABLE EXISTS ----------------
        cursor.execute("""
            SELECT 1
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = 'friend'
        """)

        if cursor.fetchone():
            # Table already exists
            print("Table 'friend' already exists. Skipping creation.")
            return

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
            CREATE TABLE [friend] (
                id INT IDENTITY(1,1) PRIMARY KEY,         -- auto-increment primary key
                UserID UNIQUEIDENTIFIER NOT NULL,         -- user who owns the friend relationship
                friend_id NVARCHAR(255) NOT NULL,         -- ID of the friend (stored as string)
                created_at DATETIME DEFAULT GETDATE()     -- timestamp when friendship was created
            )
        """)

        # Commit table creation
        conn.commit()

        print("Friend table created successfully.")