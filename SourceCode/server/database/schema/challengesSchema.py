# challengesSchema.py:
import pyodbc


# ---------------- CREATE CHALLENGES TABLE ----------------
# Creates the challenges table if it does not already exist
def create_challenges_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    # Query system tables to see if 'challenges' table already exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'challenges'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'challenges' already exists. Skipping creation.")
    else:
        print("Table 'challenges' does not exist. Creating table.")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
            CREATE TABLE [challenges] (
                ChallengeID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),   -- unique challenge ID
                ChallengeName NVARCHAR(255) NOT NULL UNIQUE,                -- unique challenge name
                Description NVARCHAR(MAX) NULL,                             -- optional description
                CreatorUserID UNIQUEIDENTIFIER NOT NULL,                    -- user who created challenge
                Participants NVARCHAR(MAX) NULL DEFAULT '[]',               -- JSON list of participant user IDs
                ActivityType NVARCHAR(100) NOT NULL,                        -- type of activity (Running, Cycling, etc)
                MetricType NVARCHAR(50) NOT NULL,                           -- metric tracked (distance, count, etc)
                TargetValue FLOAT NOT NULL,                                 -- goal value for challenge
                StartDate DATE NOT NULL,                                    -- challenge start date
                EndDate DATE NOT NULL,                                      -- challenge end date
                IsCompleted BIT NOT NULL DEFAULT 0,                         -- flag if challenge is completed
                MedalsAwarded BIT NOT NULL DEFAULT 0,                       -- flag if rewards have been distributed

                -- Foreign key linking to creator user
                CONSTRAINT FK_challenges_CreatorUser 
                    FOREIGN KEY (CreatorUserID) REFERENCES [user](UserID)
            )
        """)

        # Commit table creation
        conn.commit()

        print("Challenges table created successfully.")

    # Close cursor
    cursor.close()