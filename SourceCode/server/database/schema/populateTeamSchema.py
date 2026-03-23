import pyodbc

def seed_teams_and_coaches(conn: pyodbc.Connection) -> None:
    cursor = conn.cursor()

    teams_to_seed = [
        {
            "team_name": "PennWest Men's Soccer",
            "sport": "Soccer",
            "description": "Official men's soccer team",
            "coach_emails": [
                "sabic@pennwest.edu",
                "henderson_jo@pennwest.edu"
            ]
        },
        {
            "team_name": "PennWest Women's Soccer",
            "sport": "Soccer",
            "description": "Official women's soccer team",
            "coach_emails": [
                "curtis@pennwest.edu",
                "gribowicz@pennwest.edu"
            ]
        },
        {
            "team_name": "PennWest Men's Basketball",
            "sport": "Basketball",
            "description": "Official men's basketball team",
            "coach_emails": [
                "sancomb@pennwest.edu",
                "bridgeman@pennwest.edu",
            ]
        },
        {
            "team_name": "PennWest Women's Basketball",
            "sport": "Basketball",
            "description": "Official women's basketball team",
            "coach_emails": [
                "strom@pennwest.edu",
                "tetzlaw@pennwest.edu",
            ]
        },
        {
            "team_name": "PennWest Men's Cross Country",
            "sport": "Cross Country",
            "description": "Official men's cross country",
            "coach_emails": [
                "caulfield@pennwest.edu"
            ]
        },
        {
            "team_name": "PennWest Women's Cross Country",
            "sport": "Cross Country",
            "description": "Official women's cross country",
            "coach_emails": [
                "caulfield@pennwest.edu"
            ]
        },
        {
            "team_name": "PennWest Men's Football",
            "sport": "Cross Country",
            "description": "Official men's football",
            "coach_emails": [
                "dunn_g@pennwest.edu",
                "turner@pennwest.edu",
                "orlosky_t@pennwest.edu",
                "apapley@pennwest.edu",
                "venick@pennwest.edu",
                "fiasco_j@pennwest.edu",
                "malanka_j@pennwest.edu",
                "organ_k@pennwest.edu"
            ]
        },
        {
            "team_name": "PennWest Women's Flag Football",
            "sport": "Cross Country",
            "description": "Official Women's flag football",
            "coach_emails": [
                "mitchell_n@pennwest.edu"
            ]
        },
        {
            "team_name": "PennWest Men's Golf",
            "sport": "Golf",
            "description": "Official Men's Golf",
            "coach_emails": [
                "bennett@pennwest.edu",
                "paladino_d@pennwest.edu"
            ]
        },
        {
        "team_name": "PennWest Women's Golf",
        "sport": "Golf",
        "description": "Official women's golf team",
        "coach_emails": [
            "noro@pennwest.edu",
            "morelli_v@pennwest.edu"
        ]
    },
    {
        "team_name": "PennWest Baseball",
        "sport": "Baseball",
        "description": "Official men's baseball team",
        "coach_emails": [
            "baseball@pennwest.edu"
        ]
    },
    {
        "team_name": "PennWest Men's Track and Field",
        "sport": "Track and Field",
        "description": "Official men's track and field team",
        "coach_emails": [
            "caulfield@pennwest.edu",
            "estep@pennwest.edu",
            "wert@pennwest.edu"
        ]
    },
    {
        "team_name": "PennWest Women's Softball",
        "sport": "Softball",
        "description": "Official women's softball team",
        "coach_emails": [
            "erb_k@pennwest.edu",
            "hall_r@pennwest.edu"
        ]
    },
    {
        "team_name": "PennWest Women's Swimming",
        "sport": "Swimming",
        "description": "Official women's swimming team",
        "coach_emails": [
            "gitzen@pennwest.edu",
            "kennedy_r@pennwest.edu"
        ]
    },
    {
        "team_name": "PennWest Women's Tennis",
        "sport": "Tennis",
        "description": "Official women's tennis team",
        "coach_emails": [
            "onufer@pennwest.edu"
        ]
    },
    {
        "team_name": "PennWest Women's Volleyball",
        "sport": "Volleyball",
        "description": "Official women's volleyball team",
        "coach_emails": [
            "emerich_a@pennwest.edu",
            "greene_ma@pennwest.edu"
        ]
    }
    ]

    for team in teams_to_seed:

        # ✅ Insert team if it doesn't exist
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM teams WHERE TeamName = ? AND Sport = ?
            )
            BEGIN
                INSERT INTO teams (TeamName, Sport, Description)
                VALUES (?, ?, ?)
            END
        """, (
            team["team_name"],
            team["sport"],
            team["team_name"],
            team["sport"],
            team["description"]
        ))
        conn.commit()

        # ✅ Get TeamID
        cursor.execute("""
            SELECT TeamID FROM teams
            WHERE TeamName = ? AND Sport = ?
        """, (team["team_name"], team["sport"]))

        row = cursor.fetchone()
        if not row:
            print(f"Failed to fetch TeamID for {team['team_name']}")
            continue

        team_id = row.TeamID

        # ✅ Insert coach emails
        for email in team["coach_emails"]:
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM team_coach_emails
                    WHERE TeamID = ? AND Email = ?
                )
                BEGIN
                    INSERT INTO team_coach_emails (TeamID, Email)
                    VALUES (?, ?)
                END
            """, (team_id, email, team_id, email))

        conn.commit()
        print(f"Seeded: {team['team_name']}")

    cursor.close()