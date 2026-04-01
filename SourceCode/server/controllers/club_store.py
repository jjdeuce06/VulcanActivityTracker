from flask import Flask, request, jsonify
import pyodbc
import json
from datetime import datetime, timedelta
from server.controllers.activity_store import get_user_activities

def insert_club(conn, user_id, name, description, sport_type, privacy): #inserts a new club into the database
    cursor = conn.cursor()
    try:
        is_private = 1 if str(privacy).lower() == "private" else 0

        cursor.execute("""
            INSERT INTO clubs (ClubName, Description, CreatorUserID, SportType, IsPrivate)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, user_id, sport_type, is_private))

        conn.commit()
        print("Club inserted successfully")

    except Exception as e:
        print("Insert club error:", e)
        raise

    finally:
        cursor.close()

def get_all_clubs(conn):    #gets all clubs from the database 
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT c.ClubID,
            c.ClubName,
            c.Description,
            c.CreatorUserID,
            u.Username AS CreatorUsername,
            c.Members,
            c.SportType,
            c.IsPrivate
            FROM clubs c
            JOIN [user] u ON c.CreatorUserID = u.UserID
            ORDER BY c.ClubName
        """)
        rows = cursor.fetchall()
        clubs = []
        for row in rows:
            members = []
            try:
                members = json.loads(row.Members) if getattr(row, "Members", None) else []
            except Exception:
                members = []
            clubs.append({
                "id": str(row.ClubID),
                "name": row.ClubName,
                "description": row.Description or "",
                "creator_user_id": str(row.CreatorUserID),
                "creator_username": row.CreatorUsername,
                "members": [str(m) for m in members],
                "total_members": 1 + len([str(m) for m in members]),  # owner + joined members
                "sport_type": row.SportType,
                "is_private": bool(row.IsPrivate),
            })
        return clubs
    except Exception as e:
        print("Get all clubs error:", e)
        raise
    finally:
        cursor.close()

def get_not_user_clubs(conn, user_id): #gets clubs in which the current user is not a member or creator from database
    try:
        all_clubs = get_all_clubs(conn)
        uid = str(user_id)
        not_user_clubs = [c for c in all_clubs if c["creator_user_id"] != uid and uid not in c.get("members", [])]
        return not_user_clubs
    except Exception as e:
        print("Get not user clubs error:", e)
        raise

def get_user_clubs(conn, user_id): #gets club in which the current user is a member or creator from database... For now creator isnt in member list
    try:
        all_clubs = get_all_clubs(conn)
        uid = str(user_id)
        user_clubs = [c for c in all_clubs if c["creator_user_id"] == uid or uid in c.get("members", [])]
        return user_clubs
    except Exception as e:
        print("Get user clubs error:", e)
        raise

def add_member_to_club(conn, club_id, user_id, username): #adds a user to the member list of a club in the database
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Members FROM clubs WHERE ClubID = ?", (club_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Club not found")

        members_json = getattr(row, "Members", None) or row[0]
    
        try:
            members = json.loads(members_json) if members_json else []
        except Exception:
            members = []

        user_str = str(user_id)
        if user_str in members:
            return members

        members.append(user_str)
        #members.append(username)
        new_json = json.dumps(members)
        cursor.execute("UPDATE clubs SET Members = ?, UpdatedDate = SYSDATETIME() WHERE ClubID = ?", (new_json, club_id))
        conn.commit()
        return members
    except Exception as e:
        print("Error adding member:", e)
        raise
    finally:
        cursor.close()
        
def remove_member_from_club(conn, club_id, user_id, username): #removes the user from the member list of a club in the database
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Members FROM clubs WHERE ClubID = ?", (club_id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Club not found")

        members_json = getattr(row, "Members", None) or (row[0] if len(row) > 0 else None)
        try:
            members = json.loads(members_json) if members_json else []
        except Exception:
            members = []

        user_str = str(user_id)
        username_str = str(username)
        if user_str not in members: 
            print("User not in members list or owner of club trying to leave") #
            return members

        members = [m for m in members if m != str(user_id)]
        new_json = json.dumps(members)
        cursor.execute("UPDATE clubs SET Members = ?, UpdatedDate = SYSDATETIME() WHERE ClubID = ?", (new_json, club_id))
        conn.commit()
        return members
    except Exception as e:
        print("Error removing member:", e)
        raise
    finally:
        cursor.close()
        
