document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("clubs-form"); 
  if (!form) {
    console.error("clubs-form not found");
    return;
  }

  async function loadClubs() {
  try {
    const username = localStorage.getItem("currentUser");

    if (!username) {
      console.warn("No logged-in user");
      renderClubs("all-clubs-list", [], false);
      renderClubs("my-clubs-list", [], true);
      return;
    }

    // Fetch clubs user is NOT part of
    const allResp = await fetch("/club_api/listclubs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });

    if (allResp.ok) {
      const data = await allResp.json();
      renderClubs("all-clubs-list", data.clubs || [], false);
    } else {
      console.error("Failed to load clubs", allResp.status);
    }

    // Fetch user's clubs
    const myResp = await fetch("/club_api/myclubs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });

    if (myResp.ok) {
      const data = await myResp.json();
      renderClubs("my-clubs-list", data.clubs || [], true);
    } else {
      console.error("Failed to load my clubs", myResp.status);
    }

  } catch (err) {
    console.error("Error loading clubs:", err);
  }
}

  window.loadClubs = loadClubs;//

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("club-name").value.trim();
    const description = document.getElementById("club-description").value.trim();
    const username = localStorage.getItem("currentUser");

    if (!name) {
      alert("Club name required");
      return;
    }

    try {
      const response = await fetch("/club_api/createclub", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          club_name: name,
          description,
          username
        })
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || `HTTP ${response.status}`);
      }

      alert("Club created!");
      form.reset();
      await loadClubs();
    } catch (err) {
      console.error("Create club error:", err);
      alert("Failed to create club");
    }
  });

  loadClubs();
});

function renderClubs(containerId, clubs, isMember) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = "";

  if (!clubs || clubs.length === 0) {
    container.innerHTML = "<p class='empty'>No clubs found.</p>";
    return;
  }

  const currentUser = localStorage.getItem("currentUser");

  clubs.forEach(club => {
    const card = document.createElement("div");
    card.className = "club-item";

    const members = club.members !== undefined ? club.members : [];
    const isOwner = isMember && club.creator_username === currentUser;

    card.innerHTML = `
      <h4>${club.name}</h4>
      <p>${club.description || ""}</p>
      <p>${members.length} members</p>
      <div style="display: flex; gap: 8px;">
      <button class="secondary-btn view-club-btn" data-club-id="${club.id}">
        View
      </button>
      <button class="secondary-btn" data-club-id="${club.id}" data-action="${isOwner ? 'delete' : (isMember ? 'leave' : 'join')}">
        ${isOwner ? "Delete" : (isMember ? "Leave" : "Join")}
      </button>
      </div>
    `;

    container.appendChild(card);

   

    const actionBtn = card.querySelectorAll("button.secondary-btn")[1];  // Get the second button
if (actionBtn) {
  actionBtn.addEventListener("click", async () => {
    const username = localStorage.getItem("currentUser");
    if (!username) {
      alert("Please log in to continue.");
      return;
    }
    
    const clubId = actionBtn.dataset.clubId;
    const action = actionBtn.dataset.action;
    let endpoint = "";

    if (action === "delete") {
      if (!confirm(`Delete "${club.name}"? This cannot be undone.`)) return;
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
        body: JSON.stringify({ username, club_id: clubId })
      });

      const payload = await resp.json().catch(() => null);
      console.log(endpoint, resp.status, payload);

      if (!resp.ok) {
        const msg = payload && payload.error ? payload.error : `HTTP ${resp.status}`;
        alert("Action failed: " + msg);
        return;
      }

      await (window.loadClubs ? window.loadClubs() : Promise.resolve());
    } catch (err) {
      console.error("Club action error:", err);
      alert("An error occurred.");
    }
  });
}

    const viewBtn = card.querySelector("button.view-club-btn");
    if (viewBtn) {
      viewBtn.addEventListener("click", () => {
        window.location.href = `/club/${club.id}`;
      });
    }
  });
}