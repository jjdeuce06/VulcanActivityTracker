import pyodbc

def create_challenges_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    # Check if clubs table exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'challenges'")
    if cursor.fetchone():
        print("Table 'challenges' already exists. Skipping creation.")
    else:
        print("Table 'challenges' does not exist. Creating table.")
        cursor.execute("""
            CREATE TABLE [challenges] (
                ChallengeID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                ChallengeName NVARCHAR(255) NOT NULL,
                Description NVARCHAR(MAX) NULL,
                CreatorUserID UNIQUEIDENTIFIER NOT NULL,
                Participants NVARCHAR(MAX) NULL DEFAULT '[]', -- JSON for participants user IDs
                ActivityType NVARCHAR(100) NOT NULL,  -- Running, Cycling, etc
                MetricType NVARCHAR(50) NOT NULL,     -- distance or count
                StartDate DATE NOT NULL,
                EndDate DATE NOT NULL,
                CONSTRAINT FK_challenges_CreatorUser FOREIGN KEY (CreatorUserID) REFERENCES [user](UserID)
            )
        """)
        conn.commit()
        print("Challenges table created successfully.")

    cursor.close()