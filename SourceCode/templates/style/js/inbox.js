document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("invites-container");

  const invites = await loadInvites();

  if (!invites.length) {
  container.innerHTML = `<div class="no-invites">No invites yet</div>`;
}

  invites.forEach(invite => {
    const div = document.createElement("div");
    div.className = "invite-card";

    div.innerHTML = `
        <div class="invite-title">${invite.name}</div>
        <div class="invite-meta">Sport: ${invite.sport}</div>
        <div class="invite-meta">Coach: ${invite.coach_username || "Unknown"}</div>

        <div class="invite-actions">
        <button class="btn-accept" onclick="handleAccept('${invite.id}')">Accept</button>
        <button class="btn-decline" onclick="handleDecline('${invite.id}')">Decline</button>
        </div>
    `;

    container.appendChild(div);
    });
});

async function loadInvites() {
  const response = await fetch("/team_api/invites", {
    method: "GET",
    credentials: "include"
  });

  const data = await response.json();

  if (!response.ok) {
    console.error(data.error);
    return [];
  }

  return data.invites || [];
}

async function handleAccept(teamId) {
  const res = await fetch("/team_api/acceptinvite", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ team_id: teamId })
  });

  if (res.ok) {
    location.reload(); // refresh inbox
  } else {
    const data = await res.json();
    alert(data.error);
  }
}

async function handleDecline(teamId) {
  const res = await fetch("/team_api/declineinvite", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ team_id: teamId })
  });

  if (res.ok) {
    location.reload();
  } else {
    const data = await res.json();
    alert(data.error);
  }
}