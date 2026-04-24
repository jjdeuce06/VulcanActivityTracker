# ---------------- TOGGLE LIKE (FRIENDS) ----------------
def toggle_like_friend(conn, user_id, friend_id):
    """
    Toggle a like between user_id and friend_id.
    Returns:
        liked (bool): True if now liked, False if unliked
        total_likes (int): total likes for friend_id
    """
    # Create DB cursor
    cursor = conn.cursor()
    try:
        # ---------------- CHECK EXISTING LIKE ----------------
        cursor.execute("""
            SELECT LikeID FROM likes
            WHERE LikerUserID = ? AND LikedUserID = ?
        """, (user_id, friend_id))
        existing = cursor.fetchone()

        if existing:
            # ---------------- UNLIKE ----------------
            cursor.execute("""
                DELETE FROM likes
                WHERE LikerUserID = ? AND LikedUserID = ?
            """, (user_id, friend_id))
            liked = False
        else:
            # ---------------- LIKE ----------------
            cursor.execute("""
                INSERT INTO likes (LikerUserID, LikedUserID)
                VALUES (?, ?)
            """, (user_id, friend_id))
            liked = True

        # ---------------- GET UPDATED LIKE COUNT ----------------
        cursor.execute("""
            SELECT COUNT(*) FROM likes
            WHERE LikedUserID = ?
        """, (friend_id,))
        total_likes = cursor.fetchone()[0]

        return liked, total_likes

    except Exception as e:
        # Log error and return safe values
        print("Toggle like error:", e)
        return None, None

    finally:
        # Always close cursor
        cursor.close()


# ---------------- CHECK IF FRIEND IS LIKED ----------------
def check_if_liked(conn, user_id, friend_id):
    cursor = conn.cursor()

    # Query to check existence of like
    cursor.execute("""
        SELECT 1
        FROM likes
        WHERE LikerUserID = ? AND LikedUserID = ?
    """, (user_id, friend_id))

    result = cursor.fetchone()
    cursor.close()

    # Return True if like exists
    return result is not None


# ---------------- GET TOTAL LIKES FOR USER ----------------
def get_total_likes(conn, friend_id):
    cursor = conn.cursor()

    # Count total likes for a user
    cursor.execute("""
        SELECT COUNT(*)
        FROM likes
        WHERE LikedUserID = ?
    """, (friend_id,))

    result = cursor.fetchone()
    cursor.close()

    # Return count or 0 if none
    return result[0] if result else 0


# ---------------- CHECK IF ACTIVITY HAS THUMBS UP ----------------
def check_if_thumbs_up(conn, liker_id: str, activity_id: str) -> bool:
    cursor = conn.cursor()
    try:
        # Check if user has liked a specific activity
        cursor.execute("""
            SELECT 1 FROM activity_likes
            WHERE LikerUserID = ? AND ActivityID = ?
        """, (liker_id, activity_id))

        return cursor.fetchone() is not None

    finally:
        cursor.close()


# ---------------- GET TOTAL THUMBS UP FOR ACTIVITY ----------------
def get_total_thumbs_up(conn, activity_id: str) -> int:
    cursor = conn.cursor()
    try:
        # Count total likes for an activity
        cursor.execute("""
            SELECT COUNT(*) FROM activity_likes
            WHERE ActivityID = ?
        """, (activity_id,))

        row = cursor.fetchone()
        return row[0] if row else 0

    finally:
        cursor.close()


# ---------------- TOGGLE THUMBS UP (ACTIVITY) ----------------
def toggle_thumbs_up(conn, liker_id: str, activity_id: str):
    cursor = conn.cursor()
    try:
        # Check if already liked
        liked = check_if_thumbs_up(conn, liker_id, activity_id)

        if liked:
            # ---------------- REMOVE LIKE ----------------
            cursor.execute(
                "DELETE FROM activity_likes WHERE LikerUserID = ? AND ActivityID = ?",
                (liker_id, activity_id)
            )
            liked = False
        else:
            # ---------------- ADD LIKE ----------------
            cursor.execute(
                "INSERT INTO activity_likes (LikerUserID, ActivityID) VALUES (?, ?)",
                (liker_id, activity_id)
            )
            liked = True

        # Get updated total likes
        total_likes = get_total_thumbs_up(conn, activity_id)

        return liked, total_likes

    finally:
        # Always close cursor
        cursor.close()