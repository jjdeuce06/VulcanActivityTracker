// Wait for page load
document.addEventListener("DOMContentLoaded", async () => {

  // ---------------- INITIAL SETUP ----------------
  const clubId = window.location.pathname.split("/").pop(); // Extract club ID from URL
  const currentUser = localStorage.getItem("currentUser");  // Current logged-in user

  const tabContent = document.getElementById("club-tab-content"); // Main tab content area
  const actionBtn = document.getElementById("club-action-btn");   // Join/Leave/Delete button

  let currentClub = null; // Stores loaded club data
  let activeTab = "leaderboard"; // Default tab


  // ---------------- FORMAT SPORT LABEL ----------------
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


  // ---------------- DETERMINE LEADERBOARD TYPE ----------------
  function usesDistanceRanking(sportType) {
    return ["run", "bike", "swim", "walk", "equestrian", "multisport"].includes(sportType);
  }


  // ---------------- FORMAT TIME ----------------
  function formatDuration(minutes) {
    const totalSeconds = Math.round(Number(minutes || 0) * 60);

    const hours = Math.floor(totalSeconds / 3600);
    const mins = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;

    return `${String(hours).padStart(2,"0")}:${String(mins).padStart(2,"0")}:${String(secs).padStart(2,"0")}`;
  }


  // ---------------- LOAD ACTIVITY LIKE COUNT ----------------
  function loadActivityLikeCount(username, activityId, countElement) {
    fetch("/dash_api/thumbCount", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ username, activity_id: activityId })
    })
    .then(res => res.ok ? res.json() : null)
    .then(data => {
      if (data && data.status === "ok" && countElement) {
        countElement.textContent = data.activity_total_likes || 0;
      }
    })
    .catch(err => console.error("Failed to load activity like count:", err));
  }


  // ---------------- LOAD CLUB DATA ----------------
  async function loadClub() {
    try {
      const resp = await fetch("/club_api/clubdetail", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
          club_id: clubId,
          username: currentUser
        })
      });

      // Handle not found
      if (!resp.ok) {
        alert("Club not found");
        history.back();
        return;
      }

      const data = await resp.json();
      const club = data.club;
      currentClub = club;

      // Populate UI
      document.getElementById("club-name-heading").textContent = club.name;
      document.getElementById("club-description").textContent =
        club.description || "No description provided.";

      const memberCount = document.getElementById("member-count");
      const sportType = document.getElementById("club-sport-type");
      const privacy = document.getElementById("club-privacy");
      const leftColumn = document.querySelector(".club-detail-left");

      if (memberCount) {
        memberCount.textContent =
          club.total_members ?? ((club.members?.length || 0) + 1);
      }

      if (sportType) {
        sportType.textContent = formatSport(club.sport_type || "unknown");
      }

      if (privacy) {
        privacy.textContent = club.is_private ? "Private" : "Public";
      }

      // Setup join/leave/delete button
      setupActionButton(club);

      // Handle private club restrictions
      if (!club.can_view_private_content) {
        if (memberCount) memberCount.textContent = "-";
        if (leftColumn) leftColumn.style.display = "none";
      } else {
        if (leftColumn) leftColumn.style.display = "";
        renderActiveTab();
      }

    } catch (err) {
      console.error("Error loading club:", err);
      alert("Error loading club");
    }
  }


  // ---------------- ACTION BUTTON STATE ----------------
  function setupActionButton(club) {
    if (!actionBtn) return;

    if (club.is_owner) {
      actionBtn.textContent = "Delete Club";
      actionBtn.dataset.action = "delete";
    } else if (club.is_member) {
      actionBtn.textContent = "Leave Club";
      actionBtn.dataset.action = "leave";
    } else if (club.is_private) {
      if (club.has_pending_request) {
        actionBtn.textContent = "Cancel Join Request";
        actionBtn.dataset.action = "cancel_request";
      } else {
        actionBtn.textContent = "Request to Join";
        actionBtn.dataset.action = "request_join";
      }
    } else {
      actionBtn.textContent = "Join Club";
      actionBtn.dataset.action = "join";
    }
  }


  // ---------------- HANDLE BUTTON ACTION ----------------
  async function handleAction() {
    if (!currentClub || !currentUser) {
      alert("Please log in to continue.");
      return;
    }

    const action = actionBtn.dataset.action;
    let endpoint = "";

    // Determine endpoint
    if (action === "delete") {
      if (!confirm(`Delete "${currentClub.name}"?`)) return;
      endpoint = "/club_api/deleteclub";
    } else if (action === "leave") {
      endpoint = "/club_api/leave";
    } else if (action === "request_join") {
      endpoint = "/club_api/requestjoin";
    } else if (action === "cancel_request") {
      endpoint = "/club_api/cancelrequest";
    } else {
      endpoint = "/club_api/join";
    }

    try {
      const resp = await fetch(endpoint, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
          username: currentUser,
          club_id: currentClub.id
        })
      });

      if (!resp.ok) {
        alert("Action failed");
        return;
      }

      // Redirect if deleted
      if (action === "delete") {
        window.location.href = "/clubs";
        return;
      }

      // Reload club data
      await loadClub();

    } catch (err) {
      console.error("Club action error:", err);
      alert("An error occurred.");
    }
  }


  // ---------------- TAB RENDERING ----------------
  function renderActiveTab() {
    if (!currentClub) return;

    if (activeTab === "members") renderMembers();
    else if (activeTab === "recent") renderRecentActivity();
    else renderLeaderboard();
  }


  // ---------------- MEMBERS TAB ----------------
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
        ${names.map((name,i)=>`
          <div class="club-detail-table-row club-members-table">
            <div>${i+1}</div>
            <div>${name}</div>
          </div>
        `).join("")}
      </div>
    `;
  }


  // ---------------- LEADERBOARD TAB ----------------
  function renderLeaderboard() {
    const lastWeek = currentClub.last_week_leaders || [];
    const thisWeek = currentClub.this_week_leaderboard || [];

    const distanceMode = usesDistanceRanking(currentClub.sport_type);

    tabContent.innerHTML = `
      <div class="club-leaderboard-section">
        <h3>Last Week Leaders</h3>
        ${renderLeaderboardTable(lastWeek, distanceMode)}
      </div>

      <div class="club-leaderboard-section">
        <h3>This Week's Leaderboard</h3>
        ${renderLeaderboardTable(thisWeek, distanceMode)}
      </div>
    `;
  }


  // ---------------- LEADERBOARD TABLE ----------------
  function renderLeaderboardTable(rows, distanceMode) {

    if (!rows || rows.length === 0) {
      return `<p class="empty">No leaderboard data yet.</p>`;
    }

    const body = rows.map(entry => {
      let medal = entry.rank === 1 ? "🥇 " :
                  entry.rank === 2 ? "🥈 " :
                  entry.rank === 3 ? "🥉 " : "";

      if (distanceMode) {
        return `
          <div class="club-detail-table-row">
            <div>${medal}#${entry.rank}</div>
            <div>${entry.username}</div>
            <div>${entry.distance} miles</div>
            <div>${formatDuration(entry.time)}</div>
          </div>
        `;
      }

      return `
        <div class="club-detail-table-row">
          <div>${medal}#${entry.rank}</div>
          <div>${entry.username}</div>
          <div>${formatDuration(entry.time)}</div>
        </div>
      `;
    }).join("");

    return `<div class="club-detail-table-list">${body}</div>`;
  }


  // ---------------- RECENT ACTIVITY TAB ----------------
  function renderRecentActivity() {
    const recent = currentClub.recent_activity || [];

    if (!recent.length) {
      tabContent.innerHTML = `<p class="empty">No recent club activity yet.</p>`;
      return;
    }

    tabContent.innerHTML = "";

    recent.forEach(act => {

      const card = document.createElement("div");
      card.className = "card feed-card";

      card.innerHTML = `
        <div>${act.activity_type}</div>
        <div>${act.username}</div>
      `;

      tabContent.appendChild(card);
    });
  }


  // ---------------- TAB BUTTON EVENTS ----------------
  document.querySelectorAll(".club-tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".club-tab-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeTab = btn.dataset.tab;
      renderActiveTab();
    });
  });


  // Attach action button
  if (actionBtn) {
    actionBtn.addEventListener("click", handleAction);
  }

  // Initial load
  await loadClub();
});