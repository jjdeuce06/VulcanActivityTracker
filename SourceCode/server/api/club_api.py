from flask import Blueprint, request, jsonify
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.club_store import (
    insert_club, get_all_clubs,get_not_user_clubs, get_user_clubs,
    add_member_to_club, remove_member_from_club, remove_club_from_database,
    usernames_from_userids, get_club_this_week_leaderboard, get_club_last_week_leaders,
    create_club_join_request, cancel_club_join_request,
    get_pending_club_requests_for_owner, get_user_pending_club_request,
    accept_club_join_request, decline_club_join_request,
    get_club_recent_activities
)

# Blueprint for all club-related routes
club_api = Blueprint('club_api', __name__)


@club_api.route('/createclub', methods=['POST']) #gets the data from the request and calls the insert club function
def create_club():
    try:
        # Get JSON request body
        data = request.get_json()
        print("Create club payload:", data)

        # Extract fields from request
        username = data.get("username")
        name = data.get("club_name")
        description = data.get("description")
        sport_type = data.get("sport_type")
        privacy = data.get("privacy", "public")

        # Validate required fields
        if not username or not name or not sport_type:
            return jsonify({"error": "Missing data"}), 400

        # Open DB connection
        conn = get_db_connection()
        try:
            # Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # Insert club into database
            insert_club(conn, user_id, name, description, sport_type, privacy)
            return jsonify({"status": "success"}), 201
        finally:
            # Always close connection
            conn.close()

    except Exception as e:
        print("Error creating club:", e)
        return jsonify({"error": str(e)}), 500


@club_api.route('/listclubs', methods=['POST']) #lists every club in the database user is not a member or creator of and calls the get not user clubs function
def list_clubs():
    try:
        # Get request data
        data = request.get_json() or {}
        username = data.get("username")

        # Validate username
        if not username:
            return jsonify({"error": "Missing username"}), 400

        # Open DB connection
        conn = get_db_connection()
        try:
            # Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # Get clubs user is NOT part of
            clubs = get_not_user_clubs(conn, user_id)

            # Add pending request flag to each club
            for club in clubs:
                club["has_pending_request"] = get_user_pending_club_request(conn, club["id"], str(user_id))

        finally:
            conn.close()

    except Exception as e:
        print("Error fetching user clubs:", e)
        return jsonify({"error": str(e)}), 500

    # Return result
    return jsonify({"status": "success", "clubs": clubs}), 200


@club_api.route('/myclubs', methods=['POST']) #lists clubs that the user is a member or creator of
def my_clubs():
    try:
        # Get request data
        data = request.get_json() or {}
        username = data.get("username")

        # Validate username
        if not username:
            return jsonify({"error": "Missing username"}), 400

        # Open DB connection
        conn = get_db_connection()
        try:
            # Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # Get clubs user IS part of
            clubs = get_user_clubs(conn, user_id)

            # Add pending request flag
            for club in clubs:
                club["has_pending_request"] = get_user_pending_club_request(conn, club["id"], str(user_id))

        finally:
            conn.close()

    except Exception as e:
        print("Error fetching user clubs:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "clubs": clubs}), 200


@club_api.route('/join', methods=['POST']) #user joins a club and calls the add member to club function
def join_club():
    try:
        # Get request data
        data = request.get_json() or {}
        username = data.get("username")
        club_id = data.get("club_id")

        # Validate inputs
        if not username or not club_id:
            return jsonify({"error": "Missing username or club_id"}), 400

        # Open DB connection
        conn = get_db_connection()
        try:
            # Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # Load all clubs and find matching one
            clubs = get_all_clubs(conn)
            club = next((c for c in clubs if str(c["id"]) == str(club_id)), None)
            if not club:
                return jsonify({"error": "Club not found"}), 404

            # Prevent owner from joining their own club
            if str(club.get("creator_user_id")) == str(user_id):
                return jsonify({"error": "Owner is already part of the club"}), 400

            # Private clubs require join request flow
            if club.get("is_private"):
                return jsonify({"error": "Private clubs require an approved join request"}), 403

            # Add member to club
            members = add_member_to_club(conn, club_id, user_id, username)
            return jsonify({"status": "success", "members": members}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Error joining club:", e)
        return jsonify({"error": str(e)}), 500
    

@club_api.route('/leave', methods=['POST']) #user leaves a club and calls the remove member from club function
def leave_club():
    try:
        # Get request data
        data = request.get_json() or {}
        username = data.get("username")
        club_id = data.get("club_id")

        # Validate inputs
        if not username or not club_id:
            return jsonify({"error": "Missing username or club_id"}), 400

        # Open DB connection
        conn = get_db_connection()
        try:
            # Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # Remove user from club
            members = remove_member_from_club(conn, club_id, user_id, username)

        finally:
            conn.close()

        return jsonify({"status": "success", "members": members}), 200

    except Exception as e:
        print("Error leaving club:", e)
        return jsonify({"error": str(e)}), 500


@club_api.route('/deleteclub', methods=['POST']) #deletes club
def delete_club():
    try:
        # Get request data
        data = request.get_json()
        print("Delete club payload:", data)

        username = data.get("username")
        club_id = data.get("club_id")

        # Validate inputs
        if not username or not club_id:
            return jsonify({"error": "Missing username or club_id"}), 400

        # Open DB connection
        conn = get_db_connection()
        try:
            # Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # Delete club
            remove_club_from_database(conn, club_id, user_id)
            return jsonify({"status": "success"}), 201

        finally:
            conn.close()

    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print("Error deleting club:", e)
        return jsonify({"error": str(e)}), 500