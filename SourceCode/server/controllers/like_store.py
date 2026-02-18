def toggle_like_friend(conn, user_id, friend_id):
    """
    Toggle a like between user_id and friend_id.
    Returns:
        liked (bool): True if now liked, False if unliked
        total_likes (int): total likes for friend_id
    """
    cursor = conn.cursor()
    try:
        # Check if already liked
        cursor.execute("""
            SELECT LikeID FROM likes
            WHERE LikerUserID = ? AND LikedUserID = ?
        """, (user_id, friend_id))
        existing = cursor.fetchone()

        if existing:
            # Unlike
            cursor.execute("""
                DELETE FROM likes
                WHERE LikerUserID = ? AND LikedUserID = ?
            """, (user_id, friend_id))
            liked = False
        else:
            # Like
            cursor.execute("""
                INSERT INTO likes (LikerUserID, LikedUserID)
                VALUES (?, ?)
            """, (user_id, friend_id))
            liked = True

        # Get updated count
        cursor.execute("""
            SELECT COUNT(*) FROM likes
            WHERE LikedUserID = ?
        """, (friend_id,))
        total_likes = cursor.fetchone()[0]

        return liked, total_likes

    except Exception as e:
        print("Toggle like error:", e)
        return None, None

    finally:
        cursor.close()


def check_if_liked(conn, user_id, friend_id):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM likes
        WHERE LikerUserID = ? AND LikedUserID = ?
    """, (user_id, friend_id))

    result = cursor.fetchone()
    cursor.close()

    return result is not None


def get_total_likes(conn, friend_id):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM likes
        WHERE LikedUserID = ?
    """, (friend_id,))

    result = cursor.fetchone()
    cursor.close()

    return result[0] if result else 0


def check_if_thumbs_up(conn, liker_id: str, activity_id: str) -> bool:
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 1 FROM activity_likes
            WHERE LikerUserID = ? AND ActivityID = ?
        """, (liker_id, activity_id))
        return cursor.fetchone() is not None
    finally:
        cursor.close()


def get_total_thumbs_up(conn, activity_id: str) -> int:
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM activity_likes
            WHERE ActivityID = ?
        """, (activity_id,))
        row = cursor.fetchone()
        return row[0] if row else 0
    finally:
        cursor.close()


def toggle_thumbs_up(conn, liker_id: str, activity_id: str):
    cursor = conn.cursor()
    try:
        liked = check_if_thumbs_up(conn, liker_id, activity_id)

        if liked:
            cursor.execute(
                "DELETE FROM activity_likes WHERE LikerUserID = ? AND ActivityID = ?",
                (liker_id, activity_id)
            )
            liked = False
        else:
            cursor.execute(
                "INSERT INTO activity_likes (LikerUserID, ActivityID) VALUES (?, ?)",
                (liker_id, activity_id)
            )
            liked = True

        total_likes = get_total_thumbs_up(conn, activity_id)
        return liked, total_likes

    finally:
        cursor.close()
