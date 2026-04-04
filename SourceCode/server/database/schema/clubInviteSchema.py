import pyodbc

def create_clubs_invites_table(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sys.tables WHERE name = 'club_join_requests'")
    if cursor.fetchone():
        print("Table 'club_join_requests' already exists. Skipping creation.")
    else:
        print("Creating 'club_join_requests' table...")

        cursor.execute("""
        CREATE TABLE [club_join_requests] (
            RequestID UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID() PRIMARY KEY,
            ClubID UNIQUEIDENTIFIER NOT NULL,
            RequestingUserID UNIQUEIDENTIFIER NOT NULL,
            ClubOwnerUserID UNIQUEIDENTIFIER NOT NULL,
            Status NVARCHAR(30) NOT NULL DEFAULT 'pending',
            CreatedAt DATETIME2 NOT NULL DEFAULT SYSDATETIME(),

            CONSTRAINT FK_club_join_requests_club
                FOREIGN KEY (ClubID) REFERENCES clubs(ClubID),

            CONSTRAINT FK_club_join_requests_requesting_user
                FOREIGN KEY (RequestingUserID) REFERENCES [user](UserID),

            CONSTRAINT FK_club_join_requests_owner_user
                FOREIGN KEY (ClubOwnerUserID) REFERENCES [user](UserID)
        );
        """)
        conn.commit()
        print("Club join requests table created successfully.")

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
        conn.commit()
        print("Unique pending join request index created successfully.")

    cursor.close()