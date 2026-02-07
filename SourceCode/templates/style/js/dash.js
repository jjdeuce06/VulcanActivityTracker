document.addEventListener("DOMContentLoaded", async () => {
  const username = localStorage.getItem("currentUser");
  if (username) {
    document.getElementById("user-name").textContent = username;
  }

  await fillDashActivity(username);
  await fillDashFriends(username); // pass current user for filtering

  const fBtn = document.getElementById("friendBtn");
  const dropdown = document.getElementById("friendDropdown");

  // toggle dropdown visibility
  fBtn.addEventListener("click", () => {
    dropdown.style.display =
      dropdown.style.display === "none" ? "block" : "none";
  });

  // when a user is selected from the dropdown, call addFriend()
  dropdown.addEventListener("change", (e) => {
    const selectedUser = e.target.value;
    addFriend(selectedUser); // <--- use the function
  });
});


// single GET to populate dropdown
async function fillDashFriends(currentUser) {
  try {
    const response = await fetch("/dash_api/sendFriendsList");
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const users = await response.json(); // array of usernames
    const dropdown = document.getElementById("friendDropdown");
    dropdown.innerHTML = `<option value="">Select a user</option>`; // reset

    // filter out current user
    const filteredUsers = users.filter(u => u !== currentUser);

    filteredUsers.forEach(user => {
      const opt = document.createElement("option");
      opt.value = user;
      opt.textContent = user;
      dropdown.appendChild(opt);
    });

    // show button only if users exist
    const fBtn = document.getElementById("friendBtn");
    fBtn.style.display = filteredUsers.length ? "inline-block" : "none";

  } catch (err) {
    console.error("Failed to load users:", err);
  }
}

async function addFriend(selectedUser) {
  if (!selectedUser) return;

  const list = document.getElementById("friends-list");
  const dropdown = document.getElementById("friendDropdown");

  // Add selected user to UI
  if (list.textContent.trim() === "show friends") list.textContent = "";
  const div = document.createElement("div");
  div.textContent = selectedUser;
  list.appendChild(div);

  // Remove from dropdown
  const optionToRemove = Array.from(dropdown.options).find(opt => opt.value === selectedUser);
  if (optionToRemove) optionToRemove.remove();

  // Hide dropdown and reset selection
  dropdown.style.display = "none";
  dropdown.value = "";

  // Send to backend
  const currentUser = localStorage.getItem("currentUser");
  if (!currentUser) return;

  try {
    const response = await fetch("/dash_api/addFriend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ currentUser, friendUser: selectedUser })
    });

    const result = await response.json();
    console.log("result", result);
    if (result.status !== "ok") {
      console.error("Failed to save friend:", result.message);
    } else {
      console.log("Friend saved:", selectedUser);
    }
  } catch (err) {
    console.error("Error saving friend:", err);
  }
}


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
