from flask import Blueprint, request, jsonify, session
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.team_store import (
    create_team,
    invite_user_to_team,
    accept_team_invite,
    decline_team_invite,
    get_user_teams,
    get_pending_team_invites,
    get_team_detail_for_user
)
from server.database.team_queries import user_can_access_team, get_team_details

team_api = Blueprint('team_api', __name__)

@team_api.route("/createteam", methods=["POST"])
def create_team():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        team_name = data.get("team_name")
        sport = data.get("sport")
        description = data.get("description", "")

        if not username or not team_name or not sport:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            coach_user_id = get_user_id(conn, username)
            if not coach_user_id:
                return jsonify({"error": "User not found"}), 404

            team_id = create_team(conn, coach_user_id, team_name, sport, description)
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
        username = data.get("username")
        invited_username = data.get("invited_username")
        team_id = data.get("team_id")

        print("\n=== ROUTE DEBUG ===")
        print("SESSION USER ID:", session.get("user_id"))
        print("REQUEST JSON:", request.json)
        print("====================\n")

        if not username or not invited_username or not team_id:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            coach_user_id = get_user_id(conn, username)
            invited_user_id = get_user_id(conn, invited_username)

            if not coach_user_id or not invited_user_id:
                return jsonify({"error": "User not found"}), 404

            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1
                FROM team_members
                WHERE TeamID = ? AND UserID = ? AND Role IN ('coach', 'admin') AND Status = 'active'
            """, (team_id, coach_user_id))

            if not cursor.fetchone():
                return jsonify({"error": "Only coaches can invite users"}), 403

            invite_user_to_team(conn, team_id, coach_user_id, invited_user_id)
            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Invite error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/myteams", methods=["POST"])
def my_teams():
    try:
        data = request.get_json() or {}
        username = data.get("username")

        if not username:
            return jsonify({"error": "Missing username"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            teams = get_user_teams(conn, user_id)
            return jsonify({"teams": teams}), 200
        finally:
            conn.close()

    except Exception as e:
        print("My teams error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/invites", methods=["POST"])
def my_invites():
    try:
        data = request.get_json() or {}
        username = data.get("username")

        if not username:
            return jsonify({"error": "Missing username"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            invites = get_pending_team_invites(conn, user_id)
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
        username = data.get("username")
        team_id = data.get("team_id")

        if not username or not team_id:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            accept_team_invite(conn, team_id, user_id)
            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Accept invite error:", e)
        return jsonify({"error": str(e)}), 500


@team_api.route("/declineinvite", methods=["POST"])
def decline_invite_route():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        team_id = data.get("team_id")

        if not username or not team_id:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            decline_team_invite(conn, team_id, user_id)
            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Decline invite error:", e)
        return jsonify({"error": str(e)}), 500
    
from flask import session

@team_api.route("/teamdetail", methods=["POST"])
def team_detail():
    try:
        data = request.get_json() or {}
        team_id = data.get("team_id")
        username = session.get("username")

        print("DEBUG username:", username, type(username))

        if not team_id:
            return jsonify({"error": "Missing team_id"}), 400

        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        conn = get_db_connection()
        print("DEBUG team_id:", team_id, type(team_id))
        print("DEBUG session user_id:", session.get("user_id"), type(session.get("user_id")))
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
                return jsonify({"error": "Unauthorized"}), 403

            # Get team info
            cursor.execute("""
                SELECT TeamID, TeamName, Sport, Description
                FROM teams
                WHERE TeamID = ?
            """, (team_id,))
            team_row = cursor.fetchone()

            if not team_row:
                return jsonify({"error": "Team not found"}), 404

            # Get roster
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
    

@team_api.route('/team/<team_id>', methods=['GET'])
@team_api.route('/team/<team_id>', methods=['GET'])
def get_team(team_id):
    conn = get_db_connection()

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

    return jsonify(team)