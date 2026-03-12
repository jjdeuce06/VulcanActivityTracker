//challenges.js:
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("create-challenge-form");

  const activitySelect = document.getElementById("challenge-activity-type");
  const metricSelect = document.getElementById("challenge-metric-type");
  const targetLabel = document.getElementById("challenge-target-label");

  const metricOptionsBySport = {
    run: ["distance", "time", "count"],
    bike: ["distance", "time", "count"],
    swim: ["distance", "time", "count"],
    equestrian: ["distance", "time", "count"],
    walk: ["steps", "time", "count"],
    lifting: ["sets", "time", "count"],
    yoga: ["intensity", "time", "count"],
    soccer: ["goals", "assists", "time", "count"],
    baseball: ["hits", "runs", "time", "count"],
    football: ["touchdowns", "time", "count"],
    tennis: ["time", "count"],
    volleyball: ["kills", "time", "count"],
    basketball: ["points", "rebounds", "assists", "time", "count"]
  };

  const metricLabelsBySport = {
  run: {
    distance: "Total Running Distance (in miles)",
    time: "Total Running Time (in minutes)",
    count: "Total Run Count"
  },
  bike: {
    distance: "Total Cycling Distance (in miles)",
    time: "Total Cycling Time (in minutes)",
    count: "Total Ride Count"
  },
  swim: {
    distance: "Total Swimming Distance (in meters)",
    time: "Total Swimming Time (in minutes)",
    count: "Total Swim Count"
  },
  equestrian: {
    distance: "Total Equestrian Distance (in miles)",
    time: "Total Riding Time (in minutes)",
    count: "Total Ride Count"
  },
  walk: {
    steps: "Total Walking Steps",
    time: "Total Walking Time (in minutes)",
    count: "Total Walk Count"
  },
  lifting: {
    sets: "Total Sets",
    time: "Total Lifting Time (in minutes)",
    count: "Total Workout Count"
  },
  yoga: {
    intensity: "Total Yoga Intensity",
    time: "Total Yoga Time (in minutes)",
    count: "Total Yoga Session Count"
  },
  soccer: {
    goals: "Total Goals",
    assists: "Total Assists",
    time: "Total Playing Time (in minutes)",
    count: "Total Match Count"
  },
  baseball: {
    hits: "Total Hits",
    runs: "Total Runs",
    time: "Total Playing Time (in minutes)",
    count: "Total Game Count"
  },
  football: {
    touchdowns: "Total Touchdowns",
    time: "Total Playing Time (in minutes)",
    count: "Total Game Count"
  },
  tennis: {
    time: "Total Playing Time (in minutes)",
    count: "Total Match Count"
  },
  volleyball: {
    kills: "Total Kills",
    time: "Total Playing Time (in minutes)",
    count: "Total Match Count"
  },
  basketball: {
    points: "Total Points",
    rebounds: "Total Rebounds",
    assists: "Total Assists",
    time: "Total Playing Time (in minutes)",
    count: "Total Game Count"
  }
};


  function updateTargetLabel() {
  if (!activitySelect || !metricSelect || !targetLabel) return;

  const sport = activitySelect.value;
  const metric = metricSelect.value;

  const label =
    metricLabelsBySport[sport] &&
    metricLabelsBySport[sport][metric]
      ? metricLabelsBySport[sport][metric]
      : "Target Goal";

  targetLabel.textContent = label;
  }

  if (activitySelect && metricSelect) {
    activitySelect.addEventListener("change", () => {
      const sport = activitySelect.value;
      const metrics = metricOptionsBySport[sport] || ["time", "count"];

      metricSelect.innerHTML = "";

      metrics.forEach(metric => {
        const option = document.createElement("option");
        option.value = metric;
        option.textContent = metric.charAt(0).toUpperCase() + metric.slice(1);
        metricSelect.appendChild(option);
      });

      updateTargetLabel();
    });

    metricSelect.addEventListener("change", updateTargetLabel);

    updateTargetLabel();
  }

  async function loadChallenges() {
  try {
    const username = localStorage.getItem("currentUser");

    if (!username) {
      console.warn("No logged-in user");
      renderChallenges("all-challenge-list", [], false);
      renderChallenges("my-challenge-list", [], true);
      return;
    }

    // Fetch Challenges user is NOT part of
    const allResp = await fetch("/challenges_api/listchallenges", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });

    if (allResp.ok) {
      const data = await allResp.json();
      renderChallenges("all-challenge-list", data.challenges || [], false);
    } else {
      console.error("Failed to load challenges", allResp.status);
    }

    // Fetch user's Challenges
    const myResp = await fetch("/challenges_api/mychallenges", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });

    if (myResp.ok) {
      const data = await myResp.json();
      renderChallenges("my-challenge-list", data.challenges || [], true);
    } else {
      console.error("Failed to load my challenges", myResp.status);
    }

  } catch (err) {
    console.error("Error loading challenges:", err);
  }
}

  window.loadChallenges = loadChallenges;//

  if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = localStorage.getItem("currentUser");

    const data = {
      username: username,
      challengeName: document.getElementById("challenge-name").value.trim(),
      description: document.getElementById("challenge-description").value.trim(),
      activityType: document.getElementById("challenge-activity-type").value,
      metricType: document.getElementById("challenge-metric-type").value,
      targetValue: parseFloat(document.getElementById("challenge-target").value),
      startDate: document.getElementById("start-date").value,
      endDate: document.getElementById("end-date").value
    };

    if (!data.challengeName) {
      alert("Challenge name required");
      return;
    }

    try {
      const response = await fetch("/challenges_api/createchallenge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || `HTTP ${response.status}`);
      }

      alert("Challenge created!");
      form.reset();
      window.location.href = "/challenges";
    } catch (err) {
      console.error("Create challenge error:", err);
      alert(err.message || "Failed to create challenge");
    }
  });
}

  loadChallenges();
});

