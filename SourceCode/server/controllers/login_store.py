#login controller to store data in database


def store_login(conn, username, passwordHash):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO [user] (Username, PasswordHash)
        VALUES (?, ?)
    """, (username, passwordHash))
    conn.commit()
    cursor.close()