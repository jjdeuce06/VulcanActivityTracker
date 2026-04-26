import pyodbc


# ---------------- CREATE CLUBS TABLE ----------------
# Creates the clubs table if it does not already exist
def create_clubs_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'clubs'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'clubs' already exists. Skipping creation.")
    else:
        print("Table 'clubs' does not exist. Creating table.")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
            CREATE TABLE [clubs] (
                ClubID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),   -- unique club ID
                ClubName NVARCHAR(255) NOT NULL UNIQUE,                -- unique club name
                Description NVARCHAR(MAX) NULL,                        -- optional description
                CreatorUserID UNIQUEIDENTIFIER NOT NULL,               -- user who created the club
                SportType NVARCHAR(100) NOT NULL,                      -- sport category (soccer, running, etc.)
                IsPrivate BIT NOT NULL DEFAULT 0,                      -- privacy flag (0 = public, 1 = private)
                Members NVARCHAR(MAX) NULL DEFAULT '[]',               -- JSON list of member user IDs
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),  -- creation timestamp
                UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),  -- last update timestamp

                -- Foreign key linking club to its creator
                CONSTRAINT FK_CreatorUser 
                    FOREIGN KEY (CreatorUserID) REFERENCES [user](UserID)
            )
        """)

        # Commit table creation
        conn.commit()

        print("Clubs table created successfully.")

    # Close cursor
    cursor.close()