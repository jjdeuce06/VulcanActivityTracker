import pyodbc

def create_team_schedule_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_schedule'")
    if cursor.fetchone():
        print("Table 'team_schedule' already exists. Skipping creation.")
    else:
        print("Creating 'team_schedule' table...")
        cursor.execute("""
        CREATE TABLE [team_schedule] (
            ScheduleEventID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,
            TeamID UNIQUEIDENTIFIER NOT NULL,
            CreatedByUserID UNIQUEIDENTIFIER NOT NULL,
            EventTitle NVARCHAR(150) NOT NULL,
            EventType NVARCHAR(50) NOT NULL,
            EventDate DATETIME2 NOT NULL,
            Location NVARCHAR(150) NULL,
            Notes NVARCHAR(MAX) NULL,
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

            CONSTRAINT FK_team_schedule_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            CONSTRAINT FK_team_schedule_user
                FOREIGN KEY (CreatedByUserID) REFERENCES [user](UserID)
        );
        """)
        conn.commit()
        print("Team schedule table created successfully.")

    cursor.close()