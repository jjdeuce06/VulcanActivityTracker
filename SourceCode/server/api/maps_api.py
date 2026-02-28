from flask import Flask, request, jsonify, Blueprint, session
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.map_store import add_route, get_user_routes, delete_route
import pyodbc
map_api = Blueprint('map_api', __name__)


# @map_api.route('/store_map_routes', methods=['POST'])
# def storeMapRoutes():
#     try:

#         data = request.get_json()
#         username = session.get("user_id", None)
#         route_name = data.get("route_name")
#         distance = data.get("distance")
#         coordinates = data.get("coordinates")

#         print("user from maps api:", username)

#         conn = get_db_connection()
#         try:
#             user_id = get_user_id(conn, username)

#             if not user_id:
#                 return jsonify({"error": "User not found"}), 404
#             if not route_name or distance is None or not coordinates:
#                 return jsonify({"error": "Missing required fields"}), 400
            
#             result = add_route(conn, user_id, route_name, distance, coordinates)

#             if not result["success"]:
#                 return jsonify({"error": result["error"]}), 500

        
#             return jsonify({"status": "success"}), 201

#         finally:
#             conn.close()  # safely close connection
#     except Exception as e:
#             print("Error in storeMapRoutes route:", e)
#             return jsonify({"error": str(e)}), 500

@map_api.route('/store_map_routes', methods=['POST'])
def storeMapRoutes():
    data = request.get_json()
    username = session.get("user_id", None)
    
    conn = get_db_connection()
    user_id = get_user_id(conn, username)
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    result = add_route(
        conn,
        user_id,
        data.get("name"),
        data.get("distance"),
        data.get("coordinates")
    )

    conn.close()

    return jsonify(result)