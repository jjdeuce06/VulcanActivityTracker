# ---------------- GET USER ID ----------------
# Converts a username → corresponding UserID from database
def get_user_id(conn, username):
    # Create DB cursor
    cursor = conn.cursor()

    # Query for UserID using username
    cursor.execute("SELECT UserID FROM [user] WHERE Username = ?", username)

    # Fetch result
    row = cursor.fetchone()

    # Close cursor
    cursor.close()

    # Return UserID if found
    if row:
        return row.UserID

    # Return None if user not found
    return None


# ---------------- GET USER EMAIL ----------------
# Converts a user_id → corresponding email address
def get_user_email(conn, user_id):
    # Create DB cursor
    cursor = conn.cursor()

    # Query for email using UserID
    cursor.execute("SELECT Email FROM [user] WHERE UserID = ?", (user_id))

    # Fetch result
    row = cursor.fetchone()

    # Close cursor
    cursor.close()

    # Return email if found
    if row:
        return row.Email

    # Return None if not found
    return None