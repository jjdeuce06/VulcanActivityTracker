from flask import Flask, request, jsonify, Blueprint, session
import os
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.map_store import add_route, get_user_routes, delete_route
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Blueprint for map-related routes
map_api = Blueprint('map_api', __name__)


@map_api.route('/store_map_routes', methods=['POST'])
def storeMapRoutes():
    # Get request data
    data = request.get_json()

    # Get current user from session (stored as user_id)
    username = session.get("user_id", None)
    
    # Open DB connection
    conn = get_db_connection()

    # Store route in database
    result = add_route(
        conn,
        username,
        data.get("name"),
        data.get("distance"),
        data.get("coordinates")
    )

    # Close connection
    conn.close()

    # Return result of insert
    return jsonify(result)


@map_api.route('/get_user_routes', methods=['GET'])
def getUserRoutes():
    try:
        # Get current user from session
        username = session.get("user_id", None)

        # Debug print
        print("Username in getMapRoutes:", username)
        
        # Open DB connection
        conn = get_db_connection()

        # Fetch all routes for user
        result = get_user_routes(conn, username)

        # Close connection
        conn.close()

        return jsonify({"success": True, "maps": result})

    except Exception as e:
        # Handle errors
        return jsonify(success=False, error=str(e))


@map_api.route('/delete_route', methods=['POST'])
def deleteRoute():
    try:
        # Get request data
        data = request.get_json()
        RouteName = data.get("name")

        # Get current user from session
        user_id = session.get("user_id", None)# the user name is id here now due to merge
        print("username in deleteRoute:", user_id)

        # Open DB connection
        conn = get_db_connection()


        # Validate user
        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        # Delete route from DB
        result = delete_route(conn, user_id, RouteName)

        # Close connection
        conn.close()

        return jsonify(result)

    except Exception as e:
        return jsonify(success=False, error=str(e))


@map_api.route('/send-weatherkey', methods=['POST'])
def sendweatherkey():
    # Return weather API key from environment variables
    return jsonify({
        "key": os.getenv("WEATHER_API_KEY")
    })