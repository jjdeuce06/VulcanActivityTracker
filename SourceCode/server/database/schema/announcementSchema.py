import pyodbc

def create_team_announcements_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_announcements'")
    if cursor.fetchone():
        print("Table 'team_announcements' already exists. Skipping creation.")
    else:
        print("Creating 'team_announcements' table...")
        cursor.execute("""
        CREATE TABLE [team_announcements] (
            AnnouncementID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,
            TeamID UNIQUEIDENTIFIER NOT NULL,
            CreatedByUserID UNIQUEIDENTIFIER NOT NULL,
            Title NVARCHAR(150) NOT NULL,
            Body NVARCHAR(MAX) NOT NULL,
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

            CONSTRAINT FK_team_announcements_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            CONSTRAINT FK_team_announcements_user
                FOREIGN KEY (CreatedByUserID) REFERENCES [user](UserID)
        );
        """)
        conn.commit()
        print("Team announcements table created successfully.")

    cursor.close()