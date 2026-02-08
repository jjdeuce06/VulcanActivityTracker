#hold schema for each data feild
#cross refernce to user ID

import pyodbc

def create_friends_table(conn: pyodbc.Connection) -> None:
    with conn.cursor() as cursor:
        # check if table exists
        cursor.execute("""
            SELECT 1
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = 'friend'
        """)
        if cursor.fetchone():
            print("Table 'friend' already exists. Skipping creation.")
            return

        # create table
        cursor.execute("""
            CREATE TABLE [friend] (
                id INT IDENTITY(1,1) PRIMARY KEY,
                UserID UNIQUEIDENTIFIER NOT NULL,
                friend_id NVARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT GETDATE()
            )
        """)
        conn.commit()
        print("Friend table created successfully.")


