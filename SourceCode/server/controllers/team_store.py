from flask import Flask, request, jsonify
import pyodbc
import json

def get_all_teams(conn):    #gets all teams from the database 
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.TeamID, t.TeamName, t.Description, t.CreatorUserID, u.Username AS CreatorUsername, t.Members
            FROM teams t
            JOIN [user] u ON t.CreatorUserID = u.UserID
            ORDER BY t.TeamName
        """)
        rows = cursor.fetchall()
        teams = []
        for row in rows:
            members = []
            try:
                members = json.loads(row.Members) if getattr(row, "Members", None) else []
            except Exception:
                members = []
            teams.append({
                "id": str(row.TeamID),
                "name": row.TeamName,
                "description": row.Description or "",
                "creator_user_id": str(row.CreatorUserID),
                "creator_username": row.CreatorUsername,
                "members": [str(m) for m in members]
            })
        return teams
    except Exception as e:
        print("Get all teams error:", e)
        raise
    finally:
        cursor.close()

def add_member_to_team(conn, team_id, user_id, username): #adds a user to the member list of a team in the database
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Members FROM teams WHERE TeamID = ?", team_id)
        row = cursor.fetchone()
        if not row:
            raise Exception("Team not found")

        members = []
        try:
            members = json.loads(row.Members) if getattr(row, "Members", None) else []
        except Exception:
            members = []

        if str(user_id) in members:
            raise Exception("User is already a member of the team")

        members.append(str(user_id))
        members_json = json.dumps(members)

        cursor.execute("UPDATE teams SET Members = ?, UpdatedDate = SYSDATETIME() WHERE TeamID = ?", members_json, team_id)
        conn.commit()
    except Exception as e:
        print("Add member to team error:", e)
        raise

def remove_member_from_team(conn, team_id, user_id): #removes a user from the member list of a team in the database
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Members FROM teams WHERE TeamID = ?", team_id)
        row = cursor.fetchone()
        if not row:
            raise Exception("Team not found")

        members = []
        try:
            members = json.loads(row.Members) if getattr(row, "Members", None) else []
        except Exception:
            members = []

        if str(user_id) not in members:
            raise Exception("User is not a member of the team")

        members.remove(str(user_id))
        members_json = json.dumps(members)

        cursor.execute("UPDATE teams SET Members = ?, UpdatedDate = SYSDATETIME() WHERE TeamID = ?", members_json, team_id)
        conn.commit()
    except Exception as e:
        print("Remove member from team error:", e)
        raise