from flask import Flask, request, jsonify, Blueprint
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.activity_store import insert_activity, get_user_activities
activity_api = Blueprint('activity_api', __name__)


@activity_api.route('/enteractivity', methods=['POST'])
def enter_activity():
    try:
        data = request.get_json()
        username = data.pop("username", None)

        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
            #print("user ID is:", user_id)

            if not user_id:
                return jsonify({"error": "User not found"}), 404

            # unwrap form if present
            if "form" in data:
                data = data["form"]
                print("Activity data:", data)

            # insert activity
            insert_activity(conn, user_id, data)

            return jsonify({"status": "success"}), 201

        finally:
            conn.close()  # safely close connection

    except Exception as e:
        print("Error in enter_activity route:", e)
        return jsonify({"error": str(e)}), 500


@activity_api.route('/fillactivity', methods=['POST'])
def fill_activity():

    try:
        data = request.get_json()
        username = data.pop("username", None)
        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
        
            if not user_id:
                return jsonify({"error": "User not found"}), 404
            
            activities = get_user_activities(conn, user_id)
            print(activities)
        finally:
            conn.close()  #close conn
    except Exception as e:
        print("Error in enter_activity route:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success","activities": activities}), 200
