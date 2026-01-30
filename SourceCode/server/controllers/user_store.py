def get_user_id(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT UserID FROM [user] WHERE Username = ?", username)
    row = cursor.fetchone()
    cursor.close()
    if row:
        return row.UserID
    return None
