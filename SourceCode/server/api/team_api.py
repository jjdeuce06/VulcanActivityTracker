from flask import Blueprint, request, jsonify
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.team_store import get_all_teams, add_member_to_team

team_api = Blueprint('team_api', __name__)

@team_api.route('/listteams', methods=['POST']) #lists every team in the database user is not a member or creator of and calls the get not user teams function
def list_teams():
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

            teams = get_all_teams(conn)
            uid = str(user_id)
            not_user_teams = [t for t in teams if t["creator_user_id"] != uid and uid not in t.get("members", [])]
        finally:
            conn.close()
    except Exception as e:
        print("Error fetching user teams:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "teams": not_user_teams}), 200