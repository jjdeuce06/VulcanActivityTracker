from flask import Blueprint, request, jsonify
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

team_api = Blueprint('team_api', __name__)

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


@team_api.route("/invite", methods=["POST"])
def invite_to_team():
    try:
        data = request.get_json() or {}
        username = data.get("username")  # coach username
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
    
@team_api.route("/teamdetail", methods=["POST"])
def team_detail():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        team_id = data.get("team_id")

        print("teamdetail payload:", data)

        if not team_id:
            return jsonify({"error": "Missing team_id"}), 400

        demo_teams = {
            "mens_soccer": {
                "id": "mens_soccer",
                "name": "Men's Soccer",
                "sport": "Soccer",
                "description": "Official private team dashboard for Men's Soccer.",
                "coach_user_id": "demo-coach-id",
                "coach_username": "Coach Demo",
                "roster": [
                    {"user_id": "1", "username": "Coach Demo", "role": "coach", "status": "accepted"},
                    {"user_id": "2", "username": "Player One", "role": "player", "status": "accepted"},
                    {"user_id": "3", "username": "Player Two", "role": "player", "status": "accepted"},
                    {"user_id": "4", "username": "Player Three", "role": "player", "status": "accepted"}
                ]
            },
            "mens_basketball": {
                "id": "mens_basketball",
                "name": "Men's Basketball",
                "sport": "Basketball",
                "description": "Official private team dashboard for Men's Basketball.",
                "coach_user_id": "demo-coach-id",
                "coach_username": "Coach Demo",
                "roster": [
                    {"user_id": "1", "username": "Coach Demo", "role": "coach", "status": "accepted"},
                    {"user_id": "5", "username": "Guard One", "role": "player", "status": "accepted"},
                    {"user_id": "6", "username": "Forward One", "role": "player", "status": "accepted"}
                ]
            }
        }

        team = demo_teams.get(team_id)

        if not team:
            return jsonify({"error": "Team not found"}), 404

        return jsonify({"team": team}), 200

    except Exception as e:
        print("Team detail error:", e)
        return jsonify({"error": str(e)}), 500
