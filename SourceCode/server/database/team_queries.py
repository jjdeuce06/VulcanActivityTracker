def assign_coach_role_if_match(conn, user_id, email):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT TeamID
        FROM team_coach_emails
        WHERE LOWER(Email) = LOWER(?)
        AND IsVerified = 1
    """, (email,))
    rows = cursor.fetchall()

    print("Matching Teams:", rows)

    for row in rows:
        print("Processing TeamID:", row.TeamID)

        cursor.execute("""
            SELECT 1
            FROM team_members
            WHERE TeamID = ?
              AND UserID = ?
        """, (row.TeamID, user_id))

        if not cursor.fetchone():
            print("➡️ Inserting coach membership")
            cursor.execute("""
                INSERT INTO team_members (TeamID, UserID, Role, Status)
                VALUES (?, ?, 'coach', 'active')
            """, (row.TeamID, user_id))
        else:
            print("➡️ Updating existing membership to coach")
            cursor.execute("""
                UPDATE team_members
                SET Role = 'coach',
                    Status = 'active'
                WHERE TeamID = ?
                  AND UserID = ?
            """, (row.TeamID, user_id))

    conn.commit()
    cursor.close()
    print("=== END ASSIGN COACH DEBUG ===\n")


def is_user_on_team(conn, user_id, team_id):
    """
    Returns True if the user is an active member of the team.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1
        FROM team_members
        WHERE UserID = ?
          AND TeamID = ?
          AND Status = 'active'
    """, (user_id, team_id))
    row = cursor.fetchone()
    cursor.close()
    return row is not None


def is_user_team_coach(conn, user_id, team_id):
    print("\n=== COACH CHECK DEBUG ===")
    print("UserID:", user_id)
    print("TeamID:", team_id)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT Role, Status
        FROM team_members
        WHERE UserID = ?
          AND TeamID = ?
    """, (user_id, team_id))

    row = cursor.fetchone()
    print("DB Membership Row:", row)

    cursor.execute("""
        SELECT 1
        FROM team_members
        WHERE UserID = ?
          AND TeamID = ?
          AND Status = 'active'
          AND Role IN ('coach', 'admin')
    """, (user_id, team_id))

    result = cursor.fetchone()

    print("Coach Authorization Result:", result is not None)
    print("=== END COACH CHECK DEBUG ===\n")

    cursor.close()
    return result is not None


def user_can_view_team(conn, team_id, user_id, email=None):
    """
    Team page access check.
    A user can view the team if they have an active membership row.
    Coaches should already be added to team_members by assign_coach_role_if_match().
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1
        FROM team_members
        WHERE TeamID = ?
          AND UserID = ?
          AND Status = 'active'
    """, (team_id, user_id))
    allowed = cursor.fetchone() is not None
    cursor.close()
    return allowed


def get_user_teams(conn, user_id):
    """
    Returns active teams the user belongs to.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.TeamID, t.TeamName, t.Sport, tm.Role
        FROM team_members tm
        JOIN teams t
          ON tm.TeamID = t.TeamID
        WHERE tm.UserID = ?
          AND tm.Status = 'active'
        ORDER BY t.TeamName
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    return rows


def get_team_members(conn, team_id):
    """
    Returns active members for a team, including username and role.
    Useful for team detail pages.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            u.UserID,
            u.Username,
            tm.Role,
            tm.Status,
            tm.JoinedAt
        FROM team_members tm
        JOIN [user] u
          ON tm.UserID = u.UserID
        WHERE tm.TeamID = ?
          AND tm.Status = 'active'
        ORDER BY
            CASE
                WHEN tm.Role = 'coach' THEN 0
                WHEN tm.Role = 'admin' THEN 1
                ELSE 2
            END,
            u.Username
    """, (team_id,))
    rows = cursor.fetchall()
    cursor.close()
    return rows


def fetch_user_by_username(conn, username):
    """
    Fetch full user row by username.
    Useful when login or other flows need more than just UserID.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT UserID, Username, Email, PasswordHash
        FROM [user]
        WHERE Username = ?
    """, (username,))
    row = cursor.fetchone()
    cursor.close()
    return row


def get_user_id(conn, username):
    """
    Fetch only the user's UserID by username.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT UserID
        FROM [user]
        WHERE Username = ?
    """, (username,))
    row = cursor.fetchone()
    cursor.close()
    return row.UserID if row else None


def create_team_invite(conn, team_id, invited_user_id, invited_by_user_id):
    """
    Create a pending invite for a user to join a team.
    Prevents duplicate pending invites and inviting existing active members.
    """
    cursor = conn.cursor()

    

    cursor.execute("""
        SELECT 1
        FROM team_invites
        WHERE TeamID = ?
          AND InvitedUserID = ?
          AND Status = 'pending'
    """, (team_id, invited_user_id))

    if cursor.fetchone():
        cursor.close()
        return False, "Invite already exists"

    cursor.execute("""
        SELECT 1
        FROM team_members
        WHERE TeamID = ?
          AND UserID = ?
          AND Status = 'active'
    """, (team_id, invited_user_id))

    if cursor.fetchone():
        cursor.close()
        return False, "User is already a team member"

    cursor.execute("""
        INSERT INTO team_invites (TeamID, InvitedUserID, InvitedByUserID, Status)
        VALUES (?, ?, ?, 'pending')
    """, (team_id, invited_user_id, invited_by_user_id))

    conn.commit()
    cursor.close()
    return True, "Invite created"


def get_pending_team_invites(conn, user_id):
    """
    Returns all pending invites for a given user.
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            i.InviteID,
            i.TeamID,
            t.TeamName,
            t.Sport,
            u.Username AS InvitedByUsername,
            i.Status,
            i.CreatedAt
        FROM team_invites i
        JOIN teams t
          ON i.TeamID = t.TeamID
        JOIN [user] u
          ON i.InvitedByUserID = u.UserID
        WHERE i.InvitedUserID = ?
          AND i.Status = 'pending'
        ORDER BY i.CreatedAt DESC
    """, (user_id,))

    rows = cursor.fetchall()

    invites = []
    for row in rows:
        invites.append({
            "invite_id": str(row.InviteID),
            "team_id": str(row.TeamID),
            "team_name": row.TeamName,
            "sport": row.Sport,
            "invited_by": row.InvitedByUsername,
            "status": row.Status,
            "created_at": row.CreatedAt.isoformat() if row.CreatedAt else None
        })

    cursor.close()
    return invites


def accept_team_invite(conn, invite_id, user_id):
    """
    Accept a pending invite:
    - validates the invite
    - adds or reactivates the user in team_members
    - marks the invite as accepted
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TeamID, Status
        FROM team_invites
        WHERE InviteID = ?
          AND InvitedUserID = ?
    """, (invite_id, user_id))

    row = cursor.fetchone()

    if not row:
        cursor.close()
        return False, "Invite not found"

    if row.Status != "pending":
        cursor.close()
        return False, "Invite already handled"

    team_id = row.TeamID

    cursor.execute("""
        SELECT 1
        FROM team_members
        WHERE TeamID = ?
          AND UserID = ?
    """, (team_id, user_id))

    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO team_members (TeamID, UserID, Role, Status)
            VALUES (?, ?, 'member', 'active')
        """, (team_id, user_id))
    else:
        cursor.execute("""
            UPDATE team_members
            SET Role = 'member',
                Status = 'active'
            WHERE TeamID = ?
              AND UserID = ?
        """, (team_id, user_id))

    cursor.execute("""
        UPDATE team_invites
        SET Status = 'accepted'
        WHERE InviteID = ?
    """, (invite_id,))

    conn.commit()
    cursor.close()
    return True, "Invite accepted"


