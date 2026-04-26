from flask import Flask, request, jsonify
import pyodbc
import json
from datetime import datetime


# ---------------- INSERT ACTIVITY ----------------
def insert_activity(conn, user_id: str, data: dict):
    print("enter insert")
    try:
        # Split common fields vs sport-specific fields
        common_fields = ['activity_type', 'date', 'duration', 'calories_burned', 'visibility', 'notes']
        activity_common = {k: data.get(k) for k in common_fields}

        # Everything else is considered sport-specific data
        sport_specific = {k: v for k, v in data.items() if k not in common_fields}

        # Debug logging
        print("Activity common fields:", activity_common)
        print("Sport-specific fields:", sport_specific)

        # ---------------- CONVERT NUMERIC VALUES ----------------
        # Convert duration and calories to float if present
        duration = float(activity_common.get('duration')) if activity_common.get('duration') is not None else None
        calories = float(activity_common.get('calories_burned')) if activity_common.get('calories_burned') is not None else None

        # ---------------- HANDLE DATE ----------------
        # Convert incoming date string → datetime object
        date_str = activity_common.get('date')
        try:
            activity_date = datetime.fromisoformat(date_str) if date_str else datetime.now()
        except ValueError:
            print(f"Invalid date format: {date_str}, using current time instead")
            activity_date = datetime.now()

        # ---------------- SERIALIZE SPORT-SPECIFIC DATA ----------------
        # Convert dictionary → JSON string for DB storage
        try:
            details_json = json.dumps(sport_specific)
        except Exception as e:
            print("Error serializing sport-specific fields:", e)
            details_json = "{}"

        # ---------------- INSERT INTO DATABASE ----------------
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO [activity] 
            (UserID, ActivityType, ActivityDate, Duration, CaloriesBurned, Visibility, Notes, Details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        user_id,
        activity_common.get('activity_type'),
        activity_date,
        duration,
        calories,
        activity_common.get('visibility', 'private'),
        activity_common.get('notes'),
        details_json
        )

        # Commit transaction
        conn.commit()
        print("Activity inserted successfully")

    except Exception as e:
        print("Insert activity error:", e)
        raise

    finally:
        # Always close cursor
        cursor.close()


# ---------------- GET USER ACTIVITIES ----------------
def get_user_activities(conn, user_id: str):
    print("enter fill A table")

    cursor = conn.cursor()

    try:
        # Fetch all activities for a user
        cursor.execute("""
            SELECT
                ActivityType,
                ActivityDate,
                Duration,
                CaloriesBurned,
                Visibility,
                Notes,
                Details,
                ActivityID        
            FROM activity
            WHERE UserID = ?
            ORDER BY ActivityDate DESC
        """, (user_id,))

        rows = cursor.fetchall()
        activities = []

        for row in rows:
            details = {}

            # ---------------- PARSE JSON DETAILS ----------------
            # Convert stored JSON string → dictionary
            if row.Details:
                try:
                    details = json.loads(row.Details)
                except json.JSONDecodeError:
                    print("Invalid JSON in Details column")

            # Build activity object
            activity = {
                "activity_type": row.ActivityType,
                "date": row.ActivityDate.isoformat(),
                "duration": row.Duration,
                "calories_burned": row.CaloriesBurned,
                "visibility": row.Visibility,
                "notes": row.Notes,
                "activity_id": str(row.ActivityID)
            }

            # Merge sport-specific fields into main object
            activity.update(details)

            activities.append(activity)

        return activities

    except Exception as e:
        print("Fetch activity error:", e)
        raise

    finally:
        # Always close cursor
        cursor.close()


# ---------------- GET PUBLIC ACTIVITIES ----------------
def get_public_activities(conn, user_id):
    cursor = conn.cursor()

    # Query only public activities for a user
    query = """
        SELECT ActivityID, ActivityType, ActivityDate, Duration,
               CaloriesBurned, Visibility, Notes, Details
        FROM activity
        WHERE UserID = ? AND Visibility = 'public'
        ORDER BY ActivityDate DESC
    """

    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    activities = []

    for row in rows:
        details = {}

        # Parse JSON details if present
        if row.Details:
            try:
                details = json.loads(row.Details)
            except:
                pass

        # Build activity object
        activity = {
            "activity_type": row.ActivityType,
            "date": row.ActivityDate.isoformat() if row.ActivityDate else None,
            "duration": row.Duration,
            "calories_burned": row.CaloriesBurned,
            "visibility": row.Visibility,
            "notes": row.Notes,
            "activity_id": str(row.ActivityID)
        }

        # Merge sport-specific data
        activity.update(details)

        activities.append(activity)

    return activities