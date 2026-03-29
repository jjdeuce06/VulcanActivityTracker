from flask import Blueprint, request, jsonify, session
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.team_store import create_team

from server.database.team_queries import (
    is_user_team_coach,
    create_team_invite,
    get_user_teams,
    get_pending_team_invites,
    accept_team_invite,
    decline_team_invite,
    user_can_view_team,
    get_team_members
)

team_api = Blueprint('team_api', __name__)

# -------------------------
# CREATE TEAM
# -------------------------
@team_api.route("/createteam", methods=["POST"])
def create_team_route():
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


# -------------------------
# INVITE USER
# -------------------------
@team_api.route("/invite", methods=["POST"])
def invite_to_team():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        invited_username = data.get("invited_username")
        team_id = data.get("team_id")

        if not username or not invited_username or not team_id:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            coach_user_id = get_user_id(conn, username)
            invited_user_id = get_user_id(conn, invited_username)

            if not coach_user_id or not invited_user_id:
                return jsonify({"error": "User not found"}), 404

            # 🔑 CLEAN coach check
            if not is_user_team_coach(conn, coach_user_id, team_id):
                return jsonify({"error": "Only coaches can invite users"}), 403

            success, message = create_team_invite(
                conn, team_id, invited_user_id, coach_user_id
            )

            if not success:
                return jsonify({"error": message}), 400

            return jsonify({"status": "success"}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Invite error:", e)
        return jsonify({"error": str(e)}), 500


# -------------------------
# MY TEAMS
# -------------------------
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


# -------------------------
# GET INVITES
# -------------------------
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


# -------------------------
# ACCEPT INVITE (FIXED)
# -------------------------
@team_api.route("/acceptinvite", methods=["POST"])
def accept_invite_route():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        invite_id = data.get("invite_id")  # 🔥 FIXED

        if not username or not invite_id:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            success, message = accept_team_invite(conn, invite_id, user_id)

            if not success:
                return jsonify({"error": message}), 400

            return jsonify({"status": "success"}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Accept invite error:", e)
        return jsonify({"error": str(e)}), 500


# -------------------------
# DECLINE INVITE (FIXED)
# -------------------------
@team_api.route("/declineinvite", methods=["POST"])
def decline_invite_route():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        invite_id = data.get("invite_id")  # 🔥 FIXED

        if not username or not invite_id:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            success, message = decline_team_invite(conn, invite_id, user_id)

            if not success:
                return jsonify({"error": message}), 400

            return jsonify({"status": "success"}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Decline invite error:", e)
        return jsonify({"error": str(e)}), 500


# -------------------------
# TEAM DETAIL
# -------------------------
@team_api.route("/teamdetail", methods=["POST"])
def team_detail():
    try:
        data = request.get_json() or {}
        team_id = data.get("team_id")

        if not team_id:
            return jsonify({"error": "Missing team_id"}), 400

        user_id = session.get("user_id")

        # 🔥 CRITICAL FIX: session stores username, not GUID
        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, user_id)

            if not user_id:
                return jsonify({"error": "Not logged in"}), 401

            if not user_can_view_team(conn, team_id, user_id):
                return jsonify({"error": "Unauthorized"}), 403

            cursor = conn.cursor()

            cursor.execute("""
                SELECT TeamID, TeamName, Sport, Description
                FROM teams
                WHERE TeamID = ?
            """, (team_id,))
            team_row = cursor.fetchone()

            if not team_row:
                return jsonify({"error": "Team not found"}), 404

            roster_rows = get_team_members(conn, team_id)

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
                "is_coach": is_user_team_coach(conn, user_id, team_id),
                "roster": roster
            }

            return jsonify({"team": team}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Team detail error:", e)
        return jsonify({"error": str(e)}), 500


# -------------------------
# LIST ALL TEAMS
# -------------------------
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