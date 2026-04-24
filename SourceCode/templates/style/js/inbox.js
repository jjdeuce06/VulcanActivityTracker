// ---------------- PAGE LOAD: FETCH AND DISPLAY ALL INVITES ----------------
document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("invites-container");

  // Load both sources at the same time
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
// Create a card for each invite/request
  allItems.forEach(item => {
    const div = document.createElement("div");
    div.className = "invite-card";

    // ---------------- TEAM INVITE CARD ----------------
    if (item.type === "team_invite") {
      div.innerHTML = `
        <div class="invite-title">${item.team_name}</div>
        <div class="invite-meta">Team Invite</div>
        <div class="invite-meta">Sport: ${item.sport}</div>
        <div class="invite-meta">Coach: ${item.invited_by || "Unknown"}</div>

        <div class="invite-actions">
          <button class="btn-accept" onclick="handleAcceptTeam('${item.invite_id}')">Accept</button>
          <button class="btn-decline" onclick="handleDeclineTeam('${item.invite_id}')">Decline</button>
        </div>
      `;
       // ---------------- CLUB JOIN REQUEST CARD ----------------
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


// -----------------------------
// TEAM INVITES
// -----------------------------
async function loadTeamInvites() {
  try {
    const response = await fetch("/team_api/invites", {
      method: "GET",
      credentials: "include"
    });

    const data = await response.json();

    console.log("INVITES RESPONSE:", data);

    if (!response.ok) return [];

    // 🔥 IMPORTANT FIX
    return Array.isArray(data.invites) ? data.invites : [];

  } catch (err) {
    console.error("Failed to load invites:", err);
    return [];
  }
}

// ---------------- TEAM INVITE ACTIONS ----------------
async function handleAcceptTeam(inviteId) {
  const res = await fetch("/team_api/acceptinvite", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ invite_id: inviteId }) // ✅ FIXED
  });

  if (res.ok) {
    location.reload();
  } else {
    const data = await res.json();
    alert(data.error);
  }
}

async function handleDeclineTeam(inviteId) {
  const res = await fetch("/team_api/declineinvite", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ invite_id: inviteId }) // ✅ FIXED
  });

  if (res.ok) {
    location.reload();
  } else {
    const data = await res.json();
    alert(data.error);
  }
}


// -----------------------------
// CLUB REQUESTS 
// -----------------------------
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

// ---------------- CLUB REQUEST ACTIONS ----------------
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