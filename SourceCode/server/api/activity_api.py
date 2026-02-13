from flask import Flask, request, jsonify, Blueprint
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.activity_store import insert_activity, get_user_activities, get_public_activities
import pyodbc
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
                #print("Activity data:", data)

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
            #print(activities)
        finally:
            conn.close()  #close conn
    except Exception as e:
        print("Error in enter_activity route:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success","activities": activities}), 200

@activity_api.route('/fillDashAct', methods=['POST'])
def fill_Dashactivity():

    try:
        data = request.get_json()
        username = data.pop("username", None)
        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
        
            if not user_id:
                return jsonify({"error": "User not found"}), 404
            
            activities = get_user_activities(conn, user_id)
        finally:
            conn.close()  #close conn
    except Exception as e:
        print("Error in enter_activity route:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success","activities": activities}), 200


@activity_api.route('/fillFrAct', methods=['POST'])
def fill_FriendActivity():

    try:
        data = request.get_json()
        username = data.pop("username", None)
        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
        
            if not user_id:
                return jsonify({"error": "User not found"}), 404
            
            activities = get_public_activities(conn, user_id)

        finally:
            conn.close()  #close conn
    except Exception as e:
        print("Error in enter_activity route:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success","activities": activities}), 200



#----------------MAKE OWN API FILE-----------------
@activity_api.route('/publicleaderboard', methods=['GET'])
def public_leaderboard():
    try:
        sport_type = request.args.get("sport_type")  # optional filter

        conn = get_db_connection()
        try:
            rows = get_public_leaderboard(conn, sport_type=sport_type)
        finally:
            conn.close()

        # define score here if you want (example: score = totalMinutes)
        for r in rows:
            r["score"] = r["totalMinutes"]

        return jsonify({"status": "success", "leaderboard": rows}), 200

    except Exception as e:
        print("Error in public_leaderboard:", e)
        return jsonify({"error": str(e)}), 500

def get_public_leaderboard(conn, sport_type=None):
    print("sport type: ", sport_type)
    params = []
    sql = """
        SELECT
            u.Username AS name,
            COUNT(a.ActivityID) AS totalActivities,
            COALESCE(SUM(a.Duration), 0) AS totalMinutes,

            (
                SELECT
                a.ActivityType AS activityType,
                a.Duration AS duration,
                a.Details AS details
                FROM activity a
                WHERE a.UserID = u.UserID
                AND a.Visibility = 'public'
                FOR JSON PATH
            ) AS activities
            FROM [user] u
            LEFT JOIN activity a
            ON a.UserID = u.UserID
            AND a.Visibility = 'public'
            GROUP BY u.Username, u.UserID
            ORDER BY totalMinutes DESC;
    """

    cur = conn.cursor()
    cur.execute(sql, params)
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def get_specific_sport_data(conn, sport):
    pass
def get_specific_sport_data(conn, sport):
    pass


