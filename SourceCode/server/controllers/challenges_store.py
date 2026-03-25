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
                   ch.EndDate,
                   ch.IsCompleted,
                    ch.MedalsAwarded
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
                "end_date": str(row.EndDate),
                "is_completed": bool(row.IsCompleted),
                "medals_awarded": bool(row.MedalsAwarded),
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



def get_dash_challenges(conn, user_id):
    try:
        all_challenges = get_all_challenges(conn)
        uid = str(user_id)

        user_challenges = []
        for c in all_challenges:
            participants = c.get("participants") or []
            participants = [str(p) for p in participants]

            # only include challenges created by this user OR joined by this user
            if c["creator_user_id"] == uid or uid in participants:
                c["progress"] = calculate_challenge_progress(conn, c, user_id) or {
                    "current": 0,
                    "target": c.get("target_value", 0),
                    "percent": 0
                }
                user_challenges.append(c)

        return user_challenges

    except Exception as e:
        print("Get user challenges error:", e)
        raise
    
def add_participant_to_challenge(conn, challenge_id, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Participants, CreatorUserID FROM challenges WHERE ChallengeID = ?", (challenge_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Challenge not found")
        
        if str(row.CreatorUserID) == str(user_id):
            raise ValueError("Challenge owner cannot join their own challenge")
        
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
    

def challenge_name_exists(conn, challenge_name):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 1
            FROM challenges
            WHERE LOWER(LTRIM(RTRIM(ChallengeName))) = LOWER(LTRIM(RTRIM(?)))
        """, (challenge_name,))
        row = cursor.fetchone()
        return row is not None
    except Exception as e:
        print("Challenge name exists check error:", e)
        raise
    finally:
        cursor.close()    
        

def get_participant_details(conn, user_ids):
    cursor = conn.cursor()
    try:
        if not user_ids:
            return []

        clean_ids = [str(uid) for uid in user_ids if str(uid).strip()]
        placeholders = ",".join("?" for _ in clean_ids)

        cursor.execute(f"""
            SELECT UserID, Username
            FROM [user]
            WHERE UserID IN ({placeholders})
        """, tuple(clean_ids))

        rows = cursor.fetchall()
        user_map = {str(row.UserID): row.Username for row in rows}

        return [
            {"user_id": str(uid), "username": user_map.get(str(uid), f"User {uid}")}
            for uid in clean_ids
        ]

    finally:
        cursor.close()
        
def get_challenge_leaderboard(conn, challenge):
    leaderboard = []

    participant_ids = challenge.get("participants", [])
    if not participant_ids:
        return []

    participant_details = get_participant_details(conn, participant_ids)

    for participant in participant_details:
        progress = calculate_challenge_progress(conn, challenge, participant["user_id"])

        leaderboard.append({
            "user_id": participant["user_id"],
            "username": participant["username"],
            "current": progress["current"],
            "target": progress["target"],
            "percent": progress["percent"]
        })

    leaderboard.sort(key=lambda p: p["current"], reverse=True)

    for index, entry in enumerate(leaderboard, start=1):
        entry["rank"] = index

    return leaderboard

def get_user_medals(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Medals FROM [user] WHERE UserID = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("User not found")

        medals_json = getattr(row, "Medals", None) or row[0]
        try:
            medals = json.loads(medals_json) if medals_json else {}
        except Exception:
            medals = {}

        return {
            "gold": int(medals.get("gold", 0)),
            "silver": int(medals.get("silver", 0)),
            "bronze": int(medals.get("bronze", 0)),
            "completed": int(medals.get("completed", 0))
        }
    finally:
        cursor.close()


def add_medal_to_user(conn, user_id, medal_type):
    cursor = conn.cursor()
    try:
        medals = get_user_medals(conn, user_id)

        if medal_type not in medals:
            raise ValueError("Invalid medal type")

        medals[medal_type] += 1

        cursor.execute(
            "UPDATE [user] SET Medals = ? WHERE UserID = ?",
            (json.dumps(medals), user_id)
        )
        conn.commit()
        return medals
    finally:
        cursor.close()


def award_challenge_medals(conn, challenge):
    if challenge.get("medals_awarded"):
        return

    leaderboard = get_challenge_leaderboard(conn, challenge)

    # award top 3 medals
    medal_order = ["gold", "silver", "bronze"]
    for index, entry in enumerate(leaderboard[:3]):
        add_medal_to_user(conn, entry["user_id"], medal_order[index])

    # award "completed" to every participant who met the goal
    for entry in leaderboard:
        if float(entry["current"]) >= float(entry["target"]):
            add_medal_to_user(conn, entry["user_id"], "completed")

    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE challenges
            SET IsCompleted = 1,
                MedalsAwarded = 1
            WHERE ChallengeID = ?
        """, (challenge["id"],))
        conn.commit()
    finally:
        cursor.close()


def finalize_expired_challenges(conn):
    today = datetime.now().date()
    all_challenges = get_all_challenges(conn)

    for challenge in all_challenges:
        if challenge.get("is_completed"):
            continue

        end_date = datetime.fromisoformat(challenge["end_date"]).date()

        if end_date < today:
            award_challenge_medals(conn, challenge)


def get_visible_not_user_challenges(conn, user_id):
    all_challenges = get_all_challenges(conn)
    uid = str(user_id)
    return [
        c for c in all_challenges
        if not c.get("is_completed")
        and c["creator_user_id"] != uid
        and uid not in c.get("participants", [])
    ]


def get_visible_user_challenges(conn, user_id):
    all_challenges = get_all_challenges(conn)
    uid = str(user_id)

    user_challenges = [
        c for c in all_challenges
        if not c.get("is_completed")
        and (c["creator_user_id"] == uid or uid in c.get("participants", []))
    ]

    for challenge in user_challenges:
        challenge["progress"] = calculate_challenge_progress(conn, challenge, user_id)

    return user_challenges