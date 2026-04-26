import pyodbc


# ---------------- CREATE USER TABLE ----------------
# Creates the user table if it does not already exist
def create_user_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'user'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'user' already exists. Skipping creation.")
    else:
        print("Table 'user' does not exist. Creating table.")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
            CREATE TABLE [user] (
                UserID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),   -- unique user ID (UUID)
                Email VARCHAR(255) NOT NULL UNIQUE,                    -- unique email address
                Username VARCHAR(255) NOT NULL UNIQUE,                 -- unique username
                PasswordHash NVARCHAR(255) NOT NULL,                   -- hashed password (argon2)
                isActive BIT NOT NULL DEFAULT 1,                       -- account active flag
                LastLogin DATETIME2 NULL,                              -- last login timestamp
                FailedLoginAttempted INT DEFAULT 0,                    -- failed login attempt counter
                TempPassword VARCHAR(255) NULL,                        -- temporary password (if used)
                
                -- JSON field storing user medals and achievements
                Medals NVARCHAR(MAX) NOT NULL DEFAULT '{"gold": 0, "silver": 0, "bronze": 0, "completed": 0}',
                
                UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME()   -- last update timestamp
            )
        """)

        # Commit table creation
        conn.commit()

        print("User table created successfully.")

    # Close cursor
    cursor.close()