document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("invites-container");

  const [teamInvites, clubRequests] = await Promise.all([
    loadTeamInvites(),
    loadClubRequests()
  ]);

  const allItems = [
    ...teamInvites.map(item => ({ ...item, type: "team_invite" })),
    ...clubRequests.map(item => ({ ...item, type: "club_request" }))
  ];

  if (!allItems.length) {
    container.innerHTML = `<div class="no-invites">No invites yet</div>`;
    return;
  }

  allItems.forEach(item => {
    const div = document.createElement("div");
    div.className = "invite-card";

    if (item.type === "team_invite") {
      div.innerHTML = `
        <div class="invite-title">${item.name}</div>
        <div class="invite-meta">Team Invite</div>
        <div class="invite-meta">Sport: ${item.sport}</div>
        <div class="invite-meta">Coach: ${item.coach_username || "Unknown"}</div>

        <div class="invite-actions">
          <button class="btn-accept" onclick="handleAcceptTeam('${item.id}')">Accept</button>
          <button class="btn-decline" onclick="handleDeclineTeam('${item.id}')">Decline</button>
        </div>
      `;
    } else {
      div.innerHTML = `
        <div class="invite-title">${item.name}</div>
        <div class="invite-meta">Club Join Request</div>
        <div class="invite-meta">Sport: ${item.sport}</div>
        <div class="invite-meta">From: ${item.requesting_username}</div>

        <div class="invite-actions">
          <button class="btn-accept" onclick="handleAcceptClub('${item.club_id}', '${item.requesting_username}')">Accept</button>
          <button class="btn-decline" onclick="handleDeclineClub('${item.club_id}', '${item.requesting_username}')">Decline</button>
        </div>
      `;
    }

    container.appendChild(div);
  });
});

async function loadTeamInvites() {
  const response = await fetch("/team_api/invites", {
    method: "GET",
    credentials: "include"
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) return [];
  return data.invites || [];
}

async function loadClubRequests() {
  const username = localStorage.getItem("currentUser");
  if (!username) return [];

  const response = await fetch("/club_api/clubrequests", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) return [];
  return data.requests || [];
}

async function handleAcceptTeam(teamId) {
  const res = await fetch("/team_api/acceptinvite", {
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

async function handleDeclineTeam(teamId) {
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

async function handleAcceptClub(clubId, requestingUsername) {
  const username = localStorage.getItem("currentUser");
  const res = await fetch("/club_api/acceptrequest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username,
      club_id: clubId,
      requesting_username: requestingUsername
    })
  });

  if (res.ok) {
    location.reload();
  } else {
    const data = await res.json();
    alert(data.error);
  }
}

async function handleDeclineClub(clubId, requestingUsername) {
  const username = localStorage.getItem("currentUser");
  const res = await fetch("/club_api/declinerequest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username,
      club_id: clubId,
      requesting_username: requestingUsername
    })
  });

  if (res.ok) {
    location.reload();
  } else {
    const data = await res.json();
    alert(data.error);
  }
}