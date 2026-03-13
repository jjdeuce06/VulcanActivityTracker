#challenges_store.py:
from flask import Flask, request, jsonify
from datetime import datetime
from server.controllers.activity_store import get_user_activities
import pyodbc
import json

def insert_challenge(conn, user_id, name, description,
                     activity_type, metric_type, target_value,
                     start_date, end_date):#inserts a new challenge into the database
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO challenges
            (ChallengeName, Description, CreatorUserID,
             ActivityType, MetricType, TargetValue,
             StartDate, EndDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            description,
            user_id,
            activity_type,
            metric_type,
            target_value,
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
            SELECT ch.ChallengeID,
                   ch.ChallengeName,
                   ch.Description,
                   ch.CreatorUserID,
                   u.Username AS CreatorUsername,
                   ch.Participants,
                   ch.ActivityType,
                   ch.MetricType,
                   ch.TargetValue,
                   ch.StartDate,
                   ch.EndDate
            FROM challenges ch
            JOIN [user] u ON ch.CreatorUserID = u.UserID
            ORDER BY ch.StartDate DESC
        """)

        rows = cursor.fetchall()
        challenges = []

        for row in rows:
            participants = []
            try:
                participants = json.loads(row.Participants) if getattr(row, "Participants", None) else []
            except Exception:
                participants = []

            challenges.append({
                "id": str(row.ChallengeID),
                "name": row.ChallengeName,
                "description": row.Description or "",
                "creator_user_id": str(row.CreatorUserID),
                "creator_username": row.CreatorUsername,
                "participants": [str(p) for p in participants],
                "activity_type": row.ActivityType,
                "metric_type": row.MetricType,
                "target_value": row.TargetValue,
                "start_date": str(row.StartDate),
                "end_date": str(row.EndDate)
            })

        return challenges

    except Exception as e:
        print("Get all challenges error:", e)
        raise
    finally:
        cursor.close()
        
def get_not_user_challenges(conn, user_id):
    try:
        all_challenges = get_all_challenges(conn)
        uid = str(user_id)
        not_user_challenges = [c for c in all_challenges if c["creator_user_id"] != uid and uid not in c.get("participants", [])]
        return not_user_challenges
    except Exception as e:
        print("Get not user challenges error:", e)
        raise

def get_user_challenges(conn, user_id):
    try:
        all_challenges = get_all_challenges(conn)
        uid = str(user_id)
        user_challenges = [c for c in all_challenges if c["creator_user_id"] == uid or uid in c.get("participants", [])]
        for challenge in user_challenges:
            challenge["progress"] = calculate_challenge_progress(conn, challenge, user_id)
        return user_challenges
    except Exception as e:
        print("Get user challenges error:", e)
        raise
    
def add_participant_to_challenge(conn, challenge_id, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Participants FROM challenges WHERE ChallengeID = ?", (challenge_id))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Challenge not found")
        
        participants_json = getattr(row, "Participants", None) or row[0]
        
        try:
            participants = json.loads(participants_json) if participants_json else []
        except Exception:
            participants = []
            
        user_str = str(user_id)
        if user_str in participants:
            return participants
        
        participants.append(user_str)
        
        new_json = json.dumps(participants)
        cursor.execute("UPDATE challenges SET Participants = ? WHERE ChallengeID = ?", (new_json, challenge_id))
        conn.commit()
        return participants
    except Exception as e:
        print("Error adding participant:", e)
        raise
    finally:
        cursor.close()
        

def remove_participant_from_challenge(conn, challenge_id, user_id): #removes the user from the member list of a challenge in the database
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Participants FROM challenges WHERE ChallengeID = ?", (challenge_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Challenge not found")

        participants_json = getattr(row, "Participants", None) or (row[0] if len(row) > 0 else None)
        try:
            participants = json.loads(participants_json) if participants_json else []
        except Exception:
            participants = []

        user_str = str(user_id)
        if user_str not in participants: 
            print("User not in participants list or owner of club trying to leave") #
            return participants

        participants = [p for p in participants if p != user_str]
        new_json = json.dumps(participants)
        cursor.execute("UPDATE challenges SET Participants = ? WHERE ChallengeID = ?", (new_json, challenge_id))
        conn.commit()
        return participants
    except Exception as e:
        print("Error removing participant:", e)
        raise
    finally:
        cursor.close()
        
     
        
def remove_challenge_from_database(conn, challenge_id, user_id):
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT CreatorUserID FROM challenges WHERE ChallengeID = ?", (challenge_id, ))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Challenge Not Found")
        if str(row.CreatorUserID) != str(user_id):
            raise ValueError("Only Challenge Owner can Delete Club")
        
        cursor.execute("DELETE FROM challenges WHERE ChallengeID = ? AND CreatorUserID = ?", (challenge_id, user_id,))
    
        conn.commit()
        print("Challenge deleted successfully")
        return True

    except Exception as e:
        print("Delete challenge error:", e)
        raise

    finally:
        cursor.close()
        

def calculate_challenge_progress(conn, challenge, user_id):
    activities = get_user_activities(conn, user_id)

    start = datetime.fromisoformat(challenge["start_date"])
    end = datetime.fromisoformat(challenge["end_date"])

    total = 0.0

    for activity in activities:

        print("---- CHECKING ACTIVITY ----")
        print("Activity:", activity)
        print("Challenge activity_type:", challenge["activity_type"])
        print("Challenge metric:", challenge["metric_type"])
        print("----------------------------")

        #Match activity type
        if activity["activity_type"] != challenge["activity_type"]:
            continue

        # Parse date correctly
        activity_date = datetime.fromisoformat(activity["date"])

        if not (start <= activity_date <= end):
            continue

        metric = challenge["metric_type"].lower()

        # DISTANCE
        if metric == "distance":
            total += float(activity.get("distance", 0))

        # TIME
        elif metric == "time":
            total += float(activity.get("duration", 0))

        # COUNT
        elif metric == "count":
            total += 1

        # STEPS
        elif metric == "steps":
            total += float(activity.get("steps", 0))

        # SETS
        elif metric == "sets":
            total += float(activity.get("sets", 0))

        # GOALS
        elif metric == "goals":
            total += float(activity.get("goals", 0))

        # ASSISTS
        elif metric == "assists":
            total += float(activity.get("assists", 0))

        # HITS
        elif metric == "hits":
            total += float(activity.get("hits", 0))

        # RUNS
        elif metric == "runs":
            total += float(activity.get("runs", 0))

        # TOUCHDOWNS
        elif metric == "touchdowns":
            total += float(activity.get("touchdowns", 0))

        # POINTS
        elif metric == "points":
            total += float(activity.get("points", 0))

        # REBOUNDS
        elif metric == "rebounds":
            total += float(activity.get("rebounds", 0))

        # KILLS
        elif metric == "kills":
            total += float(activity.get("kills", 0))

        # INTENSITY
        elif metric == "intensity":
            total += float(activity.get("intensity", 0))

    target = float(challenge["target_value"])
    percent = 0

    if target > 0:
        percent = min((total / target) * 100, 100)

    return {
        "current": round(total, 2),
        "target": target,
        "percent": round(percent, 1)
    }