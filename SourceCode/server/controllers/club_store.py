from flask import Flask, request, jsonify
import pyodbc
import json

def insert_club(conn, user_id, name, description): #inserts a new club into the database
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO clubs (ClubName, Description, CreatorUserID)
            VALUES (?, ?, ?)
        """, (name, description, user_id))

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
            SELECT ClubID, ClubName, Description, CreatorUserID, Members
            FROM clubs
            ORDER BY ClubName
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
                "members": [str(m) for m in members]
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

def add_member_to_club(conn, club_id, user_id): #adds a user to the member list of a club in the database
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
        new_json = json.dumps(members)
        cursor.execute("UPDATE clubs SET Members = ?, UpdatedDate = SYSDATETIME() WHERE ClubID = ?", (new_json, club_id))
        conn.commit()
        return members
    except Exception as e:
        print("Error adding member:", e)
        raise
    finally:
        cursor.close()
        
def remove_member_from_club(conn, club_id, user_id): #removes the user from the member list of a club in the database
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
        if user_str not in members: 
            print("User not in members list or owner of club trying to leave") #
            return members

        members = [m for m in members if m != user_str]
        new_json = json.dumps(members)
        cursor.execute("UPDATE clubs SET Members = ?, UpdatedDate = SYSDATETIME() WHERE ClubID = ?", (new_json, club_id))
        conn.commit()
        return members
    except Exception as e:
        print("Error removing member:", e)
        raise
    finally:
        cursor.close()