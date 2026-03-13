# login controller to store data in database

def store_login(conn, email, username, passwordHash):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO [user] (Email, Username, PasswordHash)
            VALUES (?, ?, ?)
        """, (email, username, passwordHash))
        conn.commit()
    finally:
        cursor.close()


def fetch_login(conn, username):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT PasswordHash
            FROM [user]
            WHERE Username = ?
        """, (username,))
        row = cursor.fetchone()
        return row.PasswordHash if row else None
    finally:
        cursor.close()


def fetch_all_users(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT Username
            FROM [user]
        """)
        rows = cursor.fetchall()
        users = [row.Username for row in rows]
        return users
    finally:
        cursor.close()


def fetch_user_by_email(conn, email):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT UserID, Username, Email
            FROM [user]
            WHERE Email = ?
        """, (email,))
        return cursor.fetchone()
    finally:
        cursor.close()


def fetch_user_by_username(conn, username):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT UserID, Username, Email
            FROM [user]
            WHERE Username = ?
        """, (username,))
        return cursor.fetchone()
    finally:
        cursor.close()

def update_password_by_email(conn, email, passwordHash):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE [user]
            SET PasswordHash = ?
            WHERE Email = ?
        """, (passwordHash, email))
        conn.commit()
        print("")
        return cursor.rowcount > 0
    finally:
        cursor.close()