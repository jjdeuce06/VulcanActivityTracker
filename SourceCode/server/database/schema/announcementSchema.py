import pyodbc


# ---------------- CREATE TEAM ANNOUNCEMENTS TABLE ----------------
# Creates the team_announcements table if it does not already exist
def create_team_announcements_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    # Query system tables to see if 'team_announcements' already exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_announcements'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'team_announcements' already exists. Skipping creation.")
    else:
        print("Creating 'team_announcements' table...")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
        CREATE TABLE [team_announcements] (
            AnnouncementID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,  -- unique ID for each announcement
            TeamID UNIQUEIDENTIFIER NOT NULL,                                       -- references team
            CreatedByUserID UNIQUEIDENTIFIER NOT NULL,                              -- user who created announcement
            Title NVARCHAR(150) NOT NULL,                                           -- announcement title
            Body NVARCHAR(MAX) NOT NULL,                                            -- announcement content
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),                     -- timestamp of creation

            -- Foreign key linking to team
            CONSTRAINT FK_team_announcements_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            -- Foreign key linking to user
            CONSTRAINT FK_team_announcements_user
                FOREIGN KEY (CreatedByUserID) REFERENCES [user](UserID)
        );
        """)

        # Commit table creation
        conn.commit()

        print("Team announcements table created successfully.")

    # Close cursor
    cursor.close()