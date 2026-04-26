import json

# ----------------------------------
# ADD / SAVE ROUTE
# ----------------------------------
def add_route(conn, user_id: str, route_name: str, distance: float, coordinates: list) -> dict:
    try:
        # Create DB cursor
        cursor = conn.cursor()

        # Convert coordinates list → JSON string for storage
        coordinates_json = json.dumps(coordinates)

        # Insert route into maps table and return new MapID
        cursor.execute("""
            INSERT INTO maps (UserID, RouteName, DistanceMiles, MapData)
            OUTPUT INSERTED.MapID
            VALUES (?, ?, ?, ?)
        """, (user_id, route_name, distance, coordinates_json))

        # Fetch generated MapID
        new_id = cursor.fetchone()[0]

        # Commit transaction
        conn.commit()

        # Close cursor
        cursor.close()

        # Return success response with new route ID
        return {
            "success": True,
            "route_id": str(new_id)
        }

    except Exception as e:
        # Return error response
        return {
            "success": False,
            "error": str(e)
        }


# ----------------------------------
# GET ROUTES FOR USER
# ----------------------------------
def get_user_routes(conn, user_id: str) -> dict:
    try:
        # Create DB cursor
        cursor = conn.cursor()

        # Fetch all routes for a given user
        cursor.execute("""
            SELECT MapID, RouteName, DistanceMiles, MapData
            FROM maps
            WHERE UserID = ?
            ORDER BY MapID DESC
        """, (user_id,))

        routes = []

        # Process query results
        rows = cursor.fetchall()
        for row in rows:
            routes.append({
                "id": str(row.MapID),
                "name": row.RouteName,
                "distance": float(row.DistanceMiles),
                # Convert stored JSON string → Python list
                "coordinates": json.loads(row.MapData)
            })

        # Close cursor
        cursor.close()

        # Return routes
        return {
            "success": True,
            "routes": routes
        }

    except Exception as e:
        # Return error response
        return {
            "success": False,
            "error": str(e)
        }


# ----------------------------------
# DELETE ROUTE
# ----------------------------------
def delete_route(conn, user_id: str, RouteName: str) -> dict:
    try:
        # Create DB cursor
        cursor = conn.cursor()

        # Delete route matching name and user
        cursor.execute(
            "DELETE FROM maps WHERE RouteName = ? AND UserID = ?",
            (RouteName, user_id)
        )

        # Commit transaction
        conn.commit()

        # Close cursor
        cursor.close()

        # Return success response
        return {"success": True}

    except Exception as e:
        # Return error response
        return {
            "success": False,
            "error": str(e)
        }