import pyodbc

def create_team(conn, coach_user_id, team_name, sport, description):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO teams (TeamName, Sport, Description, CoachUserID)
            OUTPUT INSERTED.TeamID
            VALUES (?, ?, ?, ?)
        """, (team_name, sport, description, coach_user_id))

        row = cursor.fetchone()
        team_id = str(row[0])

        # auto-add coach as accepted member
        cursor.execute("""
            INSERT INTO team_members (TeamID, UserID, Role, Status, JoinedDate)
            VALUES (?, ?, 'coach', 'accepted', SYSDATETIME())
        """, (team_id, coach_user_id))

        conn.commit()
        return team_id
    finally:
        cursor.close()


def invite_user_to_team(conn, team_id, coach_user_id, invited_user_id):
    cursor = conn.cursor()
    try:
        # verify coach owns team
        cursor.execute("""
            SELECT TeamID
            FROM teams
            WHERE TeamID = ? AND CoachUserID = ?
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
            SELECT t.TeamID, t.TeamName, t.Sport, t.Description, t.CoachUserID, u.Username AS CoachUsername
            FROM teams t
            JOIN team_members tm ON t.TeamID = tm.TeamID
            JOIN [user] u ON t.CoachUserID = u.UserID
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
        # first get team
        cursor.execute("""
            SELECT TeamID, TeamName, Sport, Description, CoachUserID
            FROM teams
            WHERE TeamID = ?
        """, (team_id,))
        team = cursor.fetchone()

        if not team:
            return None

        # check access
        cursor.execute("""
            SELECT Role, Status
            FROM team_members
            WHERE TeamID = ? AND UserID = ?
        """, (team_id, user_id))
        membership = cursor.fetchone()

        if not membership or membership.Status != "accepted":
            return "forbidden"

        # get roster
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
            "roster": roster
        }
    finally:
        cursor.close()