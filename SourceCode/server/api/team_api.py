from flask import Blueprint, request, jsonify, session
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_email
from server.controllers.team_store import (
    create_team as create_team_store,
    invite_user_to_team,
    accept_team_invite,
    decline_team_invite,
    get_user_teams,
    get_pending_team_invites,
    get_team_detail_for_user
)
from server.database.team_queries import (   
    user_can_access_team, 
    get_team_details,
    create_team_announcement,
    is_user_team_coach,
    create_team_invite,
    get_team_announcements,
    create_team_schedule_event,
    get_team_schedule,
    get_team_leaderboard,
    get_pending_team_invites,
    accept_team_invite,
    decline_team_invite
)

team_api = Blueprint("team_api", __name__)


@team_api.route("/createteam", methods=["POST"])
def create_team_route():
    try:
        data = request.get_json() or {}
        team_name = data.get("team_name")
        sport = data.get("sport")
        description = data.get("description", "")

        username = session.get("username")
        user_id = session.get("user_id")

        if not user_id or not username:
            return jsonify({"error": "Not logged in"}), 401

        if not team_name or not sport:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            team_id = create_team_store(conn, user_id, team_name, sport, description)
            return jsonify({"status": "success", "team_id": team_id}), 201
        finally:
            conn.close()

    except Exception as e:
        print("Create team error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/invite", methods=["POST"])
