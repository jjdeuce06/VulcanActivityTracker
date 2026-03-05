from flask import Blueprint, request, jsonify, session
import pyodbc

from server.database.connect import get_db_connection

settings_api = Blueprint("settings_api", __name__)

# change username
@settings_api.route("/change-username", methods=["POST"])
def change_username():

    data = request.get_json()
    new_username = data.get("username")

    user_id = session.get("user_id")

    conn = get_db_connection()
    cursor = conn.cursor()

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

    user_id = session.get("user_id")
    if not user_id:
        return jsonify(success=False, message="Not logged in"), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT UserID FROM [user] WHERE Username = ?", user_id)
    delete_user = cursor.fetchone()
    if not delete_user:
        return jsonify(success=False, message="User not found"), 404
    
    print("User ID to delete:", delete_user.UserID)

    try:
        conn.autocommit = False

        # 1) CLUBS: remove user from memberships; delete clubs they created
        cursor.execute("SELECT ClubID, Members, CreatorUserID FROM clubs")
        clubs = cursor.fetchall()

        print("Attempting to delete account for user:", user_id)

        for club in clubs:
            club_id = club.ClubID
            members = club.Members or ""
            creator = club.CreatorUserID
            print("no error here 1")

            # Policy: if they created the club, delete the club
            if creator == user_id:
                cursor.execute("DELETE FROM clubs WHERE ClubID = ?", club_id)
                print("no error here 2")
                continue

            # Otherwise remove them from the Members list (comma-separated IDs)
            member_ids = []
            for m in members.split(","):
                m = m.strip()
                if m.isdigit():
                    member_ids.append(int(m))
            print("no error here 3")

            member_ids = [mid for mid in member_ids if mid != int(user_id)]
            new_members = ",".join(str(mid) for mid in member_ids)
            print("no error here 4")


            # Only update if it actually changed
            if new_members != members:
                cursor.execute(
                    "UPDATE clubs SET Members = ? WHERE ClubID = ?",
                    new_members, club_id
                )
            
        print("Processed club delete")

        # 2) ACTIVITIES: delete user activities (rename table if yours differs)
        print("Attempting to delete activities for user:", delete_user.UserID)
        cursor.execute("DELETE FROM activity WHERE UserID = ?", delete_user.UserID)
        print("Processed activity delete")

        # 3) USER: delete the user last
        cursor.execute("DELETE FROM [user] WHERE UserID = ?", delete_user.UserID)
        print("Processed user delete")

        conn.commit()
        session.clear()

        return jsonify(success=True, message="Account deleted")

    except Exception as e:
        conn.rollback()
        return jsonify(success=False, message=str(e)), 500

    finally:
        conn.autocommit = True
        conn.close()