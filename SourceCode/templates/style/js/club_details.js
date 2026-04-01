document.addEventListener("DOMContentLoaded", async () => {
  const clubId = window.location.pathname.split("/").pop();
  const currentUser = localStorage.getItem("currentUser");
  const tabContent = document.getElementById("club-tab-content");
  const actionBtn = document.getElementById("club-action-btn");

  let currentClub = null;
  let activeTab = "leaderboard";

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

  function loadActivityLikeCount(username, activityId, countElement) {
  fetch("/dash_api/thumbCount", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username,
      activity_id: activityId
    })
  })
    .then(response => {
      if (!response.ok) return null;
      return response.json();
    })
    .then(data => {
      if (data && data.status === "ok" && countElement) {
        countElement.textContent = data.activity_total_likes || 0;
      }
    })
    .catch(err => {
      console.error("Failed to load activity like count:", err);
    });
}

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

      setupActionButton(club);

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

  function renderLeaderboardTable(rows, distanceMode) {
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
  const username = localStorage.getItem("currentUser");

  if (!recent.length) {
    tabContent.innerHTML = `<p class="empty">No recent club activity yet.</p>`;
    return;
  }

  const topActivities = [...recent]
    .sort((a, b) => new Date(b.date) - new Date(a.date));

  tabContent.innerHTML = "";

  topActivities.forEach(act => {
    let extra = "";

    if (act.activity_type?.toLowerCase() === "swim" && act.distance) {
      extra = `${act.distance} ${act.unit || ""}`.trim();
    } else if (act.distance) {
      extra = `${act.distance} ${act.unit || "miles"}`.trim();
    }

    const dateObj = new Date(act.date);
    const formattedDate = !isNaN(dateObj)
      ? dateObj.toLocaleDateString("en-US", {
          year: "numeric",
          month: "short",
          day: "numeric"
        })
      : "Unknown Date";

    const card = document.createElement("div");
    card.className = "card feed-card club-recent-feed-card";

    card.innerHTML = `
      <div class="feed-title">${(act.activity_type || "Activity").toUpperCase()}</div>
      <div class="feed-meta">${formattedDate} • ${act.username}</div>
      <div class="feed-details">
        Duration: ${act.duration ?? "N/A"} min • Calories: ${act.calories_burned ?? "N/A"}${extra ? " • " + extra : ""}
      </div>
      ${act.notes ? `<div class="feed-notes">Notes: ${act.notes}</div>` : ""}
      <div class="stat">
        <div class="label"></div>
        <div class="onActivity-like">
          <button style="background: none; border: none; padding: 0; margin: 0;"
                  class="onActivity-likebtn"
                  data-activity-id="${act.activity_id}">👍</button>
          <span class="onActivity-like-count">0</span>
        </div>
      </div>
    `;

    tabContent.appendChild(card);

    const likeBtn = card.querySelector(".onActivity-likebtn");
    const likeCount = card.querySelector(".onActivity-like-count");

    if (likeBtn && likeCount) {
      loadActivityLikeCount(username, act.activity_id, likeCount);

      if (username !== act.username) {
        thumbsUp(username, act.username, act.activity_id, likeBtn, likeCount);
      } else {
        likeBtn.classList.add("disabled-like-btn");
        likeBtn.style.cursor = "default";
      }
    }
  });
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