import pyodbc

def create_or_update_user(conn: pyodbc.Connection) -> None:
    from config.database.schemas.databases import create_table_if_not_exists

    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'user'")
    table_exists = cursor.fetchone() is not None

    if table_exists:
        print("Table 'user' exists. Checking PasswordHash column.")

        cursor.execute("""
            SELECT DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'user' AND COLUMN_NAME = 'PasswordHash'
        """)
        row = cursor.fetchone()

        if row:
            data_type, length = row[0].lower(), row[1]
            print(f"Current PasswordHash column: {data_type}({length})")

            if data_type not in ('varchar', 'nvarchar') or length < 255:
                print("Altering PasswordHash column to NVARCHAR(255).")
                try:
                    cursor.execute("""
                        ALTER TABLE [user]
                        ALTER COLUMN PasswordHash NVARCHAR(255) NOT NULL
                    """)
                    conn.commit()
                    print("PasswordHash column altered successfully.")
                except Exception as e:
                    print(f"Error during ALTER COLUMN: {e}")
            else:
                print("PasswordHash column is valid. No alteration needed.")

        else:
            print("PasswordHash column not found. Adding column.")
            cursor.execute("""
                ALTER TABLE [user]
                ADD PasswordHash NVARCHAR(255) NULL
            """)
            conn.commit()
            print("PasswordHash column added.")

    else:
        print("Table 'user' does not exist. Creating table.")

        create_table_if_not_exists(
            conn,
            "user",
            """
            CREATE TABLE [user] (
                UserID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),

                Username VARCHAR(255) NOT NULL UNIQUE,
                PasswordHash NVARCHAR(255) NOT NULL,

                FirstName VARCHAR(255) NOT NULL,
                LastName VARCHAR(255) NOT NULL,

                isActive BIT NOT NULL DEFAULT 1,

                LastLogin DATETIME2,
                FailedLoginAttempted INT DEFAULT 0,

                TempPassword VARCHAR(255),

                UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

                FOREIGN KEY (EntityID) REFERENCES entity(EntityID)
            )
            """
        )
        print("User table created successfully.")

    cursor.close()
