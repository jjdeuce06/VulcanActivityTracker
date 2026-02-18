document.addEventListener("DOMContentLoaded", async () => {
  const clubId = window.location.pathname.split("/").pop();
  
  try {
    const resp = await fetch("/club_api/clubdetail", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ club_id: clubId })
    });

    if (!resp.ok) {
      alert("Club not found");
      history.back();
      return;
    }

    const data = await resp.json();
    const club = data.club;
    console.log("Loaded club:", club);
    console.log("data:", data);

    document.getElementById("club-name-heading").textContent = club.name;
    document.getElementById("club-description").textContent = club.description || "No description provided.";
    document.getElementById("member-count").textContent = club.members.length;

    const membersList = document.getElementById("members-list");
    if (club.members.length > 0) 
      {
      console.log("Club members:", club.members);
      club.members.forEach(member => {
        const div = document.createElement("div");
        div.className = "club-item";
        div.textContent = member;
        membersList.appendChild(div);
      });
    } else {
      membersList.innerHTML = "<p class='empty'>No members yet</p>";
    }
  } catch (err) {
    console.error("Error loading club:", err);
    alert("Error loading club");
  }
});