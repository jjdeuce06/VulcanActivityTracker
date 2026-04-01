document.addEventListener("DOMContentLoaded", async () => {
  const clubId = window.location.pathname.split("/").pop();
  const currentUser = localStorage.getItem("currentUser");
  const tabContent = document.getElementById("club-tab-content");
  const actionBtn = document.getElementById("club-action-btn");

  let currentClub = null;
  let activeTab = "leaderboard";

  async function loadClub() {
    try {
      const resp = await fetch("/club_api/clubdetail", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          club_id: clubId,
          username: currentUser
        })
      });

      if (!resp.ok) {
        alert("Club not found");
        history.back();
        return;
      }

      const data = await resp.json();
      const club = data.club;
      currentClub = club;

      document.getElementById("club-name-heading").textContent = club.name;
      document.getElementById("club-description").textContent =
        club.description || "No description provided.";
      document.getElementById("member-count").textContent =
        club.total_members ?? ((club.members?.length || 0) + 1);
      document.getElementById("club-sport-type").textContent =
        formatSport(club.sport_type || "unknown");
      document.getElementById("club-privacy").textContent =
        club.is_private ? "Private" : "Public";

      setupActionButton(club);
      renderActiveTab();
    } catch (err) {
      console.error("Error loading club:", err);
      alert("Error loading club");
    }
  }

  function formatSport(value) {
    const labels = {
      run: "Running",
      bike: "Cycling",
      swim: "Swimming",
      lifting: "Weightlifting",
      walk: "Walking",
      yoga: "Yoga",
      soccer: "Soccer",
      baseball: "Baseball",
      football: "Football",
      tennis: "Tennis",
      volleyball: "Volleyball",
      basketball: "Basketball",
      equestrian: "Equestrian",
      multisport: "Multisport"
    };
    return labels[value] || value;
  }

  function setupActionButton(club) {
    if (!actionBtn) return;

    if (club.is_owner) {
      actionBtn.textContent = "Delete Club";
      actionBtn.dataset.action = "delete";
    } else if (club.is_member) {
      actionBtn.textContent = "Leave Club";
      actionBtn.dataset.action = "leave";
    } else {
      actionBtn.textContent = club.is_private ? "Request to Join" : "Join Club";
      actionBtn.dataset.action = "join";
    }
  }

  async function handleAction() {
    if (!currentClub || !currentUser) {
      alert("Please log in to continue.");
      return;
    }

    const action = actionBtn.dataset.action;
    let endpoint = "";

    if (action === "delete") {
      if (!confirm(`Delete "${currentClub.name}"? This cannot be undone.`)) return;
      endpoint = "/club_api/deleteclub";
    } else if (action === "leave") {
      endpoint = "/club_api/leave";
    } else {
      endpoint = "/club_api/join";
    }

    try {
      const resp = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: currentUser,
          club_id: currentClub.id
        })
      });

      const payload = await resp.json().catch(() => null);

      if (!resp.ok) {
        const msg = payload && payload.error ? payload.error : `HTTP ${resp.status}`;
        alert("Action failed: " + msg);
        return;
      }

      if (action === "delete") {
        window.location.href = "/clubs";
        return;
      }

      await loadClub();
    } catch (err) {
      console.error("Club action error:", err);
      alert("An error occurred.");
    }
  }

  function renderActiveTab() {
    if (!currentClub) return;

    if (activeTab === "members") {
      renderMembers();
    } else if (activeTab === "recent") {
      renderRecentActivity();
    } else {
      renderLeaderboard();
    }
  }

  function renderMembers() {
    const names = currentClub.member_usernames || [];

    if (!names.length) {
      tabContent.innerHTML = `<p class="empty">No members yet.</p>`;
      return;
    }

    tabContent.innerHTML = `
      <div class="club-detail-table-header club-members-table">
        <div>#</div>
        <div>Name</div>
      </div>
      <div class="club-detail-table-list">
        ${names.map((name, index) => `
          <div class="club-detail-table-row club-members-table">
            <div>${index + 1}</div>
            <div>${name}</div>
          </div>
        `).join("")}
      </div>
    `;
  }

  function formatSportLabel(value) {
  const labels = {
    run: "Running",
    bike: "Cycling",
    swim: "Swimming",
    lifting: "Weightlifting",
    walk: "Walking",
    yoga: "Yoga",
    soccer: "Soccer",
    baseball: "Baseball",
    football: "Football",
    tennis: "Tennis",
    volleyball: "Volleyball",
    basketball: "Basketball",
    equestrian: "Equestrian",
    multisport: "Multisport"
  };
  return labels[value] || value;
}