function renderChallenges(containerId, challenges, isParticipant) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = "";

  if (!challenges || challenges.length === 0) {
    container.innerHTML = "<p class='empty'>No challenges found.</p>";
    return;
  }

  const currentUser = localStorage.getItem("currentUser");

  challenges.forEach(challenge => {
    const card = document.createElement("div");
    card.className = "challengepage-item";

    const participants = challenge.participants !== undefined ? challenge.participants : [];
    const isOwner = isParticipant && challenge.creator_username === currentUser

    card.innerHTML = `
      <div class="challengepage-card-top">
      <h4>${challenge.name}</h4>
      <div class="challengepage-card-dates">
        <span><strong>Start:</strong> ${challenge.start_date || ""}</span>
        <span><strong>End:</strong> ${challenge.end_date || ""}</span>
      </div>
      </div>

      <p class="challengepage-description-text">${challenge.description || ""}</p>
      <p>${participants.length} participants</p>

      <p><strong>Activity:</strong> ${challenge.activity_type}</p>
      <p><strong>Metric:</strong> ${challenge.metric_type}</p>

      ${isParticipant && challenge.progress ? `
    <div class="challenge-progress">
      <p class="challengepage-progress-text">
        ${challenge.progress.current} / ${challenge.progress.target} ${formatMetricLabel(challenge.metric_type)}
      </p>
      <div class="progress-container">
        <div class="progress-bar"
             style="width: ${challenge.progress.percent}%;">
        </div>
      </div>
    </div>
    ` : ""}

      <div class="challengepage-card-buttons">
      <button class="secondary-btn view-challenge-btn" data-challenge-id="${challenge.id}">
        View
      </button>
      <button class="secondary-btn" data-challenge-id="${challenge.id}" data-action="${isOwner ? 'delete' : (isParticipant ? 'leave' : 'join')}">
        ${isOwner ? "Delete" : (isParticipant ? "Leave" : "Join")}
      </button>
      </div>
    `;

    container.appendChild(card);

   

    const actionBtn = card.querySelector("button.secondary-btn[data-action]");  // Get the second button
if (actionBtn) {
  actionBtn.addEventListener("click", async () => {
    const username = localStorage.getItem("currentUser");
    if (!username) {
      alert("Please log in to continue.");
      return;
    }
    
    const challengeId = actionBtn.dataset.challengeId;
    const action = actionBtn.dataset.action;
    let endpoint = "";

    if (action === "delete") {
      if (!confirm(`Delete this challenge? This cannot be undone.`)) return;
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
        body: JSON.stringify({ username, challenge_id: challengeId })
      });

      const payload = await resp.json().catch(() => null);
      console.log(endpoint, resp.status, payload);

      if (!resp.ok) {
        const msg = payload && payload.error ? payload.error : `HTTP ${resp.status}`;
        alert("Action failed: " + msg);
        return;
      }

      await (window.loadChallenges ? window.loadChallenges() : Promise.resolve());
    } catch (err) {
      console.error("Challenge action error:", err);
      alert("An error occurred.");
    }
  });
}

  const viewBtn = card.querySelector("button.view-challenge-btn");
    if (viewBtn) {
      viewBtn.addEventListener("click", () => {
        window.location.href = `/challenge/${encodeURIComponent(challenge.name)}`;
      });
    }

  });
}

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