def decline_team_invite(conn, invite_id, user_id):
    """
    Decline a pending invite.
    """
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE team_invites
        SET Status = 'declined'
        WHERE InviteID = ?
          AND InvitedUserID = ?
          AND Status = 'pending'
    """, (invite_id, user_id))

    if cursor.rowcount == 0:
        cursor.close()
        return False, "Invite not found or already handled"

    conn.commit()
    cursor.close()
    return True, "Invite declined"

def user_can_access_team(conn, team_id, user_id):
    print("\n=== ACCESS CHECK DEBUG ===")
    print("UserID:", user_id)
    print("TeamID:", team_id)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM team_members
        WHERE TeamID = ?
          AND UserID = ?
          AND Status IN ('active', 'accepted')
    """, (team_id, user_id))

    member = cursor.fetchone()
    print("Membership Check:", member)

    if member:
        print("✅ Access granted via membership\n")
        cursor.close()
        return True

    cursor.execute("""
        SELECT Email
        FROM [user]
        WHERE UserID = ?
    """, (user_id,))

    user_row = cursor.fetchone()
    print("User Row:", user_row)

    if not user_row:
        cursor.close()
        return False

    user_email = user_row.Email
    print("User Email:", user_email)

    cursor.execute("""
        SELECT 1
        FROM team_coach_emails
        WHERE TeamID = ? AND Email = ?
    """, (team_id, user_email))

    email_match = cursor.fetchone()
    print("Email Access Match:", email_match)

    cursor.close()
    return email_match is not None

def get_team_details(conn, team_id):
    cursor = conn.cursor()
    try:
        # 🔹 Get basic team info + coach username
        cursor.execute("""
            SELECT 
                t.TeamID,
                t.TeamName,
                t.Sport,
                t.Description,
                t.CreatedDate,
                t.UpdatedDate,
                u.Username AS CoachUsername
            FROM teams t
            JOIN [user] u ON t.CoachUserID = u.UserID
            WHERE t.TeamID = ?
        """, (team_id,))

        row = cursor.fetchone()
        if not row:
            return None

        team = {
            "team_id": str(row.TeamID),
            "team_name": row.TeamName,
            "sport": row.Sport,
            "description": row.Description,
            "coach": row.CoachUsername,
            "created_date": str(row.CreatedDate),
            "updated_date": str(row.UpdatedDate),
            "members": []
        }

        # 🔹 Get members
        cursor.execute("""
            SELECT u.Username, tm.Role, tm.Status
            FROM team_members tm
            JOIN [user] u ON tm.UserID = u.UserID
            WHERE tm.TeamID = ?
        """, (team_id,))

        members = cursor.fetchall()

        for m in members:
            team["members"].append({
                "username": m.Username,
                "role": m.Role,
                "status": m.Status
            })

        return team

    finally:
        cursor.close()

def link_coach_to_team(conn, user_id, email):
    print("\n=== LINK COACH DEBUG ===")
    print("UserID:", user_id)
    print("Email:", email)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT TeamID
        FROM team_coach_emails
        WHERE Email = ?
    """, (email,))

    matches = cursor.fetchall()
    print("Matching Teams from email:", matches)

    cursor.execute("""
        UPDATE teams
        SET CoachUserID = ?
        WHERE CoachUserID IS NULL
        AND TeamID IN (
            SELECT TeamID
            FROM team_coach_emails
            WHERE Email = ?
        )
    """, (user_id, email))

    print("Rows updated:", cursor.rowcount)

    conn.commit()
    cursor.close()

    print("=== END LINK COACH DEBUG ===\n")