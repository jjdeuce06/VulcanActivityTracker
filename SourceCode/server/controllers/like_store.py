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