def remove_club_from_database(conn, club_id, user_id):
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT CreatorUserID FROM clubs WHERE ClubID = ?", (club_id, ))
        row = cursor.fetchone()
        if not row:
            raise ValueError("Club Not Found")
        if str(row.CreatorUserID) != str(user_id):
            raise ValueError("Only Club Owner can Delete Club")
        
        cursor.execute("DELETE FROM clubs WHERE ClubID = ? AND CreatorUserID = ?", (club_id, user_id,))
    
        conn.commit()
        print("Club deleted successfully")
        return True

    except Exception as e:
        print("Delete club error:", e)
        raise

    finally:
        cursor.close()

def usernames_from_userids(conn, user_ids):
    if not user_ids:
        return []

    cursor = conn.cursor()
    try:
        placeholders = ",".join("?" for _ in user_ids)
        cursor.execute(
            f"SELECT UserID, Username FROM [user] WHERE UserID IN ({placeholders})",
            tuple(user_ids)
        )
        rows = cursor.fetchall()
        id_to_name = {str(r.UserID): r.Username for r in rows}
        return [id_to_name.get(str(uid)) for uid in user_ids if id_to_name.get(str(uid))]
    finally:
        cursor.close()
        
def club_uses_distance_ranking(sport_type):
    return sport_type in {"run", "bike", "swim", "walk", "equestrian", "multisport"}


def get_club_member_details(conn, club):
    members = club.get("members", []) or []
    creator_id = str(club.get("creator_user_id"))

    all_ids = [creator_id] + [str(uid) for uid in members if str(uid) != creator_id]
    return usernames_from_userids(conn, all_ids), all_ids


def get_week_range(reference_date=None):
    if reference_date is None:
        reference_date = datetime.now()

    start_of_week = reference_date - timedelta(days=reference_date.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)

    return start_of_week, end_of_week


def calculate_club_member_stats(conn, user_id, sport_type, start_date, end_date):
    activities = get_user_activities(conn, user_id)

    total_distance = 0.0
    total_time = 0.0

    for activity in activities:
        if activity.get("activity_type") != sport_type and sport_type != "multisport":
            continue

        try:
            activity_date = datetime.fromisoformat(activity["date"])
        except Exception:
            continue

        if not (start_date <= activity_date < end_date):
            continue

        total_distance += float(activity.get("distance", 0) or 0)
        total_time += float(activity.get("duration", 0) or 0)

    return {
        "distance": round(total_distance, 2),
        "time": round(total_time, 2)
    }


def get_club_leaderboard_for_range(conn, club, start_date, end_date):
    member_ids = [str(club.get("creator_user_id"))] + [str(uid) for uid in club.get("members", [])]
    member_ids = list(dict.fromkeys(member_ids))

    usernames = usernames_from_userids(conn, member_ids)
    id_to_username = dict(zip(member_ids, usernames))

    sport_type = club.get("sport_type")
    use_distance = club_uses_distance_ranking(sport_type)

    leaderboard = []

    for user_id in member_ids:
        stats = calculate_club_member_stats(conn, user_id, sport_type, start_date, end_date)

        leaderboard.append({
            "user_id": user_id,
            "username": id_to_username.get(user_id, "Unknown User"),
            "distance": stats["distance"],
            "time": stats["time"]
        })

    if use_distance:
        leaderboard.sort(key=lambda x: (x["distance"], x["time"]), reverse=True)
    else:
        leaderboard.sort(key=lambda x: x["time"], reverse=True)

    for index, entry in enumerate(leaderboard, start=1):
        entry["rank"] = index

    return leaderboard


def get_club_this_week_leaderboard(conn, club):
    start_of_week, end_of_week = get_week_range()
    return get_club_leaderboard_for_range(conn, club, start_of_week, end_of_week)


def get_club_last_week_leaders(conn, club):
    this_week_start, _ = get_week_range()
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start

    leaderboard = get_club_leaderboard_for_range(conn, club, last_week_start, last_week_end)
    return leaderboard[:3]