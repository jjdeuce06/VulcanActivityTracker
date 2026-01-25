#login controller to store data in database


def store_login(conn, username, passwordHash):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO [user] (Username, PasswordHash)
        VALUES (?, ?)
    """, (username, passwordHash))
    conn.commit()
    cursor.close()

def fetch_login(conn, username):
    cursor = conn.cursor()
    cursor.execute("""SELECT PasswordHash FROM [user] WHERE Username = ? """, (username,))
    row = cursor.fetchone()
    print("verify stored hash:", row.PasswordHash)
    return row.PasswordHash if row else None

def fetch_all_users(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT Username FROM [user]""")
    rows = cursor.fetchall()
    users = [row.Username for row in rows]  
    return users

