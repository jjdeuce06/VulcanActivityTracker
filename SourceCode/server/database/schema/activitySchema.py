#hold schema for each data feild
#cross refernce to user ID

import pyodbc

def create_activity_table(conn: pyodbc.Connection) -> None:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 1 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'activity'
        """)
        if cursor.fetchone():
            print("Table 'activity' already exists. Skipping creation.")
            return

        cursor.execute("""
            CREATE TABLE [activity] (
                ActivityID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                UserID UNIQUEIDENTIFIER NOT NULL,             -- link to user
                ActivityType NVARCHAR(50) NOT NULL,
                ActivityDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
                Duration INT NULL,                            -- minutes
                CaloriesBurned INT NULL,
                Visibility NVARCHAR(50) NULL DEFAULT 'private',
                Notes NVARCHAR(MAX) NULL,
                Details NVARCHAR(MAX) NULL,                   -- JSON for sport-specific fields
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
                UpdatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
                CONSTRAINT FK_UserActivity FOREIGN KEY (UserID) REFERENCES [user](UserID)
            )
        """)
        conn.commit()
        print("Activity table created successfully.")

