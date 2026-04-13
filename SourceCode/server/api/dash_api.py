from flask import Flask, request, jsonify, Blueprint, session
from server.database.connect import get_db_connection
from server.controllers.login_store import fetch_all_users
from server.controllers.user_store import get_user_id
from server.controllers.friend_store import insert_friend, get_users_friends
from server.controllers.like_store import toggle_like_friend, check_if_liked, get_total_likes, check_if_thumbs_up, get_total_thumbs_up, toggle_thumbs_up
from server.controllers.club_store import get_user_clubs
from server.controllers.challenges_store import get_dash_challenges

# Blueprint for dashboard-related functionality
dash_api = Blueprint('dash_api', __name__)


@dash_api.route('/sendFriendsList', methods =['POST'])
def sendFriendsList():

    # Get request data
    data = request.json
    username = data.get("currentUser")

    conn = get_db_connection()
    try:
        # Get user ID
        userID = get_user_id(conn, username)

        # Get all users in system
        existing_users = fetch_all_users(conn)

        # Get current user's friends
        existing_friends = get_users_friends(conn, userID)

    finally:
        # Always close connection
        conn.close()  

    # Return users + friend list
    return jsonify({
        "all_users": existing_users,
        "existing_friends": existing_friends
    })


@dash_api.route('/addFriend', methods=['POST'])
def add_friend():
    # Get request data
    data = request.json
    username = data.get("currentUser")
    friend_user = data.get("friendUser")
    
    conn = get_db_connection()
    try:
        # Convert username → user_id
        current_userID = get_user_id(conn, username)

        # Validate inputs
        if not current_userID or not friend_user:
            return jsonify({"status": "error", "message": "Missing user"}), 400
        
        # Insert friend relationship
        insert_friend(conn, current_userID, friend_user)

    finally:
        # Commit changes and close connection
        conn.commit()

    # Return success response
    return jsonify({"status": "ok", "added": friend_user})


@dash_api.route("/like", methods=["POST"])
def like_friend():
    # Get request data
    data = request.get_json()
    username = data.get("username")
    friend = data.get("friend")
    action = data.get("action") #action option

    conn = get_db_connection()
    try:
        # Convert usernames → IDs
        userID = get_user_id(conn, username)
        friendID = get_user_id(conn, friend)

        # Validate users
        if not userID or not friendID:
            return jsonify({"status": "error"}), 400

        # If just fetching like state
        if action == "get":
            liked = check_if_liked(conn, userID, friendID)
            total_likes = get_total_likes(conn, friendID)

        else:
            # Toggle like/unlike
            liked, total_likes = toggle_like_friend(conn, userID, friendID)

        # Get number of friends for this user
        sendFriendNumber = len(get_users_friends(conn, friendID))

    finally:
        # Save changes and close connection
        conn.commit()
        conn.close()

    # Return like status + counts
    return jsonify({
        "status": "ok",
        "liked": liked,
        "total_likes": total_likes,
        "friend_num": sendFriendNumber
    })


@dash_api.route("/likesCount", methods=["POST"])
def get_likes_count():
    # Get request data
    data = request.get_json()
    username = data.get("username")

    conn = get_db_connection()
    try:
        # Convert username → user_id
        userID = get_user_id(conn, username)

        # Validate user
        if not userID:
            return jsonify({"status": "error"}), 400

        # Get total likes for this user
        total_likes = get_total_likes(conn, userID)

    finally:
        conn.close()

    return jsonify({
        "status": "ok",
        "total_likes": total_likes
    })


@dash_api.route("/thumbsUp", methods=["POST"])
def thumbs_up_friend():
    # Get request data
    data = request.get_json()
    username = data.get("username")
    friend = data.get("friend")
    action = data.get("action") #action option
    activity_id = data.get("activity_id")
    
    conn = get_db_connection()
    try:
        # Convert usernames → IDs
        userID = get_user_id(conn, username)
        friendID = get_user_id(conn, friend)

        # Validate users
        if not userID or not friendID:
            return jsonify({"status": "error"}), 400
        
        # Prevent liking own activity
        if str(userID) == str(friendID):
            return jsonify({"status": "error", "message": "You cannot like your own activity"}), 403

        # Fetch like state
        if action == "get":
            liked = check_if_thumbs_up(conn, userID, activity_id)
            total_likes = get_total_thumbs_up(conn, activity_id)

        else:
            # Toggle thumbs up
            liked, total_likes = toggle_thumbs_up(conn, userID, activity_id)

    finally:
        # Save changes and close connection
        conn.commit()
        conn.close()

    return jsonify({
        "status": "ok",
        "liked": liked,
        "total_likes": total_likes
    })


@dash_api.route("/thumbCount", methods=["POST"])
def get_thumb_count():
    # Get request data
    data = request.get_json()
    username = data.get("username")
    activity_id = data.get("activity_id")

    conn = get_db_connection()
    try:
        # Convert username → user_id
        userID = get_user_id(conn, username)

        # Validate user
        if not userID:
            return jsonify({"status": "error"}), 400

        # Get total likes for activity
        total_likes = get_total_thumbs_up(conn, activity_id)

    finally:
        conn.close()

    return jsonify({
        "status": "ok",
        "activity_total_likes": total_likes
    })


@dash_api.route("/fillDashClubs", methods =["POST"])
def fill_dash_clubs():

    # Get request data
    data = request.json
    username = data.get("currentUser")

    conn = get_db_connection()
    try:
        # Convert username → user_id
        userID = get_user_id(conn, username)

        # Get clubs for dashboard
        dash_clubs = get_user_clubs(conn, userID)
       
    finally:
        conn.close()  

    return jsonify({
        "dash_clubs": dash_clubs
    })


@dash_api.route("/fillDashChallenges", methods =["GET"])
def fill_dash_challenges():

    # Get username from session (logged-in user)
    username = session.get("username", None)

    conn = get_db_connection()
    try:
        # Convert username → user_id
        userID = get_user_id(conn, username)

        # Get challenges for dashboard
        dash_challenges = get_dash_challenges(conn, userID)

    finally:
        conn.close()  

    return jsonify({
        "dash_challenge": dash_challenges
    })