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
    
    from server.database.schema.challengesSchema import create_challenges_table
    create_challenges_table(conn)
    print("likes table schema initialized or updated.")