from flask import Flask, request, jsonify, Blueprint
from argon2 import PasswordHasher
from server.database.connect import get_db_connection
from server.controllers.login_store import store_login, fetch_login
login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods =['POST'])
def login():
    print("enter login api")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    print("Recived: ", username, password)
    ph = PasswordHasher()
    stored_hash = ph.hash(password)
    print("stored hash:", stored_hash)

    with get_db_connection() as conn:
        store_login(conn, username, stored_hash)
    print("Login Credentails Stored Successfully")


    return jsonify({"status": "ok"})


@login_api.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password hash"}), 400
    
    with get_db_connection() as conn:
        stored_hash = fetch_login(conn, username)
    if not stored_hash:
        return jsonify({"error": "Invalid username or password"}), 401
    

    ph = PasswordHasher()
    try:
        if ph.verify(stored_hash, password):
            return jsonify({"message": "Login successful"}), 200
    except:
        return jsonify({"error": "Invalid username or password"}), 401