function usesDistanceRanking(sportType) {
  return ["run", "bike", "swim", "walk", "equestrian", "multisport"].includes(sportType);
}

function formatDuration(minutes) {
  const totalSeconds = Math.round(Number(minutes || 0) * 60);

  const hours = Math.floor(totalSeconds / 3600);
  const mins = Math.floor((totalSeconds % 3600) / 60);
  const secs = totalSeconds % 60;

  const paddedHours = String(hours).padStart(2, "0");
  const paddedMins = String(mins).padStart(2, "0");
  const paddedSecs = String(secs).padStart(2, "0");

  return `${paddedHours}:${paddedMins}:${paddedSecs}`;
}

function renderLeaderboard() {
  const lastWeek = currentClub.last_week_leaders || [];
  const thisWeek = currentClub.this_week_leaderboard || [];
  const distanceMode = usesDistanceRanking(currentClub.sport_type);

  tabContent.innerHTML = `
    <div class="club-leaderboard-section">
      <h3>Last Week Leaders</h3>
      ${renderLeaderboardTable(lastWeek, distanceMode, true)}
    </div>

    <div class="club-leaderboard-section">
      <h3>This Week's Leaderboard</h3>
      ${renderLeaderboardTable(thisWeek, distanceMode, false)}
    </div>
  `;
}

function renderLeaderboardTable(rows, distanceMode, topThreeOnly) {
  if (!rows || rows.length === 0) {
    return `<p class="empty">No leaderboard data yet.</p>`;
  }

  const header = distanceMode
    ? `
      <div class="club-detail-table-header club-leaderboard-table-distance">
        <div>Rank</div>
        <div>Name</div>
        <div>Distance</div>
        <div>Time</div>
      </div>
    `
    : `
      <div class="club-detail-table-header club-leaderboard-table-time">
        <div>Rank</div>
        <div>Name</div>
        <div>Total Time</div>
      </div>
    `;

  const body = rows.map(entry => {
    let medal = "";
    if (entry.rank === 1) medal = "🥇 ";
    else if (entry.rank === 2) medal = "🥈 ";
    else if (entry.rank === 3) medal = "🥉 ";

    if (distanceMode) {
      return `
        <div class="club-detail-table-row club-leaderboard-table-distance">
          <div>${medal}#${entry.rank}</div>
          <div>${entry.username}</div>
          <div>${entry.distance} miles</div>
          <div>${formatDuration(entry.time)}</div>
        </div>
      `;
    }

    return `
      <div class="club-detail-table-row club-leaderboard-table-time">
        <div>${medal}#${entry.rank}</div>
        <div>${entry.username}</div>
        <div>${formatDuration(entry.time)}</div>
      </div>
    `;
  }).join("");

  return `
    ${header}
    <div class="club-detail-table-list">
      ${body}
    </div>
  `;
}

  function renderRecentActivity() {
    const recent = currentClub.recent_activity || [];

    if (!recent.length) {
      tabContent.innerHTML = `
        <p class="empty">No recent club activity yet.</p>
      `;
      return;
    }

    tabContent.innerHTML = `
      <div class="club-detail-table-header club-recent-table">
        <div>Name</div>
        <div>Activity</div>
        <div>Date</div>
      </div>
      <div class="club-detail-table-list">
        ${recent.map(row => `
          <div class="club-detail-table-row club-recent-table">
            <div>${row.name}</div>
            <div>${row.activity}</div>
            <div>${row.date}</div>
          </div>
        `).join("")}
      </div>
    `;
  }

  document.querySelectorAll(".club-tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".club-tab-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeTab = btn.dataset.tab;
      renderActiveTab();
    });
  });

  if (actionBtn) {
    actionBtn.addEventListener("click", handleAction);
  }

  await loadClub();
});