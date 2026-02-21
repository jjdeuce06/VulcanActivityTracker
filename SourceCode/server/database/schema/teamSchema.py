import pyodbc

def create_teams_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    # Check if teams table exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'teams'")
    if cursor.fetchone():
        print("Table 'teams' already exists. Skipping creation.")
    else:
        print("Table 'teams' does not exist. Creating table.")
        cursor.execute("""
            CREATE TABLE [teams] (
                TeamID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                TeamName NVARCHAR(255) NOT NULL,
                Description NVARCHAR(MAX) NULL,
                CreatorUserID UNIQUEIDENTIFIER NOT NULL,
                Members NVARCHAR(MAX) NULL DEFAULT '[]', -- JSON for member user IDs
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
                UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
                CONSTRAINT FK_TeamCreatorUser FOREIGN KEY (CreatorUserID) REFERENCES [user](UserID)
            )
        """)
        conn.commit()
        print("Teams table created successfully.")

    cursor.close()