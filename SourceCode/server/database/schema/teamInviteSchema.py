import pyodbc


# ---------------- CREATE TEAM INVITES TABLE ----------------
# Creates the team_invites table and associated index if it does not already exist
def create_team_invites_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_invites'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'team_invites' already exists. Skipping creation.")
    else:
        print("Creating 'team_invites' table...")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
        CREATE TABLE [team_invites] (
            InviteID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,  -- unique invite ID
            TeamID UNIQUEIDENTIFIER NOT NULL,                                -- team the invite is for
            InvitedUserID UNIQUEIDENTIFIER NOT NULL,                         -- user being invited
            InvitedByUserID UNIQUEIDENTIFIER NOT NULL,                       -- user who sent the invite (coach/admin)
            Status NVARCHAR(30) NOT NULL DEFAULT 'pending',                  -- invite status (pending/accepted/declined)
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),              -- timestamp when invite was created

            -- Foreign key linking to team
            CONSTRAINT FK_team_invites_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            -- Foreign key linking to invited user
            CONSTRAINT FK_team_invites_invited_user
                FOREIGN KEY (InvitedUserID) REFERENCES [user](UserID),

            -- Foreign key linking to inviter
            CONSTRAINT FK_team_invites_invited_by
                FOREIGN KEY (InvitedByUserID) REFERENCES [user](UserID)
        );
        """)

        # Commit table creation
        conn.commit()
        print("Team invites table created successfully.")

        # ---------------- CREATE UNIQUE INDEX ----------------
        # Prevent duplicate pending invites for same team/user
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

        # Commit index creation
        conn.commit()

        print("Unique pending invite index created successfully.")

    # Close cursor
    cursor.close()