def invite_to_team():
    try:
        data = request.get_json() or {}
        invited_email = data.get("invited_email")
        team_id = data.get("team_id")

        coach_user_id = session.get("user_id")

        print("\n=== ROUTE DEBUG ===")
        print("SESSION USER ID:", coach_user_id)
        print("REQUEST JSON:", data)
        print("====================\n")

        if not coach_user_id:
            return jsonify({"error": "Not logged in"}), 401

        if not invited_email or not team_id:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            # ✅ FIX 1: convert email -> user_id (GUID)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT UserID
                FROM [user]
                WHERE LOWER(Email) = LOWER(?)
            """, (invited_email,))
            row = cursor.fetchone()

            if not row:
                cursor.close()
                return jsonify({"error": "Invited user not found"}), 404

            invited_user_id = row.UserID
            print("INVITED USER ID:", invited_user_id, type(invited_user_id))

            # ✅ FIX 2: use your helper instead of raw SQL
            if not is_user_team_coach(conn, coach_user_id, team_id):
                cursor.close()
                return jsonify({"error": "Only coaches can invite users"}), 403

            cursor.close()

            # ✅ FIX 3: use correct invite function
            success, message = create_team_invite(
                conn,
                team_id,
                invited_user_id,
                coach_user_id
            )

            if not success:
                return jsonify({"error": message}), 400

            return jsonify({"status": "success", "message": message}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Invite error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/myteams", methods=["GET"])
def my_teams():
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        conn = get_db_connection()
        try:
            teams = get_user_teams(conn, user_id)
            return jsonify({"teams": teams}), 200
        finally:
            conn.close()

    except Exception as e:
        print("My teams error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/invites", methods=["GET"])
def my_invites():
    try:
        user_id = session.get("user_id")

        print("\n=== INVITES DEBUG ===")
        print("SESSION USER ID:", user_id)
        print("=====================\n")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        conn = get_db_connection()
        try:
            invites = get_pending_team_invites(conn, user_id)

            print("INVITES RETURNED:", invites)  # 🔥 KEY DEBUG

            return jsonify({"invites": invites}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Invites error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/acceptinvite", methods=["POST"])
def accept_invite_route():
    try:
        data = request.get_json() or {}
        invite_id = data.get("invite_id")  # 🔥 FIXED
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        if not invite_id:
            return jsonify({"error": "Missing invite_id"}), 400

        conn = get_db_connection()
        try:
            success, message = accept_team_invite(conn, invite_id, user_id)

            if not success:
                return jsonify({"error": message}), 400

            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Accept invite error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/declineinvite", methods=["POST"])
def decline_invite_route():
    try:
        data = request.get_json() or {}
        team_id = data.get("team_id")
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        if not team_id:
            return jsonify({"error": "Missing team_id"}), 400

        conn = get_db_connection()
        try:
            decline_team_invite(conn, team_id, user_id)
            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Decline invite error:", e)
        return jsonify({"error": str(e)}), 500@team_api.route("/declineinvite", methods=["POST"])
def decline_invite_route():
    try:
        data = request.get_json() or {}
        invite_id = data.get("invite_id")  # 🔥 FIXED
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        if not invite_id:
            return jsonify({"error": "Missing invite_id"}), 400

        conn = get_db_connection()
        try:
            success, message = decline_team_invite(conn, invite_id, user_id)

            if not success:
                return jsonify({"error": message}), 400

            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Decline invite error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/teamdetail", methods=["POST"])
def team_detail():
    try:
        data = request.get_json() or {}
        team_id = data.get("team_id")
        username = session.get("username")
        user_id = session.get("user_id")

        print("DEBUG username:", username, type(username))

        if not team_id:
            return jsonify({"error": "Missing team_id"}), 400

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        conn = get_db_connection()
        print("DEBUG team_id:", team_id, type(team_id))
        print("DEBUG session user_id:", user_id, type(user_id))
        print("DEBUG username:", username, type(username))
        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT Role, Status
                FROM team_members
                WHERE TeamID = ? AND UserID = ?
            """, (team_id, user_id))
            membership = cursor.fetchone()

            print("Membership row:", membership)
            print("user_can_access_team result:", user_can_access_team(conn, team_id, user_id))

            if not user_can_access_team(conn, team_id, user_id):
                cursor.close()
                return jsonify({"error": "Unauthorized"}), 403

            cursor.execute("""
                SELECT TeamID, TeamName, Sport, Description
                FROM teams
                WHERE TeamID = ?
            """, (team_id,))
            team_row = cursor.fetchone()

            if not team_row:
                cursor.close()
                return jsonify({"error": "Team not found"}), 404

            cursor.execute("""
                SELECT u.UserID, u.Username, tm.Role, tm.Status
                FROM team_members tm
                JOIN [user] u ON tm.UserID = u.UserID
                WHERE tm.TeamID = ?
                ORDER BY
                    CASE
                        WHEN tm.Role = 'coach' THEN 0
                        WHEN tm.Role = 'admin' THEN 1
                        ELSE 2
                    END,
                    u.Username
            """, (team_id,))
            roster_rows = cursor.fetchall()
            cursor.close()

            roster = []
            for row in roster_rows:
                roster.append({
                    "user_id": str(row.UserID),
                    "username": row.Username,
                    "role": row.Role,
                    "status": row.Status
                })

            team = {
                "id": str(team_row.TeamID),
                "name": team_row.TeamName,
                "sport": team_row.Sport,
                "description": team_row.Description,
                "is_coach": bool(membership and membership.Role in ["coach", "admin"]),
                "roster": roster
            }

            return jsonify({"team": team}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Team detail error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/listallteams", methods=["GET"])
def list_all_teams():
    try:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT TeamID, TeamName, Sport, Description
                FROM teams
                ORDER BY TeamName
            """)
            rows = cursor.fetchall()
            cursor.close()

            teams = []
            for row in rows:
                teams.append({
                    "TeamID": str(row.TeamID),
                    "TeamName": row.TeamName,
                    "Sport": row.Sport,
                    "Description": row.Description
                })

            return jsonify({"teams": teams}), 200
        finally:
            conn.close()

    except Exception as e:
        print("List all teams error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/team/<team_id>", methods=["GET"])
def get_team(team_id):
    conn = get_db_connection()
    try:
        user_id = session.get("user_id")

        print("\n=== TEAM ROUTE DEBUG ===")
        print("Team ID:", team_id)
        print("Session UserID:", user_id)
        print("========================")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        access = user_can_access_team(conn, team_id, user_id)
        print("Access Result:", access)

        if not access:
            return jsonify({"error": "Access denied"}), 403

        team = get_team_details(conn, team_id)
        return jsonify(team), 200
    finally:
        conn.close()

@team_api.route("/announcement", methods=["POST"])
def create_announcement_route():
    try:
        data = request.get_json() or {}
        team_id = data.get("team_id")
        title = data.get("title")
        body = data.get("body")
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        if not team_id or not title or not body:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            if not is_user_team_coach(conn, user_id, team_id):
                return jsonify({"error": "Only coaches can post announcements"}), 403

            create_team_announcement(conn, team_id, user_id, title, body)
            return jsonify({"status": "success"}), 201
        finally:
            conn.close()

    except Exception as e:
        print("Create announcement error:", e)
        return jsonify({"error": str(e)}), 500

@team_api.route("/announcements/<team_id>", methods=["GET"])
def get_announcements_route(team_id):
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        conn = get_db_connection()
        try:
            if not user_can_access_team(conn, team_id, user_id):
                return jsonify({"error": "Unauthorized"}), 403

            announcements = get_team_announcements(conn, team_id)
            return jsonify({"announcements": announcements}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Get announcements error:", e)
        return jsonify({"error": str(e)}), 500
    

@team_api.route("/schedule", methods=["POST"])
def create_schedule_event_route():
    try:
        data = request.get_json() or {}
        team_id = data.get("team_id")
        event_title = data.get("event_title")
        event_type = data.get("event_type")
        event_date = data.get("event_date")
        location = data.get("location")
        notes = data.get("notes")
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        if not team_id or not event_title or not event_type or not event_date:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            if not is_user_team_coach(conn, user_id, team_id):
                return jsonify({"error": "Only coaches can create schedule events"}), 403

            create_team_schedule_event(
                conn,
                team_id,
                user_id,
                event_title,
                event_type,
                event_date,
                location,
                notes
            )
            return jsonify({"status": "success"}), 201
        finally:
            conn.close()

    except Exception as e:
        print("Create schedule event error:", e)
        return jsonify({"error": str(e)}), 500

@team_api.route("/schedule/<team_id>", methods=["GET"])
def get_schedule_route(team_id):
    try:
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        conn = get_db_connection()
        try:
            if not user_can_access_team(conn, team_id, user_id):
                return jsonify({"error": "Unauthorized"}), 403

            events = get_team_schedule(conn, team_id)
            return jsonify({"events": events}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Get schedule error:", e)
        return jsonify({"error": str(e)}), 500

@team_api.route("/leaderboard/<team_id>", methods=["GET"])
def team_leaderboard(team_id):
    try:
        user_id = session.get("user_id")
        sport_type = request.args.get("sport_type", "all")

        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        conn = get_db_connection()
        try:
            if not user_can_access_team(conn, team_id, user_id):
                return jsonify({"error": "Unauthorized"}), 403

            leaderboard = get_team_leaderboard(conn, team_id, sport_type)
            return jsonify({"leaderboard": leaderboard}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Team leaderboard error:", e)
        return jsonify({"error": str(e)}), 500