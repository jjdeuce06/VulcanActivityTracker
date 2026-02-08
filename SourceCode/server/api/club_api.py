from flask import Blueprint, request, jsonify
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.club_store import insert_club, get_all_clubs,get_not_user_clubs, get_user_clubs, add_member_to_club, remove_member_from_club

club_api = Blueprint('club_api', __name__)

@club_api.route('/createclub', methods=['POST']) #gets the data from the request and calls the insert club function
def create_club():
    try:
        data = request.get_json()
        print("Create club payload:", data)
        username = data.get("username")
        name = data.get("club_name")
        description = data.get("description")
        
        if not username or not name:
            return jsonify({"error": "Missing data"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            insert_club(conn, user_id, name, description)
            return jsonify({"status": "success"}), 201
        finally:
            conn.close()

    except Exception as e:
        print("Error creating club:", e)
        return jsonify({"error": str(e)}), 500


@club_api.route('/listclubs', methods=['POST']) #lists every club in the database user is not a member or creator of and calls the get not user clubs function
def list_clubs():
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

            clubs = get_not_user_clubs(conn, user_id)
        finally:
            conn.close()
    except Exception as e:
        print("Error fetching user clubs:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "clubs": clubs}), 200


@club_api.route('/myclubs', methods=['POST']) #lists clubs that the user is a member or creator of
def my_clubs():
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

            clubs = get_user_clubs(conn, user_id)
        finally:
            conn.close()
    except Exception as e:
        print("Error fetching user clubs:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "clubs": clubs}), 200


@club_api.route('/join', methods=['POST']) #user joins a club and calls the add member to club function
def join_club():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        club_id = data.get("club_id")
        if not username or not club_id:
            return jsonify({"error": "Missing username or club_id"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            members = add_member_to_club(conn, club_id, user_id)
        finally:
            conn.close()

        return jsonify({"status": "success", "members": members}), 200

    except Exception as e:
        print("Error joining club:", e)
        return jsonify({"error": str(e)}), 500
    
@club_api.route('/leave', methods=['POST']) #user leaves a club and calls the remove member from club function
def leave_club():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        club_id = data.get("club_id")
        if not username or not club_id:
            return jsonify({"error": "Missing username or club_id"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            members = remove_member_from_club(conn, club_id, user_id)
        finally:
            conn.close()

        return jsonify({"status": "success", "members": members}), 200

    except Exception as e:
        print("Error leaving club:", e)
        return jsonify({"error": str(e)}), 500