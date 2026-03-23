def assign_coach_role_if_match(conn, user_id, email):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TeamID
        FROM team_coach_emails
        WHERE LOWER(Email) = LOWER(?)
        AND IsVerified = 1
    """, (email,))
    rows = cursor.fetchall()

    for row in rows:
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1
                FROM team_members
                WHERE TeamID = ? AND UserID = ?
            )
            BEGIN
                INSERT INTO team_members (TeamID, UserID, Role, Status)
                VALUES (?, ?, 'coach', 'active')
            END
        """, (row.TeamID, user_id, row.TeamID, user_id))

    conn.commit()
    cursor.close()


def is_user_on_team(conn, user_id, team_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1
        FROM team_members
        WHERE UserID = ? AND TeamID = ? AND Status = 'active'
    """, (user_id, team_id))
    row = cursor.fetchone()
    cursor.close()
    return row is not None


def is_user_team_coach(conn, user_id, team_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1
        FROM team_members
        WHERE UserID = ?
        AND TeamID = ?
        AND Status = 'active'
        AND Role IN ('coach', 'admin')
    """, (user_id, team_id))
    row = cursor.fetchone()
    cursor.close()
    return row is not None


def get_user_teams(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.TeamID, t.TeamName, t.Sport, tm.Role
        FROM team_members tm
        JOIN teams t ON tm.TeamID = t.TeamID
        WHERE tm.UserID = ?
        AND tm.Status = 'active'
        ORDER BY t.TeamName
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    return rows

def fetch_user_by_username(conn, username):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT UserID, Username, Email, PasswordHash
        FROM [user]
        WHERE Username = ?
    """, (username,))
    
    row = cursor.fetchone()
    cursor.close()
    return row
