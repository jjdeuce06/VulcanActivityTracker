document.addEventListener("DOMContentLoaded", async () => {

    const teamsContainer = document.getElementById("teams-container");
    const mensTeams = {
        "Men's Soccer": "mens_soccer",
        "Men's Basketball": "mens_basketball",
        "Men's Cross Country": "mens_cross_country",
        "Men's Football": "mens_football",
        "Men's Golf": "mens_golf",
        "Men's Baseball": "mens_baseball",
        "Men's Track and Field": "mens_track_and_field",
    };

    const womensTeams = {
        "Women's Soccer": "womens_soccer",
        "Women's Basketball": "womens_basketball",
        "Women's Cross Country": "womens_cross_country",
        "Women's Track and Field": "womens_track_and_field",
        "Women's Flag Football": "womens_flag_football",
        "Women's Softball": "womens_softball",
        "Women's Swimming": "womens_swimming",
        "Women's Tennis": "womens_tennis",
        "Women's Volleyball": "womens_volleyball",
    };

    const defaultTeams = mensTeams; // Default


    document.getElementById("sortByGender").addEventListener("change", (event) => {
        const selectedGender = event.target.value;
        teamsContainer.innerHTML = ""; // Clear existing teams

        let teamsToDisplay = {};
        if (selectedGender === "men") {
            teamsToDisplay = mensTeams;
        } else if (selectedGender === "women") {
            teamsToDisplay = womensTeams;
        }

        for (const [teamName, teamId] of Object.entries(teamsToDisplay)) {
            const teamElement = document.createElement("div");
            teamElement.classList.add("team");
            teamElement.innerHTML = `
                <h3>${teamName}</h3>
                <a href="/teams/${teamId}">View Team</a>
            `;
            teamsContainer.appendChild(teamElement);
        }
    });


    function loadTeams(teams) {
        teamsContainer.innerHTML = "";
        for (const [teamName, teamId] of Object.entries(teams)) {
            const teamElement = document.createElement("div");
            teamElement.classList.add("team");
            teamElement.innerHTML = `
                <h3>${teamName}</h3>
                <a href="/teams/${teamId}">View Team</a>
            `;
            teamsContainer.appendChild(teamElement);
        }
    }

    // Load default teams on page load
    loadTeams(defaultTeams);
    
    });
