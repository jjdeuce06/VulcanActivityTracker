import json
# ----------------------------------
# ADD / SAVE ROUTE
# ----------------------------------
def add_route(conn, user_id: str, route_name: str, distance: float, coordinates: list) -> dict:
    try:
        cursor = conn.cursor()

        coordinates_json = json.dumps(coordinates)

        cursor.execute("""
            INSERT INTO maps (UserID, RouteName, DistanceMiles, MapData)
            OUTPUT INSERTED.MapID
            VALUES (?, ?, ?, ?)
        """, (user_id, route_name, distance, coordinates_json))

        new_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()

        return {
            "success": True,
            "route_id": str(new_id)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ----------------------------------
# GET ROUTES FOR USER
# ----------------------------------
def get_user_routes(conn, user_id: str) -> dict:
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MapID, RouteName, DistanceMiles, MapData
            FROM maps
            WHERE UserID = ?
            ORDER BY MapID DESC
        """, (user_id,))

        routes = []

        rows = cursor.fetchall()
        for row in rows:
            routes.append({
                "id": str(row.MapID),
                "name": row.RouteName,
                "distance": float(row.DistanceMiles),
                "coordinates": json.loads(row.MapData)
            })

        cursor.close()

        return {
            "success": True,
            "routes": routes
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ----------------------------------
# DELETE ROUTE
# ----------------------------------
def delete_route(conn, user_id: str, RouteName: str) -> dict:
    try:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM maps WHERE RouteName = ? AND UserID = ?", (RouteName, user_id))
        conn.commit()

        cursor.close()

        return {"success": True}

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }