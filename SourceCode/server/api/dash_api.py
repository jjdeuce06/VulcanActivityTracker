from flask import Flask, request, jsonify, Blueprint
from server.database.connect import get_db_connection
from server.controllers.login_store import fetch_all_users
dash_api = Blueprint('dash_api', __name__)


@dash_api.route('/sendFriendsList', methods =['GET'])
def sendFriendsList():

    with get_db_connection() as conn:
        #check if usrname exists already
        existing_users = fetch_all_users(conn)
        print(existing_users)

    return jsonify(existing_users)