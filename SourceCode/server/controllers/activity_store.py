from flask import Flask, request, jsonify
import pyodbc
import json
from datetime import datetime

def insert_activity(conn, user_id: str, data: dict):
    # Split common vs sport-specific fields
    common_fields = ['activity_type', 'date', 'duration', 'calories_burned', 'visibility', 'notes']
    activity_common = {k: data.get(k) for k in common_fields}

    # Everything else goes into Details JSON
    sport_specific = {k: v for k, v in data.items() if k not in common_fields}

    # Convert date to datetime object if needed
    activity_date = datetime.fromisoformat(activity_common.get('date')) if activity_common.get('date') else datetime.now()

    # Insert into DB
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO [activity] (UserID, ActivityType, ActivityDate, Duration, CaloriesBurned, Visibility, Notes, Details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    user_id,
    activity_common.get('activity_type'),
    activity_date,
    activity_common.get('duration'),
    activity_common.get('calories_burned'),
    activity_common.get('visibility', 'private'),
    activity_common.get('notes'),
    json.dumps(sport_specific)  # store dynamic fields as JSON
    )
    conn.commit()
    cursor.close()
    conn.close()