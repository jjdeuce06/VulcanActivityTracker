from flask import Flask, request, jsonify, Blueprint, session
from server.database.connect import get_db_connection
from server.controllers.user_store import get_user_id
from server.controllers.map_store import add_route, get_user_routes, delete_route
map_api = Blueprint('map_api', __name__)

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


@map_api.route('/get_user_routes', methods=['GET'])
def getUserRoutes():
    try:

        username = session.get("user_id", None)
        
        conn = get_db_connection()
        user_id = get_user_id(conn, username)
        if not user_id:
            return jsonify({"error": "Not logged in"}), 401

        result = get_user_routes(conn, user_id)
        conn.close()
        return jsonify({"success": True, "maps": result})
    except Exception as e:
        return jsonify(success=False, error=str(e))