# login controller to store data in database


# ---------------- STORE LOGIN ----------------
# Inserts a new user into the database
def store_login(conn, email, username, passwordHash):
    # Create DB cursor
    cursor = conn.cursor()

    # Insert user record with email, username, and hashed password
    cursor.execute("""
        INSERT INTO [user] (Email, Username, PasswordHash)
        VALUES (?, ?, ?)
    """, (email, username, passwordHash))

    # Commit transaction
    conn.commit()

    # Close cursor
    cursor.close()


# ---------------- FETCH LOGIN ----------------
# Retrieves the stored password hash for a given username
def fetch_login(conn, username):
    # Create DB cursor
    cursor = conn.cursor()

    # Query for password hash
    cursor.execute("""SELECT PasswordHash FROM [user] WHERE Username = ? """, (username,))

    # Get result
    row = cursor.fetchone()

    # Return password hash if user exists, otherwise None
    return row.PasswordHash if row else None


# ---------------- FETCH ALL USERS ----------------
# Returns a list of all usernames in the system
def fetch_all_users(conn):
    # Create DB cursor
    cursor = conn.cursor()

    # Query all usernames
    cursor.execute("""SELECT Username FROM [user]""")

    # Fetch all rows
    rows = cursor.fetchall()

    # Convert rows to list of usernames
    users = [row.Username for row in rows]  

    return users