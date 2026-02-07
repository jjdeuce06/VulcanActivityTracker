from datetime import datetime 

def insert_friend(conn, current_user: str, friend_user: str) -> None:
    """
    Inserts a friend relationship into the 'friend' table.
    Prevents duplicates.
    """
    cursor = conn.cursor()

    # Check if the friend relationship already exists
    cursor.execute("""
        SELECT 1 FROM [friend]
        WHERE UserID = ? AND friend_id = ?
    """, (current_user, friend_user))

    if cursor.fetchone():
        raise ValueError(f"Friend '{friend_user}' already added for user '{current_user}'.")

    # Insert the new friend
    cursor.execute("""
        INSERT INTO [friend] (UserID, friend_id, created_at)
        VALUES (?, ?, ?)
    """, (current_user, friend_user, datetime.now()))