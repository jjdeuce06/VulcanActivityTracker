from flask import Flask, request, jsonify, Blueprint
from argon2 import PasswordHasher
from server.database.connect import get_db_connection
from server.controllers.login_store import store_login
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




