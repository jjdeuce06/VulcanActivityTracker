document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("clubs-form"); 
  if (!form) {
    console.error("clubs-form not found");
    return;
  }

  async function loadClubs() {
    try {
      // Fetch all clubs
      const allResp = await fetch("/club_api/listclubs");
      if (allResp.ok) {
        const data = await allResp.json();
        renderClubs("all-clubs-list", data.clubs || [], false);
      } else {
        console.error("Failed to load all clubs", allResp.status);
      }

      //fsetchs the user's clubs
      const username = localStorage.getItem("currentUser") || null;
      if (username) {
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
      } else {
        //users list is empty if theyre not loggged in
        renderClubs("my-clubs-list", [], true);
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

  clubs.forEach(club => {
    const card = document.createElement("div");
    card.className = "club-item";

    const members = club.members !== undefined ? club.members : [];

    card.innerHTML = `
      <h4>${club.name}</h4>
      <p>${club.description || ""}</p>
      <p>${members.length} members</p>
      <button class="secondary-btn" data-club-id="${club.id}">
        ${isMember ? "Leave" : "Join"}
      </button>
    `;

    container.appendChild(card);

    const btn = card.querySelector("button.secondary-btn");
    if (btn) {
      btn.addEventListener("click", async () => {
        const username = localStorage.getItem("currentUser");
        if (!username) {
          alert("Please log in to continue.");
          return;
        }
        const clubId = btn.dataset.clubId;
        const endpoint = isMember ? "/club_api/leave" : "/club_api/join";
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
            alert((isMember ? "Failed to leave: " : "Failed to join: ") + msg);
            return;
          }

          //refreshs the lists after joining or leaving or creating a club
          try {
            await (window.loadClubs ? window.loadClubs() : Promise.resolve());
          } catch (err) {
            console.error("loadClubs failed after action:", err);
            location.reload();
          }
        } catch (err) {
          console.error((isMember ? "Leave" : "Join") + " club error:", err);
          alert((isMember ? "Failed to leave club." : "Failed to join club."));
        }
      });
    }
  });
}