document.addEventListener("DOMContentLoaded", () => {
  const teamsContainer = document.getElementById("teams-container");
  const genderSelect = document.getElementById("sortByGender");

  let allTeams = [];

  async function fetchAllTeams() {
    try {
      const response = await fetch("/team_api/listallteams", {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });

      const result = await response.json();

      if (!response.ok) {
        teamsContainer.innerHTML = `<p>${result.error || "Failed to load teams."}</p>`;
        return;
      }

      allTeams = result.teams || [];
      renderTeams();
    } catch (error) {
      console.error("Error fetching teams:", error);
      teamsContainer.innerHTML = "<p>Something went wrong while loading teams.</p>";
    }
  }

  function renderTeams() {
    teamsContainer.innerHTML = "";

    const selectedGender = genderSelect.value;

    let filteredTeams = allTeams.filter(team => {
      const name = (team.TeamName || "").toLowerCase();
      console.log(name);

      if (selectedGender === "women") 
      {
        return name.includes("women");
      }
      else if (selectedGender === "men")
      {
        return name.includes(" men");
      }
    });

    if (filteredTeams.length === 0) {
      teamsContainer.innerHTML = "<p>No teams found.</p>";
      return;
    }

    filteredTeams.forEach(team => {
      const teamElement = document.createElement("div");
      teamElement.classList.add("team");

      teamElement.innerHTML = `
        <h3>${team.TeamName}</h3>
        <a href="/teams/${team.TeamID}">View Team</a>
      `;

      teamsContainer.appendChild(teamElement);
    });
  }

  genderSelect.addEventListener("change", renderTeams);

  fetchAllTeams();
});