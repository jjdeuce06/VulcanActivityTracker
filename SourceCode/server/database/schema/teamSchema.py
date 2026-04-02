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
            CoachUserID UNIQUEIDENTIFIER NULL,
            CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
            UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME()
            CONSTRAINT FK_teams_coach
                FOREIGN KEY (CoachUserID) REFERENCES [user](UserID)
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
            Role NVARCHAR(30) NOT NULL DEFAULT 'member',
            Status NVARCHAR(30) NOT NULL DEFAULT 'active',
            JoinedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
            CONSTRAINT FK_team_members_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),
            CONSTRAINT FK_team_members_user
                FOREIGN KEY (UserID) REFERENCES [user](UserID)
        );
                            
        """)
        conn.commit()
        print("Team Members table created successfully.")

        cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sys.indexes 
            WHERE name = 'UQ_team_members_team_user'
        )
        BEGIN
            ALTER TABLE team_members
            ADD CONSTRAINT UQ_team_members_team_user UNIQUE (TeamID, UserID);
        END
        """)
        conn.commit()

    cursor.close()

def create_team_coach_emails_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_coach_emails'")
    if cursor.fetchone():
        print("Table 'team_coach_emails' already exists. Skipping creation.")
    else:
        print("Creating 'team_coach_emails' table...")

        cursor.execute("""
        CREATE TABLE [team_coach_emails] (
            CoachEmailID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,
            TeamID UNIQUEIDENTIFIER NOT NULL,
            Email NVARCHAR(255) NOT NULL,
            IsVerified BIT NOT NULL DEFAULT 1,
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

            CONSTRAINT FK_team_coach_emails_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID)
        );
        """)

        conn.commit()
        print("Team coach emails table created successfully.")

    cursor.close()


def create_team_join_requests_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_join_requests'")
    if cursor.fetchone():
        print("Table 'team_join_requests' already exists. Skipping creation.")
    else:
        print("Creating 'team_join_requests' table...")

        cursor.execute("""
        CREATE TABLE [team_join_requests] (
            RequestID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,
            TeamID UNIQUEIDENTIFIER NOT NULL,
            UserID UNIQUEIDENTIFIER NOT NULL,
            Status NVARCHAR(30) NOT NULL DEFAULT 'pending',
            RequestedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

            CONSTRAINT FK_team_join_requests_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            CONSTRAINT FK_team_join_requests_user
                FOREIGN KEY (UserID) REFERENCES [user](UserID)
        );
        """)

        conn.commit()
        print("Team join requests table created successfully.")

    cursor.close()