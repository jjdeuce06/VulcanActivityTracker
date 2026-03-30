import pyodbc

def create_team(conn, coach_user_id, team_name, sport, description):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teams (TeamName, Sport, Description)
        OUTPUT inserted.TeamID
        VALUES (?, ?, ?)
    """, (team_name, sport, description))

    row = cursor.fetchone()
    if not row:
        raise ValueError("Failed to create team")

    team_id = row.TeamID

    cursor.execute("""
        INSERT INTO team_members (TeamID, UserID, Role, Status)
        VALUES (?, ?, 'coach', 'active')
    """, (team_id, coach_user_id))

    conn.commit()
    cursor.close()

    return str(team_id)


def invite_user_to_team(conn, team_id, coach_user_id, invited_user_id):
    cursor = conn.cursor()
    try:
        # verify coach owns team
        cursor.execute("""
            SELECT TeamID
            FROM teams
<<<<<<< HEAD
            WHERE TeamID = ? AND CoachEmailID = ?
=======
            WHERE TeamID = ? AND CoachUserID = ?
>>>>>>> 4e2c12486e594634ad0ee20db86fe64ce0eda99e
        """, (team_id, coach_user_id))
        team = cursor.fetchone()

        if not team:
            raise ValueError("Only the coach can invite players")

        # already exists?
        cursor.execute("""
            SELECT Status
            FROM team_members
            WHERE TeamID = ? AND UserID = ?
        """, (team_id, invited_user_id))
        existing = cursor.fetchone()

        if existing:
            raise ValueError("User already has a team membership/invite")

        cursor.execute("""
            INSERT INTO team_members (TeamID, UserID, Role, Status)
            VALUES (?, ?, 'player', 'invited')
        """, (team_id, invited_user_id))

        conn.commit()
        return True
    finally:
        cursor.close()


def accept_team_invite(conn, team_id, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE team_members
            SET Status = 'accepted',
                JoinedDate = SYSDATETIME()
            WHERE TeamID = ? AND UserID = ? AND Status = 'invited'
        """, (team_id, user_id))

        if cursor.rowcount == 0:
            raise ValueError("Invite not found")

        conn.commit()
        return True
    finally:
        cursor.close()


def decline_team_invite(conn, team_id, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE team_members
            SET Status = 'declined'
            WHERE TeamID = ? AND UserID = ? AND Status = 'invited'
        """, (team_id, user_id))

        if cursor.rowcount == 0:
            raise ValueError("Invite not found")

        conn.commit()
        return True
    finally:
        cursor.close()


def get_user_teams(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
<<<<<<< HEAD
            SELECT t.TeamID, t.TeamName, t.Sport, t.Description, t.CoachEmailID, u.Username AS CoachUsername
            FROM teams t
            JOIN team_members tm ON t.TeamID = tm.TeamID
            JOIN [user] u ON t.CoachEmailID = u.Email
=======
            SELECT t.TeamID, t.TeamName, t.Sport, t.Description, t.CoachUserID, u.Username AS CoachUsername
            FROM teams t
            JOIN team_members tm ON t.TeamID = tm.TeamID
            JOIN [user] u ON t.CoachUserID = u.UserID
>>>>>>> 4e2c12486e594634ad0ee20db86fe64ce0eda99e
            WHERE tm.UserID = ? AND tm.Status = 'accepted'
            ORDER BY t.TeamName
        """, (user_id,))

        rows = cursor.fetchall()
        teams = []
        for row in rows:
            teams.append({
                "id": str(row.TeamID),
                "name": row.TeamName,
                "sport": row.Sport,
                "description": row.Description or "",
                "coach_user_id": str(row.CoachUserID),
                "coach_username": row.CoachUsername
            })
        return teams
    finally:
        cursor.close()


def get_pending_team_invites(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.TeamID, t.TeamName, t.Sport, t.Description, u.Username AS CoachUsername
            FROM teams t
            JOIN team_members tm ON t.TeamID = tm.TeamID
            JOIN [user] u ON t.CoachUserID = u.UserID
            WHERE tm.UserID = ? AND tm.Status = 'invited'
            ORDER BY t.TeamName
        """, (user_id,))

        rows = cursor.fetchall()
        invites = []
        for row in rows:
            invites.append({
                "id": str(row.TeamID),
                "name": row.TeamName,
                "sport": row.Sport,
                "description": row.Description or "",
                "coach_username": row.CoachUsername
            })
        return invites
    finally:
        cursor.close()


def get_team_detail_for_user(conn, team_id, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.TeamID, t.TeamName, t.Sport, t.Description, t.CoachUserID, u.Username AS CoachUsername
            FROM teams t
            JOIN [user] u ON t.CoachUserID = u.UserID
            WHERE t.TeamID = ?
        """, (team_id,))
        team = cursor.fetchone()

        if not team:
            return None

        # cursor.execute("""
        #     SELECT Role, Status
        #     FROM team_members
        #     WHERE TeamID = ? AND UserID = ?
        # """, (team_id, user_id))
        # membership = cursor.fetchone()

        # if not membership or membership.Status != "accepted":
        #     return "forbidden"

        cursor.execute("""
            SELECT u.UserID, u.Username, tm.Role, tm.Status
            FROM team_members tm
            JOIN [user] u ON tm.UserID = u.UserID
            WHERE tm.TeamID = ? AND tm.Status = 'accepted'
            ORDER BY
                CASE WHEN tm.Role = 'coach' THEN 0 ELSE 1 END,
                u.Username
        """, (team_id,))
        roster_rows = cursor.fetchall()

        roster = []
        for row in roster_rows:
            roster.append({
                "user_id": str(row.UserID),
                "username": row.Username,
                "role": row.Role,
                "status": row.Status
            })

        return {
            "id": str(team.TeamID),
            "name": team.TeamName,
            "sport": team.Sport,
            "description": team.Description or "",
            "coach_user_id": str(team.CoachUserID),
            "coach_username": team.CoachUsername,
            "roster": roster
        }

    finally:
        cursor.close()


def invite_user_to_team(conn, team_id, coach_user_id, invited_user_id):
    cursor = conn.cursor()
    try:
<<<<<<< HEAD
        # ✅ 1. Verify coach owns the team
=======
>>>>>>> 4e2c12486e594634ad0ee20db86fe64ce0eda99e
        cursor.execute("""
            SELECT TeamID
            FROM teams
            WHERE TeamID = ? AND CoachUserID = ?
        """, (team_id, coach_user_id))
<<<<<<< HEAD

        if not cursor.fetchone():
            raise ValueError("Only the coach can invite players")

        # ✅ 2. Check if user already exists in team_members
=======
        team = cursor.fetchone()

        if not team:
            raise ValueError("Only the coach can invite players")

>>>>>>> 4e2c12486e594634ad0ee20db86fe64ce0eda99e
        cursor.execute("""
            SELECT Status
            FROM team_members
            WHERE TeamID = ? AND UserID = ?
        """, (team_id, invited_user_id))
<<<<<<< HEAD

        existing = cursor.fetchone()
        if existing:
            raise ValueError("User already has membership or pending invite")

        # ✅ 3. Insert invite
=======
        existing = cursor.fetchone()

        if existing:
            raise ValueError("User already has a membership or pending invite")

>>>>>>> 4e2c12486e594634ad0ee20db86fe64ce0eda99e
        cursor.execute("""
            INSERT INTO team_members (TeamID, UserID, Role, Status)
            VALUES (?, ?, 'player', 'invited')
        """, (team_id, invited_user_id))

        conn.commit()
        return True

    finally:
        cursor.close()