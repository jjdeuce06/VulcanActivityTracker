from flask import Flask, request, jsonify, Blueprint, session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from server.database.connect import get_db_connection
from server.controllers.login_store import (
    store_login,
    fetch_login,
    fetch_all_users,
    fetch_user_by_email,
    fetch_user_by_username
)

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
    hashed_password = ph.hash(password)

    try:
        with get_db_connection() as conn:
            existing_user = fetch_user_by_username(conn, username)
            if existing_user:
                return jsonify({"error": "Username already exists"}), 400

            existing_email = fetch_user_by_email(conn, email)
            if existing_email:
                return jsonify({"error": "Email already exists"}), 400

            store_login(conn, email, username, hashed_password)
            print("Login credentials stored successfully")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("Registration error:", e)
        return jsonify({"error": "Failed to create account"}), 500


@login_api.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    try:
        with get_db_connection() as conn:
            stored_hash = fetch_login(conn, username)

        if not stored_hash:
            return jsonify({"error": "Invalid username or password"}), 401

        ph = PasswordHasher()
        ph.verify(stored_hash, password)

        session["user_id"] = username
        print(f"User {username} logged in successfully in session")
        return jsonify({"message": "Login successful", "username": username}), 200

    except VerifyMismatchError:
        return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Login failed"}), 500


@login_api.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out successfully"}), 200