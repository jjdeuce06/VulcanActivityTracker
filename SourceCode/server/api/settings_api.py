from flask import Blueprint, request, jsonify, session
from server.controllers.user_store import get_user_id, get_user_email
from server.controllers.activity_store import get_user_activities
from server.controllers.challenges_store import get_user_challenges
from server.controllers.club_store import get_user_clubs
import pyodbc

from server.database.connect import get_db_connection

settings_api = Blueprint("settings_api", __name__)

# change username
@settings_api.route("/change-username", methods=["POST"])
def change_username():

    data = request.get_json()
    new_username = data.get("username")

    conn = get_db_connection()
    cursor = conn.cursor()

    current_username = session.get("user_id")
    cursor.execute("SELECT UserID, Username FROM [user] WHERE Username = ?", current_username)
    user_id = cursor.fetchone().UserID

    cursor.execute("""
        UPDATE [user]
        SET Username = ?
        WHERE UserID = ?
    """, new_username, user_id)

    conn.commit()

    return jsonify({
        "success": True,
        "message": "Username updated successfully"
    })


# delete account
# delete account
@settings_api.route("/delete-account", methods=["DELETE"])
def delete_account():

    username = session.get("user_id")
    if not username:
        return jsonify(success=False, message="Not logged in"), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT UserID, Username FROM [user] WHERE Username = ?", username)
    delete_user = cursor.fetchone()
    if not delete_user:
        return jsonify(success=False, message="User not found"), 404

    actual_user_id = str(delete_user.UserID)

    print("Username to delete:", username)
    print("User ID to delete:", actual_user_id)

    try:
        conn.autocommit = False

        # 1) CLUBS
        cursor.execute("SELECT ClubID, Members, CreatorUserID FROM clubs")
        clubs = cursor.fetchall()

        for club in clubs:
            club_id = club.ClubID
            members = club.Members or ""
            creator = str(club.CreatorUserID) if club.CreatorUserID else ""

            if creator == actual_user_id:
                cursor.execute("DELETE FROM clubs WHERE ClubID = ?", club_id)
                continue

            member_ids = [m.strip() for m in members.split(",") if m.strip()]
            member_ids = [mid for mid in member_ids if mid != actual_user_id]
            new_members = ",".join(member_ids)

            if new_members != members:
                cursor.execute(
                    "UPDATE clubs SET Members = ? WHERE ClubID = ?",
                    new_members, club_id
                )

        print("Processed club delete")

        # 2) Find activities
        cursor.execute("SELECT ActivityID FROM [activity] WHERE UserID = ?", actual_user_id)
        activity_rows = cursor.fetchall()
        activity_ids = [row.ActivityID for row in activity_rows]

        print("Activity IDs to delete:", activity_ids)

        # 3) Delete likes on those activities first
        for activity_id in activity_ids:
            cursor.execute("DELETE FROM [activity_likes] WHERE ActivityID = ?", activity_id)

        print("Processed activity_likes delete")

        # 4) Delete activities
        cursor.execute("DELETE FROM [activity] WHERE UserID = ?", actual_user_id)
        print("Processed activity delete")

        # 5) Delete user-related rows in likes table
        cursor.execute("DELETE FROM [likes] WHERE LikedUserID = ?", actual_user_id)
        print("Processed likes delete for LikedUserID")

        # Optional: if your likes table also stores who gave the like
        # cursor.execute("DELETE FROM [likes] WHERE LikingUserID = ?", actual_user_id)
        # print("Processed likes delete for LikingUserID")

        # 6) Delete user
        cursor.execute("DELETE FROM [user] WHERE UserID = ?", actual_user_id)
        print("Processed user delete")

        conn.commit()
        session.clear()

        return jsonify(success=True, message="Account deleted")

    except Exception as e:
        conn.rollback()
        print("DELETE ACCOUNT ERROR:", repr(e))
        return jsonify(success=False, message=str(e)), 500

    finally:
        conn.autocommit = True
        conn.close()


@settings_api.route("/fillActivityStat", methods=["POST"])
def activity_stat():
    try:
        username = session.get("user_id", None)
        conn = get_db_connection()
        try:
            user_id = get_user_id(conn, username)
        
            if not user_id:
                return jsonify({"error": "User not found"}), 404
            
            activities = len(get_user_activities(conn, user_id))
            challenges = len(get_user_challenges(conn, user_id))
            clubs = len(get_user_clubs(conn, user_id))
            email = get_user_email(conn, user_id)
        finally:
            conn.close()  #close conn
    except Exception as e:
        print("Error in enter_activity route:", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success",
                    "activities": activities, 
                    "challenges": challenges, 
                    "clubs": clubs,
                    "name": username,
                    "email": email }), 200