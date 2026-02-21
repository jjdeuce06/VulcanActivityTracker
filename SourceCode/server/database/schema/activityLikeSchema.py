import pyodbc
def create_activity_likes_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'activity_likes'")
    if cursor.fetchone():
        print("Table 'activity_likes' already exists. Skipping creation.")
    else:
        print("Creating table 'activity_likes'.")

        cursor.execute("""
            CREATE TABLE [activity_likes] (
                ActivityLikeID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                ActivityID UNIQUEIDENTIFIER NOT NULL,
                LikerUserID UNIQUEIDENTIFIER NOT NULL,
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

                FOREIGN KEY (ActivityID) REFERENCES [activity](ActivityID),
                FOREIGN KEY (LikerUserID) REFERENCES [user](UserID),

                CONSTRAINT UQ_ActivityLike UNIQUE (ActivityID, LikerUserID)
            )
        """)

        conn.commit()
        print("Activity likes table created successfully.")

    cursor.close()
