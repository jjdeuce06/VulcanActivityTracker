from flask import Flask, request, jsonify
import pyodbc
import json

def insert_challenge(conn, user_id, name, description,
                     activity_type, metric_type,
                     start_date, end_date):#inserts a new challenge into the database
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO challenges
            (ChallengeName, Description, CreatorUserID,
             ActivityType, MetricType,
             StartDate, EndDate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            description,
            user_id,
            activity_type,
            metric_type,
            start_date,
            end_date
        ))

        conn.commit()
        print("Challenge inserted successfully")

    except Exception as e:
        print("Insert challenge error:", e)
        raise

    finally:
        cursor.close()

def get_all_challenges(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT ChallengeID,
                   ChallengeName,
                   Description,
                   ActivityType,
                   MetricType,
                   StartDate,
                   EndDate
            FROM challenges
            ORDER BY StartDate DESC
        """)

        rows = cursor.fetchall()

        challenges = []
        for row in rows:
            challenges.append({
                "ChallengeID": str(row.ChallengeID),
                "ChallengeName": row.ChallengeName,
                "Description": row.Description,
                "ActivityType": row.ActivityType,
                "MetricType": row.MetricType,
                "StartDate": str(row.StartDate),
                "EndDate": str(row.EndDate)
            })

        return challenges

    finally:
        cursor.close()