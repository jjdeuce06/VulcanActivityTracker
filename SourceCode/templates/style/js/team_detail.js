document.addEventListener("DOMContentLoaded", async () => {
const username = localStorage.getItem("currentUser") || "Coach Demo";

  if (!username) {
    alert("Please log in first.");
    window.location.href = "/login";
    return;
  }

  const pathParts = window.location.pathname.split("/").filter(Boolean);
  const teamId = pathParts[pathParts.length - 1];

  const teamNameHeading = document.getElementById("team-name-heading");
  const teamSport = document.getElementById("team-sport");
  const teamCoach = document.getElementById("team-coach");
  const teamMemberCount = document.getElementById("team-member-count");
  const teamDescription = document.getElementById("team-description");
  const rosterList = document.getElementById("roster-list");
  const coachTools = document.getElementById("coach-tools");
  const inviteForm = document.getElementById("invite-player-form");
  const inviteUsernameInput = document.getElementById("invite-username");

  async function loadTeam() {
    try {
      console.log("Loading team:", teamId, "for user:", username);

      const resp = await fetch("/team_api/teamdetail", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username,
          team_id: teamId
        })
      });

      const data = await resp.json();
      console.log("teamdetail response:", data);

      if (!resp.ok) {
        alert(data.error || "Unable to load team");
        window.location.href = "/teams";
        return;
      }

      const team = data.team;
      const roster = Array.isArray(team.roster) ? team.roster : [];

      teamNameHeading.textContent = team.name || "Team";
      teamSport.textContent = team.sport || "Sport";
      teamCoach.textContent = `Coach: ${team.coach_username || "Unknown"}`;
      teamMemberCount.textContent = `${roster.length} Member${roster.length === 1 ? "" : "s"}`;
      teamDescription.textContent = team.description || "No description provided.";

      rosterList.innerHTML = "";

      if (roster.length === 0) {
        rosterList.innerHTML = `<p class="empty-state">No roster members found.</p>`;
      } else {
        roster.forEach(member => {
          const div = document.createElement("div");
          div.className = "roster-item";
          div.innerHTML = `
            <strong>${member.username}</strong>
            <div style="margin-top: 4px; font-size: 13px; color: #c7c9e6;">
              Role: ${member.role}
            </div>
          `;
          rosterList.appendChild(div);
        });
      }

      const isCoach = true //String(team.coach_username).toLowerCase() === String(username).toLowerCase();
      coachTools.style.display = isCoach ? "block" : "none";
    } catch (err) {
      console.error("Error loading team:", err);
      alert("Error loading team");
      window.location.href = "/teams";
    }
  }

  if (inviteForm) {
    inviteForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const invitedUsername = inviteUsernameInput.value.trim();
      if (!invitedUsername) {
        alert("Enter a username to invite.");
        return;
      }

      try {
        const resp = await fetch("/team_api/invite", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            username,
            invited_username: invitedUsername,
            team_id: teamId
          })
        });

        const data = await resp.json();
        console.log("invite response:", data);

        if (!resp.ok) {
          alert(data.error || "Failed to send invite");
          return;
        }

        alert(`Invite sent to ${invitedUsername}`);
        inviteForm.reset();
      } catch (err) {
        console.error("Invite error:", err);
        alert("Error sending invite");
      }
    });
  }

  await loadTeam();
});