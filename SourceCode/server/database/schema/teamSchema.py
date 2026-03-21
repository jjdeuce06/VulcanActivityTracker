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
            TeamID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,
            TeamName NVARCHAR(100) NOT NULL,
            Sport NVARCHAR(50) NOT NULL,
            Description NVARCHAR(255) NULL,
            CoachUserID UNIQUEIDENTIFIER NOT NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
            UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME()
        );
        """)
        conn.commit()
        print("Teams table created successfully.")

    cursor.close()

def create_team_member_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    # Check if teams table exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_members'")
    if cursor.fetchone():
        print("Table 'team_members' already exists. Skipping creation.")
    else:
        print("Table 'team_members' does not exist. Creating table.")
        cursor.execute("""
        CREATE TABLE [team_members] (
            TeamMemberID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,
            TeamID UNIQUEIDENTIFIER NOT NULL,
            UserID UNIQUEIDENTIFIER NOT NULL,
            Role NVARCHAR(20) NOT NULL DEFAULT 'player',   -- coach or player
            Status NVARCHAR(20) NOT NULL DEFAULT 'invited', -- invited, accepted, declined
            InvitedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
            JoinedDate DATETIME2 NULL,

            CONSTRAINT FK_team_members_team FOREIGN KEY (TeamID) REFERENCES teams(TeamID),
            CONSTRAINT FK_team_members_user FOREIGN KEY (UserID) REFERENCES [user](UserID)
        );
        """)
        conn.commit()
        print("Team Members table created successfully.")

    cursor.close()