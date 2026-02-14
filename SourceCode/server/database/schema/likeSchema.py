import pyodbc

def create_likes_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    # Check if likes table exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'likes'")
    if cursor.fetchone():
        print("Table 'likes' already exists. Skipping creation.")
    else:
        print("Table 'likes' does not exist. Creating table.")
        cursor.execute("""
            CREATE TABLE [likes] (
                LikeID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                LikerUserID UNIQUEIDENTIFIER NOT NULL,
                LikedUserID UNIQUEIDENTIFIER NOT NULL,
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

                FOREIGN KEY (LikerUserID) REFERENCES [user](UserID),
                FOREIGN KEY (LikedUserID) REFERENCES [user](UserID)
            )
        """)
        conn.commit()
        print("Likes table created successfully.")

    cursor.close()
