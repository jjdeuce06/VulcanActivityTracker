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
    addFriend(selectedUser);
  });
});


async function fillDashFriends(currentUser) {
  try {
    const response = await fetch("/dash_api/sendFriendsList", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ currentUser })
    });

    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const data = await response.json(); 
    const existingFriends = data.existing_friends || [];
    const allUsers = data.all_users || [];

    const dropdown = document.getElementById("friendDropdown");
    dropdown.innerHTML = `<option value="">Select a user</option>`; // reset

    // filter out current user and already added friends
    const addableUsers = allUsers.filter(u => u !== currentUser && !existingFriends.includes(u));

    addableUsers.forEach(user => {
      const opt = document.createElement("option");
      opt.value = user;
      opt.textContent = user;
      dropdown.appendChild(opt);
    });

    // Show button even if some users were added; hide only if nothing to add
    const fBtn = document.getElementById("friendBtn");
    fBtn.style.display = addableUsers.length || existingFriends.length ? "inline-block" : "none";

    // populate friends card with existing friends
    const friendsList = document.getElementById("friends-list");
    friendsList.innerHTML = "";
    if (existingFriends.length === 0) {
      friendsList.textContent = "No Friends yet.";
    } else {
      existingFriends.forEach(f => {
        const friendDiv = document.createElement("div");
        friendDiv.classList.add("friend-item");

        const avatar = document.createElement("div");
        avatar.classList.add("friend-avatar");

        const nameDiv = document.createElement("div");
        nameDiv.classList.add("friend-name");
        nameDiv.textContent = f;

        const viewBtn = document.createElement("button");
        viewBtn.classList.add("friend-view-btn");
        viewBtn.textContent = "View";
        viewBtn.onclick = () => {
          const friendname = f;
          console.log("Viewing f:", friendname);
          openFriendModal(friendname);
        };

        friendDiv.appendChild(avatar);
        friendDiv.appendChild(nameDiv);
        friendDiv.appendChild(viewBtn);

        friendsList.appendChild(friendDiv);
      });

    }

    // Add click event to dropdown to add a friend
    fBtn.onclick = () => {
      if (!dropdown.value) return;
      const selectedUser = dropdown.value;
      const friendDiv = document.createElement("div");
      friendDiv.classList.add("friend-item");

      const avatar = document.createElement("div");
      avatar.classList.add("friend-avatar");

      const nameDiv = document.createElement("div");
      nameDiv.classList.add("friend-name");
      nameDiv.textContent = selectedUser;

      const viewBtn = document.createElement("button");
      viewBtn.classList.add("friend-view-btn");
      viewBtn.textContent = "View";
       viewBtn.onclick = () => {
          console.log("Viewing User:", selectedUser);
          openFriendModal(selectedUser);
        };

      friendDiv.appendChild(avatar);
      friendDiv.appendChild(nameDiv);
      friendDiv.appendChild(viewBtn);

      friendsList.appendChild(friendDiv);


      // Remove from dropdown so it can't be added again
      const optionToRemove = Array.from(dropdown.options).find(opt => opt.value === selectedUser);
      if (optionToRemove) optionToRemove.remove();

      // Reset dropdown selection
      dropdown.value = "";

      // Optional: POST to backend to save immediately
      fetch("/dash_api/addFriend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ currentUser, friendUser: selectedUser })
      }).then(res => res.json()).then(res => {
        console.log("Friend added:", res);
      }).catch(err => console.error("Failed to add friend:", err));
    };

  } catch (err) {
    console.error("Failed to load friends:", err);
  }
}


