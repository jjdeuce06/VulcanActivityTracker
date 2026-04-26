//challenges.js:

// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {

  // ---------------- ELEMENT REFERENCES ----------------
  const form = document.getElementById("create-challenge-form");

  const activitySelect = document.getElementById("challenge-activity-type");
  const metricSelect = document.getElementById("challenge-metric-type");
  const targetLabel = document.getElementById("challenge-target-label");


  // ---------------- METRIC OPTIONS BY SPORT ----------------
  // Determines which metrics are available for each sport
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


  // ---------------- METRIC LABELS (DISPLAY TEXT) ----------------
  // Provides user-friendly descriptions for metrics
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
    // (continues for each sport...)
  };


  // ---------------- UPDATE TARGET LABEL ----------------
  // Updates label text based on selected sport + metric
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


  // ---------------- DROPDOWN CHANGE HANDLING ----------------
  if (activitySelect && metricSelect) {

    // When sport changes → update metric options
    activitySelect.addEventListener("change", () => {
      const sport = activitySelect.value;

      // Get valid metrics for selected sport
      const metrics = metricOptionsBySport[sport] || ["time", "count"];

      // Clear dropdown
      metricSelect.innerHTML = "";

      // Populate new metric options
      metrics.forEach(metric => {
        const option = document.createElement("option");
        option.value = metric;
        option.textContent = metric.charAt(0).toUpperCase() + metric.slice(1);
        metricSelect.appendChild(option);
      });

      updateTargetLabel();
    });

    // When metric changes → update label
    metricSelect.addEventListener("change", updateTargetLabel);

    // Initial label setup
    updateTargetLabel();
  }


  // ---------------- LOAD CHALLENGES ----------------
  async function loadChallenges() {
    try {
      const username = localStorage.getItem("currentUser");

      // If not logged in
      if (!username) {
        console.warn("No logged-in user");
        renderChallenges("all-challenge-list", [], false);
        renderChallenges("my-challenge-list", data.challenges || [], true);
        renderMedals(data.medals || { gold: 0, silver: 0, bronze: 0, completed: 0 });
        return;
      }

      // -------- FETCH ALL CHALLENGES --------
      const allResp = await fetch("/challenges_api/listchallenges", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
      });

      if (allResp.ok) {
        const data = await allResp.json();
        renderChallenges("all-challenge-list", data.challenges || [], false);
      }

      // -------- FETCH USER'S CHALLENGES --------
      const myResp = await fetch("/challenges_api/mychallenges", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
      });

      if (myResp.ok) {
        const data = await myResp.json();

        renderChallenges("my-challenge-list", data.challenges || [], true);

        // Render medal counts
        renderMedals(data.medals || { gold: 0, silver: 0, bronze: 0, completed: 0 });
      }

    } catch (err) {
      console.error("Error loading challenges:", err);
    }
  }

  // Expose function globally
  window.loadChallenges = loadChallenges;


  // ---------------- CREATE CHALLENGE ----------------
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = localStorage.getItem("currentUser");

      // Gather form data
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

      // Validate required field
      if (!data.challengeName) {
        alert("Challenge name required");
        return;
      }

      try {
        // Send create request
        const response = await fetch("/challenges_api/createchallenge", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          const err = await response.json().catch(() => ({}));
          throw new Error(err.error || `HTTP ${response.status}`);
        }

        // Reset form + redirect
        form.reset();
        window.location.href = "/challenges";

      } catch (err) {
        console.error("Create challenge error:", err);
        alert(err.message || "Failed to create challenge");
      }
    });
  }

  // Initial load
  loadChallenges();
});


// ---------------- RENDER CHALLENGE CARDS ----------------
function renderChallenges(containerId, challenges, isParticipant) {

  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "";

  // Handle empty state
  if (!challenges || challenges.length === 0) {
    container.innerHTML = "<p class='empty'>No challenges found.</p>";
    return;
  }

  const currentUser = localStorage.getItem("currentUser");

  challenges.forEach(challenge => {

    const card = document.createElement("div");
    card.className = "challengepage-item";

    const participants = challenge.participants !== undefined ? challenge.participants : [];

    // Check ownership
    const isOwner = isParticipant && challenge.creator_username === currentUser;

    // Build card UI
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

      <!-- Progress (only if user is participant) -->
      ${isParticipant && challenge.progress ? `
      <div class="challenge-progress">
        <p class="challengepage-progress-text">
          ${challenge.progress.current} / ${challenge.progress.target} ${formatMetricLabel(challenge.metric_type)}
        </p>
        <div class="progress-container">
          <div class="progress-bar"
               style="width: ${challenge.progress.percent}%;"></div>
        </div>
      </div>
      ` : ""}

      <!-- Action buttons -->
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


    // ---------------- ACTION BUTTON ----------------
    const actionBtn = card.querySelector("button.secondary-btn[data-action]");

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

          if (!resp.ok) {
            alert("Action failed");
            return;
          }

          // Reload challenges after action
          await (window.loadChallenges ? window.loadChallenges() : Promise.resolve());

        } catch (err) {
          console.error("Challenge action error:", err);
          alert("An error occurred.");
        }
      });
    }


    // ---------------- VIEW BUTTON ----------------
    const viewBtn = card.querySelector("button.view-challenge-btn");

    if (viewBtn) {
      viewBtn.addEventListener("click", () => {
        window.location.href = `/challenge/${encodeURIComponent(challenge.name)}`;
      });
    }

  });
}


// ---------------- FORMAT METRIC LABEL ----------------
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


// ---------------- RENDER MEDALS ----------------
function renderMedals(medals) {

  document.getElementById("gold-medal-count").textContent = medals?.gold ?? 0;
  document.getElementById("silver-medal-count").textContent = medals?.silver ?? 0;
  document.getElementById("bronze-medal-count").textContent = medals?.bronze ?? 0;
  document.getElementById("completed-count").textContent = medals?.completed ?? 0;
}