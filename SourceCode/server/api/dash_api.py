from flask import Flask, request, jsonify, Blueprint
from server.database.connect import get_db_connection
from server.controllers.login_store import fetch_all_users
from server.controllers.user_store import get_user_id
from server.controllers.friend_store import insert_friend, get_users_friends
from server.controllers.like_store import toggle_like_friend
dash_api = Blueprint('dash_api', __name__)


@dash_api.route('/sendFriendsList', methods =['POST'])
def sendFriendsList():

    data = request.json
    username = data.get("currentUser")

    conn = get_db_connection()
    try:
        #check if usrname exists already
        userID = get_user_id(conn, username)
        existing_users = fetch_all_users(conn)
        existing_friends = get_users_friends(conn, userID)
        print(existing_users)
    finally:
            conn.close()  

    return jsonify({
        "all_users": existing_users,
        "existing_friends": existing_friends
    })



@dash_api.route('/addFriend', methods=['POST'])
def add_friend():
    data = request.json
    username = data.get("currentUser")
    friend_user = data.get("friendUser")
    
    conn = get_db_connection()
    try:

        current_userID = get_user_id(conn, username)
        print("current", current_userID, "friend", friend_user)

        if not current_userID or not friend_user:
            return jsonify({"status": "error", "message": "Missing user"}), 400
        
        insert_friend(conn, current_userID,friend_user )
        print("insert complete")
    finally:
        conn.commit()

    return jsonify({"status": "ok", "added": friend_user})



@dash_api.route("/like", methods=["POST"])
def like_friend():
    data = request.get_json()
    username = data.get("username")
    friend = data.get("friend")
    
    conn = get_db_connection()
    try:
        userID = get_user_id(conn, username)
        friendID = get_user_id(conn, friend)
        print("current", userID, "friend", friendID)

        if not userID or not friendID:
            return jsonify({"status": "error", "message": "Missing user"}), 400
        
        liked, total_likes = toggle_like_friend(conn, userID, friendID)
    finally:
        conn.commit()

    return jsonify({
            "status": "ok",
            "liked": liked,
            "total_likes": total_likes
        })