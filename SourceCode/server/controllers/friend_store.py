from datetime import datetime 

# ---------------- INSERT FRIEND ----------------
def insert_friend(conn, current_user: str, friend_user: str) -> None:
    """
    Inserts a friend relationship into the 'friend' table.
    Prevents duplicates.
    """
    # Create DB cursor
    cursor = conn.cursor()

    # ---------------- CHECK FOR DUPLICATE ----------------
    # Ensure this friend relationship doesn't already exist
    cursor.execute("""
        SELECT 1 FROM [friend]
        WHERE UserID = ? AND friend_id = ?
    """, (current_user, friend_user))

    # If relationship already exists, raise error
    if cursor.fetchone():
        raise ValueError(f"Friend '{friend_user}' already added for user '{current_user}'.")

    # ---------------- INSERT NEW FRIEND ----------------
    # Add new friend relationship with timestamp
    cursor.execute("""
        INSERT INTO [friend] (UserID, friend_id, created_at)
        VALUES (?, ?, ?)
    """, (current_user, friend_user, datetime.now()))


# ---------------- GET USER FRIENDS ----------------
def get_users_friends(conn, user_id: str) -> list:
    """
    Returns a list of friend usernames for the given user_id.
    """
    # Create DB cursor
    cursor = conn.cursor()

    # Fetch all friend IDs for this user
    cursor.execute("""
        SELECT friend_id 
        FROM [friend]
        WHERE UserID = ?
    """, (user_id,))
    
    # Convert query results into a simple list
    friends = [row[0] for row in cursor.fetchall()]  

    return friends