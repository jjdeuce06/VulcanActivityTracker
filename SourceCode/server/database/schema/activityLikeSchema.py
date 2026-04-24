import pyodbc

# ---------------- CREATE ACTIVITY LIKES TABLE ----------------
# Creates the activity_likes table if it does not already exist
def create_activity_likes_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    # Query system tables to see if 'activity_likes' already exists
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'activity_likes'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'activity_likes' already exists. Skipping creation.")
    else:
        print("Creating table 'activity_likes'.")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
            CREATE TABLE [activity_likes] (
                ActivityLikeID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),  -- unique ID for each like
                ActivityID UNIQUEIDENTIFIER NOT NULL,                          -- references activity
                LikerUserID UNIQUEIDENTIFIER NOT NULL,                         -- user who liked the activity
                CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),          -- timestamp of like

                -- Foreign key relationships
                FOREIGN KEY (ActivityID) REFERENCES [activity](ActivityID),
                FOREIGN KEY (LikerUserID) REFERENCES [user](UserID),

                -- Prevent duplicate likes (same user liking same activity twice)
                CONSTRAINT UQ_ActivityLike UNIQUE (ActivityID, LikerUserID)
            )
        """)

        # Commit table creation
        conn.commit()
        print("Activity likes table created successfully.")

    # Close cursor
    cursor.close()