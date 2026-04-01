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
club_api = Blueprint('club_api', __name__)

@club_api.route('/createclub', methods=['POST']) #gets the data from the request and calls the insert club function
def create_club():
    try:
        data = request.get_json()
        print("Create club payload:", data)

        username = data.get("username")
        name = data.get("club_name")
        description = data.get("description")
        sport_type = data.get("sport_type")
        privacy = data.get("privacy", "public")

        if not username or not name or not sport_type:
            return jsonify({"error": "Missing data"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            insert_club(conn, user_id, name, description, sport_type, privacy)
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
            for club in clubs:
                club["has_pending_request"] = get_user_pending_club_request(conn, club["id"], str(user_id))
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

            clubs = get_all_clubs(conn)
            club = next((c for c in clubs if str(c["id"]) == str(club_id)), None)
            if not club:
                return jsonify({"error": "Club not found"}), 404

            if str(club.get("creator_user_id")) == str(user_id):
                return jsonify({"error": "Owner is already part of the club"}), 400

            if club.get("is_private"):
                return jsonify({"error": "Private clubs require an approved join request"}), 403

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
        data = request.get_json()
        print("Delete club payload:", data)
        username = data.get("username")
        club_id = data.get("club_id")
        
        if not username or not club_id:
            return jsonify({"error": "Missing username or club_id"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            remove_club_from_database(conn, club_id, user_id)
            return jsonify({"status": "success"}), 201
        finally:
            conn.close()

    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print("Error deleting club:", e)
        return jsonify({"error": str(e)}), 500
    
@club_api.route('/clubdetail', methods=['POST'])
def club_detail():
    try:
        data = request.get_json() or {}
        club_id = data.get("club_id")
        username = data.get("username")

        if not club_id:
            return jsonify({"error": "Missing club_id"}), 400

        conn = get_db_connection()
        try:
            clubs = get_all_clubs(conn)
            club = next(
                (c for c in clubs if str(c["id"]).strip() == str(club_id).strip()),
                None
            )

            if not club:
                return jsonify({"error": "Club not found"}), 404

            owner_and_members = [str(club.get("creator_user_id"))] + [
                str(uid) for uid in club.get("members", [])
            ]
            owner_and_members = list(dict.fromkeys(owner_and_members))

            club["member_usernames"] = usernames_from_userids(conn, owner_and_members)
            club["total_members"] = len(owner_and_members)

            club["is_owner"] = False
            club["is_member"] = False
            club["has_pending_request"] = False
            club["can_view_private_content"] = not club.get("is_private", False)

            if username:
                user_id = get_user_id(conn, username)
                if user_id:
                    uid = str(user_id)

                    club["is_owner"] = str(club.get("creator_user_id")) == uid
                    club["is_member"] = uid in owner_and_members
                    club["has_pending_request"] = get_user_pending_club_request(
                        conn,
                        club["id"],
                        uid
                    )

                    if club["is_owner"] or club["is_member"] or not club.get("is_private", False):
                        club["can_view_private_content"] = True

            if club["can_view_private_content"]:
                club["this_week_leaderboard"] = get_club_this_week_leaderboard(conn, club)
                club["last_week_leaders"] = get_club_last_week_leaders(conn, club)
                club["recent_activity"] = get_club_recent_activities(conn, club)
            else:
                club["this_week_leaderboard"] = []
                club["last_week_leaders"] = []
                club["recent_activity"] = []
                club["member_usernames"] = []
                club["total_members"] = None

            return jsonify({"club": club}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Error fetching club detail:", e)
        return jsonify({"error": str(e)}), 500
    
@club_api.route('/requestjoin', methods=['POST'])
def request_join_club():
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

            clubs = get_all_clubs(conn)
            club = next((c for c in clubs if str(c["id"]) == str(club_id)), None)
            if not club:
                return jsonify({"error": "Club not found"}), 404

            uid = str(user_id)
            owner_id = str(club.get("creator_user_id"))
            member_ids = [owner_id] + [str(m) for m in club.get("members", [])]

            if not club.get("is_private"):
                return jsonify({"error": "Club is not private"}), 400

            if uid == owner_id:
                return jsonify({"error": "Owner cannot request to join their own club"}), 400

            if uid in member_ids:
                return jsonify({"error": "User is already a member"}), 400

            if get_user_pending_club_request(conn, club_id, uid):
                return jsonify({"error": "Join request already pending"}), 400

            create_club_join_request(conn, club_id, user_id, club["creator_user_id"])
            return jsonify({"status": "success"}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Request join club error:", e)
        return jsonify({"error": str(e)}), 500


@club_api.route('/cancelrequest', methods=['POST'])
def cancel_join_request():
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

            cancel_club_join_request(conn, club_id, user_id)
            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Cancel join request error:", e)
        return jsonify({"error": str(e)}), 500


@club_api.route('/clubrequests', methods=['POST'])
def club_requests_for_owner():
    try:
        data = request.get_json() or {}
        username = data.get("username")

        if not username:
            return jsonify({"error": "Missing username"}), 400

        conn = get_db_connection()
        try:
            owner_user_id = get_user_id(conn, username)
            if not owner_user_id:
                return jsonify({"error": "User not found"}), 404

            requests = get_pending_club_requests_for_owner(conn, owner_user_id)
            return jsonify({"requests": requests}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Club requests error:", e)
        return jsonify({"error": str(e)}), 500


@club_api.route('/acceptrequest', methods=['POST'])
def accept_club_request_route():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        club_id = data.get("club_id")
        requesting_username = data.get("requesting_username")

        if not username or not club_id or not requesting_username:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            owner_user_id = get_user_id(conn, username)
            requesting_user_id = get_user_id(conn, requesting_username)

            if not owner_user_id or not requesting_user_id:
                return jsonify({"error": "User not found"}), 404

            accept_club_join_request(conn, club_id, requesting_user_id, owner_user_id)
            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Accept club request error:", e)
        return jsonify({"error": str(e)}), 500


@club_api.route('/declinerequest', methods=['POST'])
def decline_club_request_route():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        club_id = data.get("club_id")
        requesting_username = data.get("requesting_username")

        if not username or not club_id or not requesting_username:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            owner_user_id = get_user_id(conn, username)
            requesting_user_id = get_user_id(conn, requesting_username)

            if not owner_user_id or not requesting_user_id:
                return jsonify({"error": "User not found"}), 404

            decline_club_join_request(conn, club_id, requesting_user_id, owner_user_id)
            return jsonify({"status": "success"}), 200
        finally:
            conn.close()

    except Exception as e:
        print("Decline club request error:", e)
        return jsonify({"error": str(e)}), 500