#challenges_api.py:
from flask import Blueprint, request, jsonify
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.challenges_store import (
    insert_challenge, get_all_challenges, get_not_user_challenges, get_user_challenges, 
    add_participant_to_challenge, remove_participant_from_challenge, remove_challenge_from_database,
    challenge_name_exists, get_participant_details, get_challenge_leaderboard,
    finalize_expired_challenges, get_visible_not_user_challenges, get_visible_user_challenges,
    get_user_medals
)

# Blueprint for challenge-related routes
challenges_api = Blueprint('challenges_api', __name__)


@challenges_api.route('/createchallenge', methods=['POST']) #create a new challenge route
def create_challenge():
    try:
        # Get request data
        data = request.get_json()
        print("Create challenge payload:", data)

        # Extract fields from request
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

        # Clean up challenge name
        name = name.strip()
        
        conn = get_db_connection()
        try:
            #cnonvert username to user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # Ensure challenge name is unique
            if challenge_name_exists(conn, name):
                return jsonify({"error": "Challenge name already exists. Please choose a unique name."}), 400
            
            # Insert challenge into DB
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
            #close connection
            conn.close()

    except Exception as e:
        print("Error creating challenge:", e)
        return jsonify({"error": str(e)}), 500


@challenges_api.route('/listchallenges', methods=['POST']) #List challenges route
def list_challenges():
    try:
        #Get request data
        data = request.get_json() or {}
        username = data.get("username")

        #Validate username
        if not username:
            return jsonify({"error": "Missing username"}), 400

        conn = get_db_connection()
        try:
            #Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            #Finalize any expired challenges before fetching
            finalize_expired_challenges(conn)

            #Get challenges user is NOT part of
            challenges = get_visible_not_user_challenges(conn, user_id)

        finally:
            conn.close()

    except Exception as e:
        print("Error fetching user challenges:", e)
        return jsonify({"error": str(e)}), 500

    #Return challenge list
    return jsonify({"status": "success", "challenges": challenges}), 200
    

@challenges_api.route('/mychallenges', methods=['POST']) #Lists challenges that the user is a member or creator of
def my_challenges():
    try:
        #Get request data
        data = request.get_json() or {}
        username = data.get("username")

        #Validate username
        if not username:
            return jsonify({"error": "Missing username"}), 400

        conn = get_db_connection()
        try:
            #Convert username to user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            #Finalize expired challenges before fetching
            finalize_expired_challenges(conn)

            #Get user's challenges
            challenges = get_visible_user_challenges(conn, user_id)

            #Get medals earned by user
            medals = get_user_medals(conn, user_id)

        finally:
            #Close connection
            conn.close()

    except Exception as e:
        print("Error fetching user challenges:", e)
        return jsonify({"error": str(e)}), 500

    #Return challenges + medals
    return jsonify({
            "status": "success",
            "challenges": challenges,
            "medals": medals
    }), 200


@challenges_api.route('/join', methods=['POST']) #User joins a challenge and calls the add member to challenge function
def join_challenge():
    try:
        #Get request data
        data = request.get_json() or {}
        username = data.get("username")
        challenge_id = data.get("challenge_id")

        #Validate inputs
        if not username or not challenge_id:
            return jsonify({"error": "Missing username or challenge_id"}), 400

        conn = get_db_connection()
        try:
            #Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            #Add user to challenge
            participants = add_participant_to_challenge(conn, challenge_id, user_id)

        finally:
            conn.close()

        return jsonify({"status": "success", "participants": participants}), 200

    except Exception as e:
        print("Error joining challenge:", e)
        return jsonify({"error": str(e)}), 500
    

@challenges_api.route('/leave', methods=['POST']) #User leaves a challenge and calls the remove member from challenge function
def leave_challenge():
    try:
        # Get request data
        data = request.get_json() or {}
        username = data.get("username")
        challenge_id = data.get("challenge_id")

        # Validate inputs
        if not username or not challenge_id:
            return jsonify({"error": "Missing username or challenge_id"}), 400

        conn = get_db_connection()
        try:
            # Convert username → user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # Remove user from challenge
            participants = remove_participant_from_challenge(conn, challenge_id, user_id)

        finally:
            conn.close()

        return jsonify({"status": "success", "participants": participants}), 200

    except Exception as e:
        print("Error leaving challenge:", e)
        return jsonify({"error": str(e)}), 500
    


@challenges_api.route('/deletechallenge', methods=['POST']) #Deletes challenge route
def delete_challenge():
    try:
        #Get request data
        data = request.get_json()
        print("Delete challenge payload:", data)

        username = data.get("username")
        challenge_id = data.get("challenge_id")
        
        #Validate inputs
        if not username or not challenge_id:
            return jsonify({"error": "Missing username or challenge_id"}), 400

        conn = get_db_connection()
        try:
            #Convert username to user_id
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            #Deletes challenge
            remove_challenge_from_database(conn, challenge_id, user_id)
            return jsonify({"status": "success"}), 201

        finally:
            conn.close()

    except ValueError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print("Error deleting challenge:", e)
        return jsonify({"error": str(e)}), 500
    

@challenges_api.route('/challengedetail', methods=['POST']) #Gets challenge details route
def challenge_detail():
    try:
        #Get request data
        data = request.get_json() or {}
        challenge_name = data.get("challenge_name")

        #Validate input
        if not challenge_name:
            return jsonify({"error": "Missing challenge_name"}), 400

        conn = get_db_connection()
        try:
            #Fetch all challenges
            challenges = get_all_challenges(conn)

            #Find specific challenge by name
            challenge = next((c for c in challenges if c["name"] == challenge_name), None)

            if not challenge:
                return jsonify({"error": "challenge not found"}), 404
            
            #Convert participant IDs to detailed user info
            participant_details = get_participant_details(conn, challenge.get("participants", []))
            challenge["participant_details"] = participant_details

            #Build leaderboard for this challenge
            leaderboard = get_challenge_leaderboard(conn, challenge)
            challenge["leaderboard"] = leaderboard

            #Return full challenge object
            return jsonify({"challenge": challenge}), 200

        finally:
            conn.close()

    except Exception as e:
        print("Error fetching challenge detail:", e)
        return jsonify({"error": str(e)}), 500