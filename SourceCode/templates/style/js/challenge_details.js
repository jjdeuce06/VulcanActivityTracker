//challenge_details.js:
document.addEventListener("DOMContentLoaded", async () => {
  const challengeName = decodeURIComponent(
    window.location.pathname.split("/").pop()
  );
  
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
    console.log("Loaded challenge:", challenge);
    console.log("data:", data);

    document.getElementById("challenge-name-heading").textContent = challenge.name;
    document.getElementById("challenge-description").textContent = challenge.description || "No description provided.";
    document.getElementById("participant-count").textContent = challenge.participants.length;

    const participantsList = document.getElementById("participants-list");
    participantsList.innerHTML = "";

    const participantDetails = challenge.participant_details || [];

    if (participantDetails.length > 0) {
      participantDetails.forEach(participant => {
        const div = document.createElement("div");
        div.className = "challengepage-item";
        div.textContent = participant.username;
        participantsList.appendChild(div);
      });
    } else {
      participantsList.innerHTML = "<p class='empty'>No participants yet</p>";
    }
  } catch (err) {
    console.error("Error loading challenge:", err);
    alert("Error loading challenge");
  }
});