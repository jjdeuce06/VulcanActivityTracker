import pyodbc


# ---------------- CREATE TEAMS TABLE ----------------
# Creates the teams table if it does not already exist
def create_teams_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'teams'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'teams' already exists. Skipping creation.")
    else:
        print("Table 'teams' does not exist. Creating table.")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
        CREATE TABLE [teams] (
            TeamID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,  -- unique team ID
            TeamName NVARCHAR(100) NOT NULL,                                -- team name
            Sport NVARCHAR(50) NOT NULL,                                    -- sport type
            Description NVARCHAR(255) NULL,                                 -- optional description
            CoachUserID UNIQUEIDENTIFIER NULL,                              -- optional coach user reference
            CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),           -- creation timestamp
            UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME()            -- last update timestamp
            CONSTRAINT FK_teams_coach                                       -- foreign key for coach
                FOREIGN KEY (CoachUserID) REFERENCES [user](UserID)
        );
        """)

        # Commit table creation
        conn.commit()
        print("Teams table created successfully.")

    # Close cursor
    cursor.close()


# ---------------- CREATE TEAM MEMBERS TABLE ----------------
# Stores membership, roles, and status for users in teams
def create_team_member_table(conn: pyodbc.Connection) -> None:

    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_members'")

    if cursor.fetchone():
        print("Table 'team_members' already exists. Skipping creation.")
    else:
        print("Table 'team_members' does not exist. Creating table.")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
        CREATE TABLE [team_members] (
            TeamMemberID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,  -- unique membership ID
            TeamID UNIQUEIDENTIFIER NOT NULL,                                     -- team reference
            UserID UNIQUEIDENTIFIER NOT NULL,                                     -- user reference
            Role NVARCHAR(30) NOT NULL DEFAULT 'member',                          -- role (member/coach/admin)
            Status NVARCHAR(30) NOT NULL DEFAULT 'active',                        -- status (active/invited/etc)
            JoinedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),                    -- join timestamp

            -- Foreign key linking to team
            CONSTRAINT FK_team_members_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            -- Foreign key linking to user
            CONSTRAINT FK_team_members_user
                FOREIGN KEY (UserID) REFERENCES [user](UserID)
        );
        """)

        conn.commit()
        print("Team Members table created successfully.")

        # ---------------- UNIQUE CONSTRAINT ----------------
        # Prevent duplicate membership entries for same user/team
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


# ---------------- CREATE TEAM COACH EMAILS TABLE ----------------
# Stores pre-approved coach emails for teams
def create_team_coach_emails_table(conn: pyodbc.Connection) -> None:

    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_coach_emails'")

    if cursor.fetchone():
        print("Table 'team_coach_emails' already exists. Skipping creation.")
    else:
        print("Creating 'team_coach_emails' table...")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
        CREATE TABLE [team_coach_emails] (
            CoachEmailID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,  -- unique email entry ID
            TeamID UNIQUEIDENTIFIER NOT NULL,                                    -- team reference
            Email NVARCHAR(255) NOT NULL,                                        -- coach email address
            IsVerified BIT NOT NULL DEFAULT 1,                                   -- verification flag
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),                  -- timestamp

            -- Foreign key linking to team
            CONSTRAINT FK_team_coach_emails_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID)
        );
        """)

        conn.commit()
        print("Team coach emails table created successfully.")

    cursor.close()


# ---------------- CREATE TEAM JOIN REQUESTS TABLE ----------------
# Handles user requests to join teams
def create_team_join_requests_table(conn: pyodbc.Connection) -> None:

    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_join_requests'")

    if cursor.fetchone():
        print("Table 'team_join_requests' already exists. Skipping creation.")
    else:
        print("Creating 'team_join_requests' table...")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
        CREATE TABLE [team_join_requests] (
            RequestID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,  -- unique request ID
            TeamID UNIQUEIDENTIFIER NOT NULL,                                 -- team being requested
            UserID UNIQUEIDENTIFIER NOT NULL,                                 -- requesting user
            Status NVARCHAR(30) NOT NULL DEFAULT 'pending',                   -- request status
            RequestedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),             -- timestamp

            -- Foreign key linking to team
            CONSTRAINT FK_team_join_requests_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            -- Foreign key linking to user
            CONSTRAINT FK_team_join_requests_user
                FOREIGN KEY (UserID) REFERENCES [user](UserID)
        );
        """)

        conn.commit()
        print("Team join requests table created successfully.")

    cursor.close()