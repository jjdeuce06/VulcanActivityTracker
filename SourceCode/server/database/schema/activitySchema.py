# hold schema for each data field
# cross reference to user ID

import pyodbc


# ---------------- CREATE ACTIVITY TABLE ----------------
# Creates the activity table if it does not already exist
def create_activity_table(conn: pyodbc.Connection) -> None:

    # Use context manager for cursor (auto closes)
    with conn.cursor() as cursor:

        # ---------------- CHECK IF TABLE EXISTS ----------------
        cursor.execute("""
            SELECT 1 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'activity'
        """)

        if cursor.fetchone():
            # Table already exists
            print("Table 'activity' already exists. Skipping creation.")
            return

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
            CREATE TABLE [activity] (
                ActivityID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),  -- unique activity ID
                UserID UNIQUEIDENTIFIER NOT NULL,                          -- foreign key to user
                ActivityType NVARCHAR(50) NOT NULL,                        -- type of activity (run, lift, etc.)
                ActivityDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),     -- when activity occurred
                Duration INT NULL,                                        -- duration in minutes
                CaloriesBurned INT NULL,                                  -- calories burned
                Visibility NVARCHAR(50) NULL DEFAULT 'private',            -- visibility setting (public/private)
                Notes NVARCHAR(MAX) NULL,                                 -- optional notes
                Details NVARCHAR(MAX) NULL,                               -- JSON for sport-specific fields
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),     -- record creation timestamp
                UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),     -- last update timestamp

                -- Foreign key constraint linking to user table
                CONSTRAINT FK_UserActivity FOREIGN KEY (UserID) REFERENCES [user](UserID)
            )
        """)

        # Commit table creation
        conn.commit()

        print("Activity table created successfully.")