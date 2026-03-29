import pyodbc

def create_team_invites_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_invites'")
    if cursor.fetchone():
        print("Table 'team_invites' already exists. Skipping creation.")
    else:
        print("Creating 'team_invites' table...")

        cursor.execute("""
        CREATE TABLE [team_invites] (
            InviteID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,
            TeamID UNIQUEIDENTIFIER NOT NULL,
            InvitedUserID UNIQUEIDENTIFIER NOT NULL,
            InvitedByUserID UNIQUEIDENTIFIER NOT NULL,
            Status NVARCHAR(30) NOT NULL DEFAULT 'pending',
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

            CONSTRAINT FK_team_invites_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            CONSTRAINT FK_team_invites_invited_user
                FOREIGN KEY (InvitedUserID) REFERENCES [user](UserID),

            CONSTRAINT FK_team_invites_invited_by
                FOREIGN KEY (InvitedByUserID) REFERENCES [user](UserID)
        );
        """)

        conn.commit()
        print("Team invites table created successfully.")

        cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sys.indexes
            WHERE name = 'UQ_team_invites_team_user_pending'
        )
        BEGIN
            CREATE UNIQUE INDEX UQ_team_invites_team_user_pending
            ON team_invites (TeamID, InvitedUserID)
            WHERE Status = 'pending';
        END
        """)
        conn.commit()

        print("Unique pending invite index created successfully.")

    cursor.close()