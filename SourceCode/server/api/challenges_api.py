from flask import Blueprint, request, jsonify
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.challenges_store import insert_challenge, get_all_challenges

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
        start_date = data.get("startDate")
        end_date = data.get("endDate")

        # Validate required fields
        if not all([username, name, activity_type, metric_type, start_date, end_date]):
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            if not user_id:
                return jsonify({"error": "User not found"}), 404

            insert_challenge(
                conn,
                user_id,
                name,
                description,
                activity_type,
                metric_type,
                start_date,
                end_date
            )

            return jsonify({"status": "success"}), 201

        finally:
            conn.close()

    except Exception as e:
        print("Error creating challenge:", e)
        return jsonify({"error": str(e)}), 500

@challenges_api.route('/list', methods=['GET'])
def list_challenges():
    try:
        conn = get_db_connection()
        try:
            challenges = get_all_challenges(conn)
            return jsonify(challenges), 200
        finally:
            conn.close()

    except Exception as e:
        print("Error fetching challenges:", e)
        return jsonify({"error": str(e)}), 500