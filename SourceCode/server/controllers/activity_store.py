from flask import Flask, request, jsonify
import pyodbc
import json
from datetime import datetime


def insert_activity(conn, user_id: str, data: dict):
    print("enter insert")
    try:
        # Split common vs sport-specific fields
        common_fields = ['activity_type', 'date', 'duration', 'calories_burned', 'visibility', 'notes']
        activity_common = {k: data.get(k) for k in common_fields}
        sport_specific = {k: v for k, v in data.items() if k not in common_fields}

        # Debug log
        print("Activity common fields:", activity_common)
        print("Sport-specific fields:", sport_specific)

        # Safely convert numeric fields
        duration = float(activity_common.get('duration')) if activity_common.get('duration') is not None else None
        calories = float(activity_common.get('calories_burned')) if activity_common.get('calories_burned') is not None else None

        # Convert date to datetime object
        date_str = activity_common.get('date')
        try:
            activity_date = datetime.fromisoformat(date_str) if date_str else datetime.now()
        except ValueError:
            print(f"Invalid date format: {date_str}, using current time instead")
            activity_date = datetime.now()

        # Ensure sport-specific fields are JSON serializable
        try:
            details_json = json.dumps(sport_specific)
        except Exception as e:
            print("Error serializing sport-specific fields:", e)
            details_json = "{}"

        # Insert into DB
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
        conn.commit()
        print("Activity inserted successfully")

    except Exception as e:
        print("Insert activity error:", e)
        raise

    finally:
        cursor.close()
