import pyodbc


# ---------------- CREATE TEAM SCHEDULE TABLE ----------------
# Creates the team_schedule table if it does not already exist
def create_team_schedule_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'team_schedule'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'team_schedule' already exists. Skipping creation.")
    else:
        print("Creating 'team_schedule' table...")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
        CREATE TABLE [team_schedule] (
            ScheduleEventID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,  -- unique event ID
            TeamID UNIQUEIDENTIFIER NOT NULL,                                        -- team this event belongs to
            CreatedByUserID UNIQUEIDENTIFIER NOT NULL,                               -- user who created the event
            EventTitle NVARCHAR(150) NOT NULL,                                       -- title of the event
            EventType NVARCHAR(50) NOT NULL,                                         -- type (practice, game, meeting, etc.)
            EventDate DATETIME2 NOT NULL,                                            -- date/time of the event
            Location NVARCHAR(150) NULL,                                             -- optional event location
            Notes NVARCHAR(MAX) NULL,                                                -- additional details/notes
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),                      -- timestamp when event was created

            -- Foreign key linking to team
            CONSTRAINT FK_team_schedule_team
                FOREIGN KEY (TeamID) REFERENCES teams(TeamID),

            -- Foreign key linking to user
            CONSTRAINT FK_team_schedule_user
                FOREIGN KEY (CreatedByUserID) REFERENCES [user](UserID)
        );
        """)

        # Commit table creation
        conn.commit()

        print("Team schedule table created successfully.")

    # Close cursor
    cursor.close()