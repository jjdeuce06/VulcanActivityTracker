import pyodbc


# ---------------- CREATE LIKES TABLE ----------------
# Creates the likes table if it does not already exist
def create_likes_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'likes'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'likes' already exists. Skipping creation.")
    else:
        print("Table 'likes' does not exist. Creating table.")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
            CREATE TABLE [likes] (
                LikeID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),   -- unique like ID
                LikerUserID UNIQUEIDENTIFIER NOT NULL,                 -- user who is liking
                LikedUserID UNIQUEIDENTIFIER NOT NULL,                 -- user being liked
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),  -- timestamp of like

                -- Foreign key linking to user (liker)
                FOREIGN KEY (LikerUserID) REFERENCES [user](UserID),

                -- Foreign key linking to user (liked)
                FOREIGN KEY (LikedUserID) REFERENCES [user](UserID)
            )
        """)

        # Commit table creation
        conn.commit()

        print("Likes table created successfully.")

    # Close cursor
    cursor.close()