async function addFriend(selectedUser) {
  if (!selectedUser) return;

  const list = document.getElementById("friends-list");
  const dropdown = document.getElementById("friendDropdown");

  // Remove placeholder if present
  if (list.textContent.trim() === "show friends" || list.textContent.trim() === "No Friends yet.") {
    list.textContent = "";
  }

  // Create friend bubble
  const friendDiv = document.createElement("div");
  friendDiv.classList.add("friend-item");

  const avatar = document.createElement("div");
  avatar.classList.add("friend-avatar");

  const nameDiv = document.createElement("div");
  nameDiv.classList.add("friend-name");
  nameDiv.textContent = selectedUser;

  const viewBtn = document.createElement("button");
  viewBtn.classList.add("friend-view-btn");
  viewBtn.textContent = "View";
  viewBtn.onclick = () => {
          console.log("Viewing User:", selectedUser);
          openFriendModal(selectedUser);
        };

  friendDiv.appendChild(avatar);
  friendDiv.appendChild(nameDiv);
  friendDiv.appendChild(viewBtn);

  list.appendChild(friendDiv);

  // Remove from dropdown so it can't be added again
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


async function openFriendModal(friendData) {
    const modal = document.getElementById("friendModal");
    const closeBtn = modal.querySelector(".close");
    const nameDiv = modal.querySelector("#friend-name");
    const username = localStorage.getItem("currentUser");

    modal.style.display = "block";

    closeBtn.onclick = () => modal.style.display = "none";
    nameDiv.textContent = friendData;

    modal.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
    await fillFriendActivity(friendData);
    await fillFriendsClub(friendData);
    await likeFeature(username, friendData);

}
async function fillFriendActivity(friendUsername) {
  try {
    const response = await fetch("/activity_api/fillFrAct", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: friendUsername })
    });

    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const data = await response.json();
    const activities = Array.isArray(data.activities) ? data.activities : [];

    populateFriendActivities(activities);

    return activities;

  } catch (err) {
    console.error("Failed to load friend activities:", err);
  }
}

function populateFriendActivities(activities) {
  const feedContainer = document.getElementById("friend-activity-feed");
  feedContainer.innerHTML = ""; // clear previous content

  if (!activities || activities.length === 0) {
    feedContainer.innerHTML = `
      <div class="card feed-card">
        <div class="no-activities">No public activities.</div>
      </div>
    `;
    return;
  }

   // Fill the activity count using the array length
  const FactivityCountDiv = document.querySelector("#Factivity-count");
  FactivityCountDiv.textContent = activities?.length ?? 0;

  activities.forEach(act => {
    let extra = "";

    // handle swim details if present
    if (act.ActivityType.toLowerCase() === "swim" && act.Details) {
      try {
        const details = JSON.parse(act.Details);
        if (details.distance && details.unit) extra = `${details.distance} ${details.unit}`;
      } catch (e) {
        console.warn("Invalid JSON in activity details:", act.Details);
      }
    }

    const dateObj = new Date(act.ActivityDate);
    const formattedDate = !isNaN(dateObj)
      ? dateObj.toLocaleDateString("en-US", { year:"numeric", month:"short", day:"numeric" })
      : "Unknown Date";

    const card = document.createElement("div");
    card.className = "card feed-card";
    card.innerHTML = `
      <div class="feed-title">${act.ActivityType.toUpperCase()}</div>
      <div class="feed-meta">${formattedDate}</div>
      <div class="feed-details">
        Duration: ${act.Duration ?? "N/A"} min • Calories: ${act.CaloriesBurned ?? "N/A"}${extra ? " • " + extra : ""}
      </div>
      ${act.Notes ? `<div class="feed-notes">Notes: ${act.Notes}</div>` : ""}
    `;
    feedContainer.appendChild(card);
  });
}


async function fillFriendsClub(friendUsername){
  try {
    const response = await fetch("/club_api/myclubs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: friendUsername })
    });

    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const data = await response.json();
    const clubs = Array.isArray(data.clubs) ? data.clubs : [];

    console.log("friends clubs:", clubs);

    populateFriendClubs(clubs);

  } catch (err) {
    console.error("Failed to load friend clubs:", err);
  }

}


function populateFriendClubs(clubs) {
    const container = document.getElementById("friendClubsContainer");

    if (!container) return;

    // Clear old content
    container.innerHTML = "";

    if (!clubs || clubs.length === 0) {
      container.innerHTML = `
       <div class="card feed-card">
        <div class="no-clubs">No Clubs.</div>
      </div>
      `;
      return;
    }

    clubs.forEach(club => {
        const card = document.createElement("div");
        card.classList.add("card");

        const name = document.createElement("div");
        name.classList.add("club-name");
        name.textContent = club.name;

        const meta = document.createElement("div");
        meta.classList.add("club-meta");
        meta.textContent = `${club.members.length} Members`;

        card.appendChild(name);
        card.appendChild(meta);
        container.appendChild(card);
    });
}
