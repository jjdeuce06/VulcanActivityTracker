import pyodbc

def create_clubs_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    # Check if clubs table exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'clubs'")
    if cursor.fetchone():
        print("Table 'clubs' already exists. Skipping creation.")
    else:
        print("Table 'clubs' does not exist. Creating table.")
        cursor.execute("""
            CREATE TABLE [clubs] (
                ClubID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                ClubName NVARCHAR(255) NOT NULL,
                Description NVARCHAR(MAX) NULL,
                CreatorUserID UNIQUEIDENTIFIER NOT NULL,
                Members NVARCHAR(MAX) NULL DEFAULT '[]', -- JSON for member user IDs
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
                UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
                CONSTRAINT FK_CreatorUser FOREIGN KEY (CreatorUserID) REFERENCES [user](UserID)
            )
        """)
        conn.commit()
        print("Clubs table created successfully.")

    cursor.close()