import pyodbc


# ---------------- CREATE TEAM ----------------
# Creates a new team and assigns the creator as coach
def create_team(conn, coach_user_id, team_name, sport, description):
    cursor = conn.cursor()

    # Insert team into teams table and return new TeamID
    cursor.execute("""
        INSERT INTO teams (TeamName, Sport, Description)
        OUTPUT inserted.TeamID
        VALUES (?, ?, ?)
    """, (team_name, sport, description))

    # Fetch inserted TeamID
    row = cursor.fetchone()
    if not row:
        raise ValueError("Failed to create team")

    team_id = row.TeamID

    # Insert creator into team_members as coach with active status
    cursor.execute("""
        INSERT INTO team_members (TeamID, UserID, Role, Status)
        VALUES (?, ?, 'coach', 'active')
    """, (team_id, coach_user_id))

    # Commit transaction
    conn.commit()
    cursor.close()

    return str(team_id)


# ---------------- INVITE USER ----------------
# Sends an invite to a user to join a team
def invite_user_to_team(conn, team_id, coach_user_id, invited_user_id):
    cursor = conn.cursor()
    try:
        # Verify that the requester is the coach of the team
        cursor.execute("""
            SELECT TeamID
            FROM teams
            WHERE TeamID = ? AND CoachUserID = ?
        """, (team_id, coach_user_id))

        if not cursor.fetchone():
            raise ValueError("Only the coach can invite players")

        # Check if user already has a membership or invite
        cursor.execute("""
            SELECT Status
            FROM team_members
            WHERE TeamID = ? AND UserID = ?
        """, (team_id, invited_user_id))

        existing = cursor.fetchone()
        if existing:
            raise ValueError("User already has membership or pending invite")

        # Insert invite into team_members with status 'invited'
        cursor.execute("""
            INSERT INTO team_members (TeamID, UserID, Role, Status)
            VALUES (?, ?, 'player', 'invited')
        """, (team_id, invited_user_id))

        conn.commit()
        return True

    finally:
        cursor.close()


# ---------------- ACCEPT INVITE ----------------
# Accepts a team invite and activates membership
def accept_team_invite(conn, team_id, user_id):
    cursor = conn.cursor()
    try:
        # Update invite status to accepted and set join timestamp
        cursor.execute("""
            UPDATE team_members
            SET Status = 'accepted',
            JoinedAt = SYSDATETIME()
            WHERE TeamID = ? AND UserID = ? AND Status = 'invited'
        """, (team_id, user_id))

        # If no rows updated, invite not found
        if cursor.rowcount == 0:
            raise ValueError("Invite not found")

        conn.commit()
        return True

    finally:
        cursor.close()


# ---------------- DECLINE INVITE ----------------
# Declines a team invite
def decline_team_invite(conn, team_id, user_id):
    cursor = conn.cursor()
    try:
        # Update invite status to declined
        cursor.execute("""
            UPDATE team_members
            SET Status = 'declined'
            WHERE TeamID = ? AND UserID = ? AND Status = 'invited'
        """, (team_id, user_id))

        # If no rows updated, invite not found
        if cursor.rowcount == 0:
            raise ValueError("Invite not found")

        conn.commit()
        return True

    finally:
        cursor.close()


# ---------------- GET USER TEAMS ----------------
# Returns all teams the user belongs to
def get_user_teams(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.TeamID, t.TeamName, t.Sport, t.Description, t.CoachUserID, u.Username AS CoachUsername
            FROM teams t
            JOIN team_members tm ON t.TeamID = tm.TeamID
            JOIN [user] u ON t.CoachUserID = u.UserID
            WHERE tm.UserID = ? AND tm.Status IN ('active', 'accepted')
            ORDER BY t.TeamName
        """, (user_id,))

        rows = cursor.fetchall()
        teams = []

        # Build team objects
        for row in rows:
            teams.append({
                "id": str(row.TeamID),
                "name": row.TeamName,
                "sport": row.Sport,
                "description": row.Description or "",
                "coach_user_id": str(row.CoachUserID) if row.CoachUserID else None,
                "coach_username": row.CoachUsername
            })

        return teams

    finally:
        cursor.close()


# ---------------- GET PENDING INVITES ----------------
# Returns all pending team invites for a user
def get_pending_team_invites(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.TeamID, t.TeamName, t.Sport, t.Description, u.Username AS CoachUsername
            FROM teams t
            JOIN team_members tm ON t.TeamID = tm.TeamID
            LEFT JOIN [user] u ON t.CoachUserID = u.UserID
            WHERE tm.UserID = ? AND tm.Status = 'invited'
            ORDER BY t.TeamName
        """, (user_id,))

        rows = cursor.fetchall()
        invites = []

        # Build invite objects
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


# ---------------- GET TEAM DETAILS ----------------
# Returns detailed info about a team including roster
def get_team_detail_for_user(conn, team_id, user_id):
    cursor = conn.cursor()
    try:
        # Fetch team info
        cursor.execute("""
            SELECT t.TeamID, t.TeamName, t.Sport, t.Description, t.CoachUserID, u.Username AS CoachUsername
            FROM teams t
            LEFT JOIN [user] u ON t.CoachUserID = u.UserID
            WHERE t.TeamID = ?
        """, (team_id,))
        team = cursor.fetchone()

        if not team:
            return None

        # Fetch team roster
        cursor.execute("""
            SELECT u.UserID, u.Username, tm.Role, tm.Status
            FROM team_members tm
            JOIN [user] u ON tm.UserID = u.UserID
            WHERE tm.TeamID = ? AND tm.Status IN ('active', 'accepted')
            ORDER BY
                CASE WHEN tm.Role = 'coach' THEN 0 ELSE 1 END,
                u.Username
        """, (team_id,))
        roster_rows = cursor.fetchall()

        roster = []

        # Build roster list
        for row in roster_rows:
            roster.append({
                "user_id": str(row.UserID),
                "username": row.Username,
                "role": row.Role,
                "status": row.Status
            })

        # Return full team object
        return {
            "id": str(team.TeamID),
            "name": team.TeamName,
            "sport": team.Sport,
            "description": team.Description or "",
            "coach_user_id": str(team.CoachUserID) if team.CoachUserID else None,
            "coach_username": team.CoachUsername,
            "roster": roster
        }

    finally:
        cursor.close()