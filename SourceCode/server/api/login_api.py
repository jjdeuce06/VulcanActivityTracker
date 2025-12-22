from flask import Flask, request, jsonify
#from flask_cors import CORS
#from argon2 import PasswordHasher
from blueprints.blue import login_api


@login_api.route('/login', methods =['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    print("Recived: ", username, password)
    return jsonify({"message": "User registered successfully"}), 201

