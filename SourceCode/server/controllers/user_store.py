def get_user_id(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT UserID FROM [user] WHERE Username = ?", username)
    row = cursor.fetchone()
    cursor.close()
    if row:
        return row.UserID
    return None


def get_user_email(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT Email FROM [user] WHERE UserID = ?", (user_id))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return row.Email
    return None