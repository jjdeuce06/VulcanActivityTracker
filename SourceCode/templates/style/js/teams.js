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

      if (selectedGender === "women") {
        return name.includes("women");
      }

      return name.includes("men");
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

  async function loadInvites() {
  const response = await fetch("/team_api/invites", {
    method: "GET",
    credentials: "include"
  });

  const data = await response.json();

  if (!response.ok) {
    console.error("Failed to load invites:", data.error);
    return [];
  }

  return data.invites || [];
}

async function acceptInvite(teamId) {
  const response = await fetch("/team_api/acceptinvite", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({ team_id: teamId })
  });

  const data = await response.json();
  if (!response.ok) {
    alert(data.error || "Failed to accept invite");
    return false;
  }

  return true;
}

async function declineInvite(teamId) {
  const response = await fetch("/team_api/declineinvite", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({ team_id: teamId })
  });

  const data = await response.json();
  if (!response.ok) {
    alert(data.error || "Failed to decline invite");
    return false;
  }

  return true;
}
});