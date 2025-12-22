from flask import Flask, request, jsonify, Blueprint
#from flask_cors import CORS
#from argon2 import PasswordHasher
#from blueprints.blue import login_api
login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods =['POST'])
def login():
    print("enter login api")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    print("Recived: ", username, password)
    return jsonify({"status": "ok"})

