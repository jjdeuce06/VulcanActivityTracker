//challenge_details.js:
document.addEventListener("DOMContentLoaded", async () => {
  const challengeName = decodeURIComponent(
    window.location.pathname.split("/").pop()
  );

  const currentUser = localStorage.getItem("currentUser");
  const actionBtn = document.getElementById("challenge-action-btn");

  function formatMetricLabel(metric) {
    const labels = {
      distance: "miles",
      time: "minutes",
      count: "count",
      steps: "steps",
      sets: "sets",
      intensity: "intensity",
      goals: "goals",
      assists: "assists",
      hits: "hits",
      runs: "runs",
      touchdowns: "touchdowns",
      kills: "kills",
      points: "points",
      rebounds: "rebounds"
    };
    return labels[metric] || metric || "";
  }

  function formatActivityLabel(activity) {
    const labels = {
      run: "Run",
      bike: "Bike",
      swim: "Swim",
      lifting: "Lift",
      walk: "Walk",
      yoga: "Do yoga",
      soccer: "Play soccer for",
      baseball: "Play baseball for",
      football: "Play football for",
      tennis: "Play tennis for",
      volleyball: "Play volleyball for",
      basketball: "Play basketball for",
      equestrian: "Do equestrian for"
    };
    return labels[activity] || activity || "Complete";
  }

  function getGoalText(challenge) {
    const activityText = formatActivityLabel(challenge.activity_type);
    const metricText = formatMetricLabel(challenge.metric_type);
    return `${activityText} ${challenge.target_value} ${metricText}`;
  }

  function parseLocalDate(dateStr) {
  const [year, month, day] = dateStr.split("-").map(Number);
  return new Date(year, month - 1, day);
}

 function getDaysLeftText(startDateStr, endDateStr) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const startDate = parseLocalDate(startDateStr);
  startDate.setHours(0, 0, 0, 0);

  const endDate = parseLocalDate(endDateStr);
  endDate.setHours(0, 0, 0, 0);

  const msPerDay = 1000 * 60 * 60 * 24;

  if (today < startDate) {
    const daysUntilStart = Math.round((startDate - today) / msPerDay);
    return `Starts in ${daysUntilStart} day${daysUntilStart === 1 ? "" : "s"}`;
  }

  if (today > endDate) {
    return "Completed";
  }

  const daysLeft = Math.round((endDate - today) / msPerDay);
  return `${daysLeft} day${daysLeft === 1 ? "" : "s"} left`;
}

  function renderLeaderboard(leaderboard, metricType) {
    const leaderboardList = document.getElementById("leaderboard-list");
    leaderboardList.innerHTML = "";

    if (!leaderboard || leaderboard.length === 0) {
      leaderboardList.innerHTML = "<p class='empty'>No leaderboard data yet.</p>";
      return;
    }

leaderboard.forEach(entry => {
  const row = document.createElement("div");
  row.className = "challenge-detail-leaderboard-row";

  let medal = "";
  if (entry.rank === 1) {
    medal = '<span class="leaderboard-medal medal-gold">🥇</span>';
    row.classList.add("leaderboard-first");
  } else if (entry.rank === 2) {
    medal = '<span class="leaderboard-medal medal-silver">🥈</span>';
    row.classList.add("leaderboard-second");
  } else if (entry.rank === 3) {
    medal = '<span class="leaderboard-medal medal-bronze">🥉</span>';
    row.classList.add("leaderboard-third");
  }

  row.innerHTML = `
    <div class="challenge-detail-rank">${medal} #${entry.rank}</div>
    <div class="challenge-detail-name">${entry.username}</div>
    <div class="challenge-detail-progress">
      <div class="challenge-detail-progress-text">
        ${entry.current} / ${entry.target} ${formatMetricLabel(metricType)}
      </div>
      <div class="progress-container">
        <div class="progress-bar" style="width: ${entry.percent}%;"></div>
      </div>
    </div>
  `;

  leaderboardList.appendChild(row);
    });
  }

  function setActionButton(challenge) {
  if (!actionBtn) return;

  const participantDetails = challenge.participant_details || [];
  const isOwner = currentUser === challenge.creator_username;
  const isJoined = participantDetails.some(
    participant => participant.username === currentUser
  );

  if (isOwner) {
    actionBtn.textContent = "Delete Challenge";
    actionBtn.dataset.action = "delete";
  } else if (isJoined) {
    actionBtn.textContent = "Leave Challenge";
    actionBtn.dataset.action = "leave";
  } else {
    actionBtn.textContent = "Join Challenge";
    actionBtn.dataset.action = "join";
  }

  actionBtn.dataset.challengeId = challenge.id;
}

  async function handleActionClick() {
    if (!actionBtn) return;

    const username = localStorage.getItem("currentUser");
    if (!username) {
      alert("Please log in to continue.");
      return;
    }

    const challengeId = actionBtn.dataset.challengeId;
    const action = actionBtn.dataset.action;

    if (!challengeId || !action) return;

    if (action === "delete") {
      const confirmed = window.confirm("Delete this challenge? This cannot be undone.");
      if (!confirmed) return;
      }

    

    let endpoint = "";

    if (action === "delete") {
      endpoint = "/challenges_api/deletechallenge";
    } else if (action === "leave") {
      endpoint = "/challenges_api/leave";
    } else {
       endpoint = "/challenges_api/join";
    }

    try {
      const resp = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          challenge_id: challengeId
        })
      });

      const payload = await resp.json().catch(() => null);

      if (!resp.ok) {
        const msg = payload && payload.error ? payload.error : `HTTP ${resp.status}`;
        alert("Action failed: " + msg);
        return;
      }

      if (action === "delete") {
        window.location.href = "/challenges";
      } else {
        window.location.reload();
      }
    } catch (err) {
      console.error("Challenge action error:", err);
      alert("An error occurred.");
    }
  }

  if (actionBtn) {
    actionBtn.addEventListener("click", handleActionClick);
  }

  try {
    const resp = await fetch("/challenges_api/challengedetail", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ challenge_name: challengeName })
    });

    if (!resp.ok) {
      alert("challenge not found");
      history.back();
      return;
    }

    const data = await resp.json();
    const challenge = data.challenge;

    document.getElementById("challenge-name-heading").textContent = challenge.name;
    document.getElementById("challenge-description").textContent =
      challenge.description || "No description provided.";
    document.getElementById("challenge-start-date").textContent = challenge.start_date || "";
    document.getElementById("challenge-end-date").textContent = challenge.end_date || "";
    document.getElementById("challenge-days-left").textContent =
      getDaysLeftText(challenge.start_date, challenge.end_date);
    document.getElementById("challenge-goal-text").textContent =
      getGoalText(challenge);
    document.getElementById("challenge-activity-type").textContent =
      challenge.activity_type || "";
    document.getElementById("challenge-metric-type").textContent =
      challenge.metric_type || "";
    document.getElementById("challenge-target-value").textContent =
      challenge.target_value ?? "";
    document.getElementById("participant-count").textContent =
      challenge.participants ? challenge.participants.length : 0;

    setActionButton(challenge);
    renderLeaderboard(challenge.leaderboard || [], challenge.metric_type);
  } catch (err) {
    console.error("Error loading challenge:", err);
    alert("Error loading challenge");
  }
});