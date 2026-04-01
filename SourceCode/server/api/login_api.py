from flask import Flask, request, jsonify, Blueprint,session
from argon2 import PasswordHasher
from server.database.connect import get_db_connection
from server.controllers.login_store import store_login, fetch_login, fetch_all_users
from server.database.team_queries import link_coach_to_team, fetch_user_by_username
from server.database.team_queries import assign_coach_role_if_match
login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods=['POST'])
def login():
    print("enter login api")
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Missing email, username, or password"}), 400

    ph = PasswordHasher()
    stored_hash = ph.hash(password)

    with get_db_connection() as conn:
        existing_users = fetch_all_users(conn)
        if username in existing_users:
            return jsonify({"error": "Username already exists"}), 400

        store_login(conn, email, username, stored_hash)
        print("Login credentials stored successfully")

        # fetch inserted user so we can get real UserID
        new_user = fetch_user_by_username(conn, username)
        if not new_user:
            return jsonify({"error": "User created but could not be fetched"}), 500

        link_coach_to_team(conn, new_user.UserID, email)
        

    return jsonify({"status": "ok"}), 200

@login_api.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    with get_db_connection() as conn:
        user = fetch_user_by_username(conn, username)   

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    ph = PasswordHasher()
    try:
        if ph.verify(user.PasswordHash, password):
            # after password is verified
            session["user_id"] = str(user.UserID)
            session["username"] = user.Username
            session["email"] = user.Email

            print("\n=== LOGIN DEBUG ===")
            print("UserID:", user.UserID)
            print("Username:", user.Username)
            print("Email:", user.Email)

            assign_coach_role_if_match(conn, user.UserID, user.Email)
            link_coach_to_team(conn, user.UserID, user.Email)

            print(f"User {user.Username} logged in successfully")
            print("DEBUG session after login:", dict(session))

            print("\n=== LOGIN DEBUG ===")
            print("UserID (should be UUID):", user.UserID)
            print("Email:", user.Email)
            print("====================\n")

            return jsonify({
                "message": "Login successful",
                "username": user.Username
            }), 200
        

    except Exception:
        return jsonify({"error": "Invalid username or password"}), 401

@login_api.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("email", None)
    return jsonify({"message": "Logged out successfully"}), 200
