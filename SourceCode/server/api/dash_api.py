from flask import Flask, request, jsonify, Blueprint
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.activity_store import insert_activity
dash_api = Blueprint('dash_api', __name__)


@dash_api.route('/enteractivity', methods =['POST'])
def enter_activity():
    try:
        data = request.get_json() #form 
        username = data.pop("username", None)  # frontend sends username

        print("this is: ", data, username)

        conn = get_db_connection()
        user_id = get_user_id(conn, username)
        print("user ID is: ", user_id)

        if not user_id:
            return jsonify({"error": "User not found"}), 404

        insert_activity(user_id, data)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
