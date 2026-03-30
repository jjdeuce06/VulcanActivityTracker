#challenges_api.py:
from flask import Blueprint, request, jsonify
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.challenges_store import (insert_challenge, get_all_challenges, get_not_user_challenges, get_user_challenges, 
                                                 add_participant_to_challenge, remove_participant_from_challenge, remove_challenge_from_database,
                                                 challenge_name_exists, get_participant_details, get_challenge_leaderboard,
                                                 finalize_expired_challenges, get_visible_not_user_challenges, get_visible_user_challenges,
                                                    get_user_medals)

challenges_api = Blueprint('challenges_api', __name__)

@challenges_api.route('/createchallenge', methods=['POST'])
def create_challenge():
    try:
        data = request.get_json()
        print("Create challenge payload:", data)

        username = data.get("username")
        name = data.get("challengeName")
        description = data.get("description")
        activity_type = data.get("activityType")
        metric_type = data.get("metricType")
        target_value = data.get("targetValue")
        start_date = data.get("startDate")
        end_date = data.get("endDate")

        # Validate required fields
        if not all([username, name, activity_type, metric_type, target_value, start_date, end_date]):
            return jsonify({"error": "Missing required fields"}), 400

        name = name.strip()
        
        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            if challenge_name_exists(conn, name):
                return jsonify({"error": "Challenge name already exists. Please choose a unique name."}), 400
            
            insert_challenge(
                conn,
                user_id,
                name,
                description,
                activity_type,
                metric_type,
                target_value,
                start_date,
                end_date
            )

            return jsonify({"status": "success"}), 201

        finally:
            conn.close()

    except Exception as e:
        print("Error creating challenge:", e)
        return jsonify({"error": str(e)}), 500

@challenges_api.route('/listchallenges', methods=['POST'])
def list_challenges():
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

            finalize_expired_challenges(conn)
            challenges = get_visible_not_user_challenges(conn, user_id)
        finally:
            conn.close()
    except Exception as e:
        print("Error fetching user challenges:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "challenges": challenges}), 200
    

@challenges_api.route('/mychallenges', methods=['POST']) #lists challenges that the user is a member or creator of
def my_challenges():
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

            finalize_expired_challenges(conn)
            challenges = get_visible_user_challenges(conn, user_id)
            medals = get_user_medals(conn, user_id)
        finally:
            conn.close()
    except Exception as e:
        print("Error fetching user challenges:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({
            "status": "success",
            "challenges": challenges,
            "medals": medals
    }), 200

@challenges_api.route('/join', methods=['POST']) #user joins a challenge and calls the add member to challenge function
def join_challenge():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        challenge_id = data.get("challenge_id")
        if not username or not challenge_id:
            return jsonify({"error": "Missing username or challenge_id"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            participants = add_participant_to_challenge(conn, challenge_id, user_id)
        finally:
            conn.close()

        return jsonify({"status": "success", "participants": participants}), 200

    except Exception as e:
        print("Error joining challenge:", e)
        return jsonify({"error": str(e)}), 500
    
    
@challenges_api.route('/leave', methods=['POST']) #user leaves a challenge and calls the remove member from challenge function
def leave_challenge():
    try:
        data = request.get_json() or {}
        username = data.get("username")
        challenge_id = data.get("challenge_id")
        if not username or not challenge_id:
            return jsonify({"error": "Missing username or challenge_id"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            participants = remove_participant_from_challenge(conn, challenge_id, user_id)
        finally:
            conn.close()

        return jsonify({"status": "success", "participants": participants}), 200

    except Exception as e:
        print("Error leaving challenge:", e)
        return jsonify({"error": str(e)}), 500
    


@challenges_api.route('/deletechallenge', methods=['POST']) #deletes challenge
def delete_challenge():
    try:
        data = request.get_json()
        print("Delete challenge payload:", data)
        username = data.get("username")
        challenge_id = data.get("challenge_id")
        
        if not username or not challenge_id:
            return jsonify({"error": "Missing username or challenge_id"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            remove_challenge_from_database(conn, challenge_id, user_id)
            return jsonify({"status": "success"}), 201
        finally:
            conn.close()

    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print("Error deleting challenge:", e)
        return jsonify({"error": str(e)}), 500
    

@challenges_api.route('/challengedetail', methods=['POST'])
def challenge_detail():
    try:
        data = request.get_json() or {}
        challenge_name = data.get("challenge_name")
        if not challenge_name:
            return jsonify({"error": "Missing challenge_name"}), 400

        conn = get_db_connection()
        try:
            challenges = get_all_challenges(conn)
            challenge = next((c for c in challenges if c["name"] == challenge_name), None)
            if not challenge:
                return jsonify({"error": "challenge not found"}), 404
            
            participant_details = get_participant_details(conn, challenge.get("participants", []))
            challenge["participant_details"] = participant_details

            leaderboard = get_challenge_leaderboard(conn, challenge)
            challenge["leaderboard"] = leaderboard

            return jsonify({"challenge": challenge}), 200
        finally:
            conn.close()
    except Exception as e:
        print("Error fetching challenge detail:", e)
        return jsonify({"error": str(e)}), 500