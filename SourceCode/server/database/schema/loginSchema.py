import pyodbc

def create_user_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'user'")
    if cursor.fetchone():
        print("Table 'user' already exists. Skipping creation.")
    else:
        print("Table 'user' does not exist. Creating table.")
        cursor.execute("""
            CREATE TABLE [user] (
                UserID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                Email VARCHAR(255) NOT NULL UNIQUE,
                Username VARCHAR(255) NOT NULL UNIQUE,
                PasswordHash NVARCHAR(255) NOT NULL,
                isActive BIT NOT NULL DEFAULT 1,
                LastLogin DATETIME2 NULL,
                FailedLoginAttempted INT DEFAULT 0,
                TempPassword VARCHAR(255) NULL,
                UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME()
            )
        """)
        conn.commit()
        print("User table created successfully.")

    cursor.close()
