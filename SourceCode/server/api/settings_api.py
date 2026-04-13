from flask import Blueprint, request, jsonify, session
from server.controllers.user_store import get_user_id, get_user_email
from server.controllers.activity_store import get_user_activities
from server.controllers.challenges_store import get_user_challenges
from server.controllers.club_store import get_user_clubs
import pyodbc

from server.database.connect import get_db_connection

# Blueprint for settings-related routes
settings_api = Blueprint("settings_api", __name__)


# ---------------- CHANGE USERNAME ----------------
@settings_api.route("/change-username", methods=["POST"])
def change_username():

    # Get request data
    data = request.get_json()
    new_username = data.get("username")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get current user from session (stored as user_id)
    current_username = session.get("user_id")

    # Fetch user record
    cursor.execute("SELECT UserID, Username FROM [user] WHERE Username = ?", current_username)
    user_id = cursor.fetchone().UserID

    # Update username in database
    cursor.execute("""
        UPDATE [user]
        SET Username = ?
        WHERE UserID = ?
    """, new_username, user_id)

    # Update session with new username
    session["username"] = new_username

    conn.commit()

    return jsonify({
        "success": True,
        "message": "Username updated successfully"
    })


# ---------------- DELETE ACCOUNT ----------------
@settings_api.route("/delete-account", methods=["DELETE"])
def delete_account():

    # Get current username from session
    username = session.get("username")

    if not username:
        return jsonify(success=False, message="Not logged in"), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user record
    cursor.execute("SELECT UserID, Username FROM [user] WHERE Username = ?", username)
    delete_user = cursor.fetchone()

    if not delete_user:
        return jsonify(success=False, message="User not found"), 404

    actual_user_id = str(delete_user.UserID)

    # Debug logs
    print("Username to delete:", username)
    print("User ID to delete:", actual_user_id)

    try:
        # Begin transaction
        conn.autocommit = False

        # ---------------- 1) HANDLE CLUBS ----------------
        cursor.execute("SELECT ClubID, Members, CreatorUserID FROM clubs")
        clubs = cursor.fetchall()

        for club in clubs:
            club_id = club.ClubID
            members = club.Members or ""
            creator = str(club.CreatorUserID) if club.CreatorUserID else ""

            # If user is creator → delete club
            if creator == actual_user_id:
                cursor.execute("DELETE FROM clubs WHERE ClubID = ?", club_id)
                continue

            # Otherwise remove user from members list
            member_ids = [m.strip() for m in members.split(",") if m.strip()]
            member_ids = [mid for mid in member_ids if mid != actual_user_id]
            new_members = ",".join(member_ids)

            if new_members != members:
                cursor.execute(
                    "UPDATE clubs SET Members = ? WHERE ClubID = ?",
                    new_members, club_id
                )

        print("Processed club delete")

        # ---------------- 2) FIND ACTIVITIES ----------------
        cursor.execute("SELECT ActivityID FROM [activity] WHERE UserID = ?", actual_user_id)
        activity_rows = cursor.fetchall()
        activity_ids = [row.ActivityID for row in activity_rows]

        print("Activity IDs to delete:", activity_ids)

        # ---------------- 3) DELETE ACTIVITY LIKES ----------------
        for activity_id in activity_ids:
            cursor.execute("DELETE FROM [activity_likes] WHERE ActivityID = ?", activity_id)

        print("Processed activity_likes delete")

        # ---------------- 4) DELETE ACTIVITIES ----------------
        cursor.execute("DELETE FROM [activity] WHERE UserID = ?", actual_user_id)
        print("Processed activity delete")

        # ---------------- 5) DELETE USER LIKES ----------------
        cursor.execute("DELETE FROM [likes] WHERE LikedUserID = ?", actual_user_id)
        print("Processed likes delete for LikedUserID")

        # ---------------- 6) DELETE USER ----------------
        cursor.execute("DELETE FROM [user] WHERE UserID = ?", actual_user_id)
        print("Processed user delete")

        # Commit transaction
        conn.commit()

        # Clear session after deletion
        session.clear()

        return jsonify(success=True, message="Account deleted")

    except Exception as e:
        # Rollback on error
        conn.rollback()
        print("DELETE ACCOUNT ERROR:", repr(e))
        return jsonify(success=False, message=str(e)), 500

    finally:
        # Restore autocommit and close connection
        conn.autocommit = True
        conn.close()


# ---------------- DASHBOARD STATS ----------------
@settings_api.route("/fillActivityStat", methods=["POST"])
def activity_stat():
    try:
        # Get username from session
        username = session.get("username", None)

        conn = get_db_connection()
        try:
            # Convert username → user_id
            user_id = get_user_id(conn, username)
        
            if not user_id:
                return jsonify({"error": "User not found"}), 404
            
            # Count user activities, challenges, and clubs
            activities = len(get_user_activities(conn, user_id))
            challenges = len(get_user_challenges(conn, user_id))
            clubs = len(get_user_clubs(conn, user_id))

            # Fetch email
            email = get_user_email(conn, user_id)

        finally:
            conn.close()  #close conn

    except Exception as e:
        print("Error in enter_activity route:", e)
        return jsonify({"error": str(e)}), 500
    
    # Debug log
    print (f"User: {username}, Activities: {activities}, Challenges: {challenges}, Clubs: {clubs}, Email: {email}")

    # Return stats
    return jsonify({
        "status": "success",
        "activities": activities, 
        "challenges": challenges, 
        "clubs": clubs,
        "name": username,
        "email": email
    }), 200


# ---------------- GET USER INFO ----------------
@settings_api.route('/get-user-info', methods=['GET'])
def get_user_info():
    # Get username from session
    username = session.get('username') 
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user info
    cursor.execute("""
        SELECT Username, Email
        FROM [user]
        WHERE Username = ?
    """, username)

    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify({"error": "User not found"}), 404

    # Return username + email
    return jsonify({
        "name": row.Username,
        "email": row.Email
    })