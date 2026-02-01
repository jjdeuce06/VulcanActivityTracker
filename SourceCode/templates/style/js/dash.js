document.addEventListener("DOMContentLoaded", async () => {
    const username = localStorage.getItem("currentUser");
    console.log("user from dash:", username);
    if (username) {
        document.getElementById("user-name").textContent = username;
    }

    await fillDashActivity(username);




});



async function fillDashActivity(username) {
  try {
    const response = await fetch("/activity_api/fillDashAct", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username })
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    console.log(data);

    //ensure array
    const activities = Array.isArray(data)
      ? data
      : data.activities;

    populateDashActivity(activities);


    return activities;

  } catch (err) {
    console.error("Failed to load activities:", err);
  }
}


function populateDashActivity(data) {
  const feedContainer = document.querySelector("#activity-feed");
  feedContainer.innerHTML = ""; // clear old feed

  // Fill the activity count using the array length
  const activityCountDiv = document.querySelector("#activity-count");
  activityCountDiv.textContent = data?.length ?? 0;

  if (!data || data.length === 0) {
    feedContainer.innerHTML = `
      <div class="feed-card">
        <div class="no-activities">No activities yet.</div>
      </div>
    `;
    return;
  }

  data.forEach(activity => {
    const common = activity.common ?? activity;
    const sport  = activity.sport  ?? activity;

    let extra = "";
    if (common.activity_type === "swim" && sport.distance) {
      extra = `${sport.distance} ${sport.unit}`;
    }

    const dateObj = new Date(common.date);
    const formattedDate = !isNaN(dateObj)
      ? dateObj.toLocaleDateString("en-US", { year:"numeric", month:"short", day:"numeric" })
      : "Unknown Date";

    // Create card without inline styles
    const card = document.createElement("div");
    card.className = "card feed-card";
    card.innerHTML = `
    <div class="feed-title">${common.activity_type.toUpperCase()}</div>
    <div class="feed-meta">${formattedDate} • ${common.visibility}</div>
    <div class="feed-details">
        Duration: ${common.duration ?? "N/A"} min • Calories: ${common.calories_burned ?? "N/A"}${extra ? " • " + extra : ""}
    </div>
    ${common.notes ? `<div class="feed-notes">Notes: ${common.notes}</div>` : ""}
    `;


    feedContainer.appendChild(card);
  });
}
