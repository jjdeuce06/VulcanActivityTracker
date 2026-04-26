import pyodbc


# ---------------- CREATE CLUB JOIN REQUESTS TABLE ----------------
# Creates the club_join_requests table and associated index if they do not exist
def create_clubs_invites_table(conn: pyodbc.Connection) -> None:

    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK IF TABLE EXISTS ----------------
    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'club_join_requests'")

    if cursor.fetchone():
        # Table already exists
        print("Table 'club_join_requests' already exists. Skipping creation.")
    else:
        print("Creating 'club_join_requests' table...")

        # ---------------- CREATE TABLE ----------------
        cursor.execute("""
        CREATE TABLE [club_join_requests] (
            RequestID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,  -- unique request ID
            ClubID UNIQUEIDENTIFIER NOT NULL,                                 -- club being requested
            RequestingUserID UNIQUEIDENTIFIER NOT NULL,                       -- user requesting to join
            ClubOwnerUserID UNIQUEIDENTIFIER NOT NULL,                        -- owner of the club
            Status NVARCHAR(30) NOT NULL DEFAULT 'pending',                   -- request status (pending/approved/denied)
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),               -- timestamp of request

            -- Foreign key to club
            CONSTRAINT FK_club_join_requests_club
                FOREIGN KEY (ClubID) REFERENCES clubs(ClubID),

            -- Foreign key to requesting user
            CONSTRAINT FK_club_join_requests_requesting_user
                FOREIGN KEY (RequestingUserID) REFERENCES [user](UserID),

            -- Foreign key to club owner
            CONSTRAINT FK_club_join_requests_owner_user
                FOREIGN KEY (ClubOwnerUserID) REFERENCES [user](UserID)
        );
        """)

        # Commit table creation
        conn.commit()
        print("Club join requests table created successfully.")

        # ---------------- CREATE UNIQUE INDEX ----------------
        # Prevents duplicate pending requests from same user to same club
        cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sys.indexes
            WHERE name = 'UQ_club_join_requests_pending'
        )
        BEGIN
            CREATE UNIQUE INDEX UQ_club_join_requests_pending
            ON club_join_requests (ClubID, RequestingUserID)
            WHERE Status = 'pending';
        END
        """)

        # Commit index creation
        conn.commit()
        print("Unique pending join request index created successfully.")

    # Close cursor
    cursor.close()