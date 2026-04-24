// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {

  // ---------------- FORM REFERENCE ----------------
  const form = document.getElementById("clubs-form");


  // ---------------- LOAD CLUBS ----------------
  async function loadClubs() {
    const allList = document.getElementById("all-clubs-list"); // all clubs container
    const myList = document.getElementById("my-clubs-list");   // user's clubs container

    // If not on clubs page, stop execution
    if (!allList && !myList) return;

    try {
      const username = localStorage.getItem("currentUser");

      // Handle no logged-in user
      if (!username) {
        console.warn("No logged-in user");
        renderClubs("all-clubs-list", [], false);
        renderClubs("my-clubs-list", [], true);
        return;
      }

      // -------- FETCH ALL CLUBS --------
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

      // -------- FETCH USER CLUBS --------
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


  // Expose globally so other scripts can refresh clubs
  window.loadClubs = loadClubs;


  // ---------------- PAGE SHOW HANDLER ----------------
  // Reload clubs when navigating back to this page
  window.addEventListener("pageshow", () => {
    if (window.loadClubs) {
      window.loadClubs();
    }
  });


  // ---------------- CREATE CLUB ----------------
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      // Collect form values
      const name = document.getElementById("club-name").value.trim();
      const description = document.getElementById("club-description").value.trim();
      const sportType = document.getElementById("club-sport-type").value;
      const privacy = document.querySelector('input[name="club_privacy"]:checked')?.value || "public";
      const username = localStorage.getItem("currentUser");

      // Validate required field
      if (!name) {
        alert("Club name required");
        return;
      }

      try {
        // Send create request
        const response = await fetch("/club_api/createclub", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            club_name: name,
            description,
            sport_type: sportType,
            privacy,
            username
          })
        });

        // Handle error
        if (!response.ok) {
          const err = await response.json().catch(() => ({}));
          throw new Error(err.error || `HTTP ${response.status}`);
        }

        // Success flow
        alert("Club created!");
        form.reset();
        window.location.href = "/clubs";

      } catch (err) {
        console.error("Create club error:", err);
        alert("Failed to create club");
      }
    });
  }

  // Initial load
  loadClubs();
});


// ---------------- RENDER CLUB CARDS ----------------
function renderClubs(containerId, clubs, isMember) {

  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "";

  // Empty state
  if (!clubs || clubs.length === 0) {
    container.innerHTML = "<p class='empty'>No clubs found.</p>";
    return;
  }

  const currentUser = localStorage.getItem("currentUser");

  clubs.forEach(club => {

    const card = document.createElement("div");
    card.className = "clubpage-item";

    // Member handling
    const members = club.members !== undefined ? club.members : [];
    const totalMembers = club.total_members !== undefined
      ? club.total_members
      : (members.length + 1);

    const isOwner = isMember && club.creator_username === currentUser;
    const hasPendingRequest = !!club.has_pending_request;


    // ---------------- DETERMINE ACTION ----------------
    let action = "";
    let actionLabel = "";

    console.log("club card", club.name, {
      is_private: club.is_private,
      has_pending_request: club.has_pending_request,
      isOwner,
      isMember
    });

    if (isOwner) {
      action = "delete";
      actionLabel = "Delete";
    } else if (isMember) {
      action = "leave";
      actionLabel = "Leave";
    } else if (club.is_private) {
      if (hasPendingRequest) {
        action = "cancel_request";
        actionLabel = "Cancel Join Request";
      } else {
        action = "request_join";
        actionLabel = "Request to Join";
      }
    } else {
      action = "join";
      actionLabel = "Join";
    }


    // ---------------- BUILD CARD UI ----------------
    card.innerHTML = `
      <h4>${club.name}</h4>
      <p class="clubpage-description-text">${club.description || "No description provided."}</p>
      <p>${totalMembers} members</p>
      <p>${club.is_private ? "Private Club" : "Public Club"}</p>

      <div class="clubpage-card-buttons">
        <button class="secondary-btn view-club-btn" data-club-id="${club.id}">
          View
        </button>
        <button class="secondary-btn" data-club-id="${club.id}" data-action="${action}">
          ${actionLabel}
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

        const clubId = actionBtn.dataset.clubId;
        const action = actionBtn.dataset.action;

        let endpoint = "";

        // Map action to API endpoint
        if (action === "delete") {
          if (!confirm(`Delete "${club.name}"? This cannot be undone.`)) return;
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
            body: JSON.stringify({ username, club_id: clubId })
          });

          if (!resp.ok) {
            alert("Action failed");
            return;
          }

          // Reload clubs after action
          await (window.loadClubs ? window.loadClubs() : Promise.resolve());

        } catch (err) {
          console.error("Club action error:", err);
          alert("An error occurred.");
        }
      });
    }


    // ---------------- VIEW BUTTON ----------------
    const viewBtn = card.querySelector("button.view-club-btn");

    if (viewBtn) {
      viewBtn.addEventListener("click", () => {
        window.location.href = `/club/${encodeURIComponent(club.id)}`;
      });
    }

  });
}