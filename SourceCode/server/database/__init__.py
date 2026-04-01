#The init file creates tables, add all creation functions here to be ported to app
def init_or_upgrade_schema(conn):
    print("Starting schema initialization...")

    from server.database.schema.loginSchema import create_user_table
    create_user_table(conn)
    print("user table schema initialized or updated.")

    from server.database.schema.activitySchema import create_activity_table
    create_activity_table(conn)
    print("activity table schema initialized or updated.")

    from server.database.schema.friendSchema import create_friends_table
    create_friends_table(conn)
    print("activity table schema initialized or updated.")
    
    from server.database.schema.clubSchema import create_clubs_table
    create_clubs_table(conn)
    print("clubs table schema initialized or updated.")

    from server.database.schema.likeSchema import create_likes_table
    create_likes_table(conn)
    print("likes table schema initialized or updated.")

    from server.database.schema.activityLikeSchema import create_activity_likes_table
    create_activity_likes_table(conn)
    print("activity_likes table schema initialized or updated.")
    
    from server.database.schema.challengesSchema import create_challenges_table
    create_challenges_table(conn)
    print("likes table schema initialized or updated.")


    from server.database.schema.mapSchema import create_maps_table
    create_maps_table(conn)
    print("maps table schema initialized or updated.")

    from server.database.schema.teamSchema import create_teams_table
    create_teams_table(conn)
    print("teams table schema initialized or updated.")

    from server.database.schema.teamSchema import create_team_member_table
    create_team_member_table(conn)
    print("team member table schema initialized or updated.")

    from server.database.schema.teamSchema import create_team_coach_emails_table
    create_team_coach_emails_table(conn)
    print("team coach email table updated")

    from server.database.schema.teamSchema import create_team_join_requests_table
    create_team_join_requests_table(conn)
    print("join request table created or initialized")

    from server.database.schema.populateTeamSchema import seed_teams_and_coaches
    seed_teams_and_coaches(conn)
    print("populating tables")

    from server.database.schema.teamInviteSchema import create_team_invites_table
    create_team_invites_table(conn)
    print("creating team invites table")

    from server.database.schema.announcementSchema import create_team_announcements_table
    create_team_announcements_table(conn)
    print("creating announcement table")

    from server.database.schema.scheduleSchema import create_team_schedule_table
    create_team_schedule_table(conn)
    print("Creating team schedule table")
    
    from server.database.schema.clubInviteSchema import create_clubs_invites_table
    create_clubs_invites_table(conn)
    print("creating clubs invites table")
