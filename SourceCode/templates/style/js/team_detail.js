document.addEventListener("DOMContentLoaded", async () => {
  const pathParts = window.location.pathname.split("/").filter(Boolean);
  const teamId = pathParts[pathParts.length - 1];

  const teamNameHeading = document.getElementById("team-name-heading");
  const teamSport = document.getElementById("team-sport");
  const teamCoach = document.getElementById("team-coach");
  const teamMemberCount = document.getElementById("team-member-count");
  const teamDescription = document.getElementById("team-description");

  const rosterList = document.getElementById("roster-list");
  const announcementList = document.getElementById("announcement-list");
  const scheduleList = document.getElementById("schedule-list");

  const coachTools = document.getElementById("coach-tools-panel");

  const inviteForm = document.getElementById("invite-player-form");
  const inviteUsernameInput = document.getElementById("invite-username");

  const announcementForm = document.getElementById("announcement-form");
  const announcementTitleInput = document.getElementById("announcement-title");
  const announcementBodyInput = document.getElementById("announcement-body");

  const scheduleForm = document.getElementById("schedule-form");
  const scheduleTitleInput = document.getElementById("schedule-title");
  const scheduleTypeInput = document.getElementById("schedule-type");
  const scheduleDateInput = document.getElementById("schedule-date");
  const scheduleLocationInput = document.getElementById("schedule-location");
  const scheduleNotesInput = document.getElementById("schedule-notes");

  let currentTeam = null;

  async function loadTeam() {
    try {
      const resp = await fetch("/team_api/teamdetail", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
          team_id: teamId
        })
      });

      const data = await resp.json();

      if (!resp.ok) {
        alert(data.error || "Unable to load team");
        window.location.href = "/teams";
        return;
      }

      const team = data.team;
      currentTeam = team;

      const roster = Array.isArray(team.roster) ? team.roster : [];

      teamNameHeading.textContent = team.name || "Team";
      teamSport.textContent = team.sport || "Sport";
      teamMemberCount.textContent = `${roster.length} Member${roster.length === 1 ? "" : "s"}`;
      teamDescription.textContent = team.description || "No description provided.";

      const coachMember = roster.find(member =>
        member.role === "coach" || member.role === "admin"
      );

      teamCoach.textContent = `Coach: ${coachMember ? coachMember.username : "Unknown"}`;

      rosterList.innerHTML = "";

      if (roster.length === 0) {
        rosterList.innerHTML = `<p class="empty-state">No roster members found.</p>`;
      } else {
        roster.forEach(member => {
          const div = document.createElement("div");
          div.className = "roster-item";
          div.innerHTML = `
            <strong>${member.username}</strong>
            <div class="item-meta">Role: ${member.role}</div>
          `;
          rosterList.appendChild(div);
        });
      }

      coachTools.style.display = team.is_coach ? "block" : "none";
    } catch (err) {
      console.error("Error loading team:", err);
      alert("Error loading team");
      window.location.href = "/teams";
    }
  }

  async function loadAnnouncements() {
    try {
      const resp = await fetch(`/team_api/announcements/${teamId}`, {
        method: "GET",
        credentials: "include"
      });

      const data = await resp.json();

      if (!resp.ok) {
        announcementList.innerHTML = `<p class="empty-state">${data.error || "Failed to load announcements."}</p>`;
        return;
      }

      const announcements = data.announcements || [];
      announcementList.innerHTML = "";

      if (announcements.length === 0) {
        announcementList.innerHTML = `<div class="announcement-item">No announcements yet.</div>`;
        return;
      }

      announcements.forEach(item => {
        const div = document.createElement("div");
        div.className = "announcement-item";
        div.innerHTML = `
          <div class="item-title">${item.title}</div>
          <div>${item.body}</div>
          <div class="item-meta">Posted by ${item.created_by} on ${formatDate(item.created_at)}</div>
        `;
        announcementList.appendChild(div);
      });
    } catch (err) {
      console.error("Error loading announcements:", err);
      announcementList.innerHTML = `<p class="empty-state">Error loading announcements.</p>`;
    }
  }

  async function loadSchedule() {
    try {
      const resp = await fetch(`/team_api/schedule/${teamId}`, {
        method: "GET",
        credentials: "include"
      });

      const data = await resp.json();

      if (!resp.ok) {
        scheduleList.innerHTML = `<p class="empty-state">${data.error || "Failed to load schedule."}</p>`;
        return;
      }

      const events = data.events || [];
      scheduleList.innerHTML = "";

      if (events.length === 0) {
        scheduleList.innerHTML = `<div class="schedule-item">No events scheduled yet.</div>`;
        return;
      }

      events.forEach(event => {
        const div = document.createElement("div");
        div.className = "schedule-item";
        div.innerHTML = `
          <div class="item-title">${event.title}</div>
          <div><strong>Type:</strong> ${event.event_type}</div>
          <div><strong>Date:</strong> ${formatDate(event.event_date)}</div>
          <div><strong>Location:</strong> ${event.location || "N/A"}</div>
          <div class="item-meta">${event.notes || ""}</div>
        `;
        scheduleList.appendChild(div);
      });
    } catch (err) {
      console.error("Error loading schedule:", err);
      scheduleList.innerHTML = `<p class="empty-state">Error loading schedule.</p>`;
    }
  }

  async function postAnnouncement() {
    const title = announcementTitleInput.value.trim();
    const body = announcementBodyInput.value.trim();

    if (!title || !body) {
      alert("Please fill out both announcement fields.");
      return;
    }

    try {
      const resp = await fetch("/team_api/announcement", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
          team_id: teamId,
          title,
          body
        })
      });

      const data = await resp.json();

      if (!resp.ok) {
        alert(data.error || "Failed to post announcement");
        return;
      }

      announcementForm.reset();
      await loadAnnouncements();
    } catch (err) {
      console.error("Error posting announcement:", err);
      alert("Error posting announcement");
    }
  }

  async function createScheduleEvent() {
    const eventTitle = scheduleTitleInput.value.trim();
    const eventType = scheduleTypeInput.value;
    const eventDate = scheduleDateInput.value;
    const location = scheduleLocationInput.value.trim();
    const notes = scheduleNotesInput.value.trim();

    if (!eventTitle || !eventType || !eventDate) {
      alert("Please fill out title, type, and date.");
      return;
    }

    try {
      const resp = await fetch("/team_api/schedule", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
          team_id: teamId,
          event_title: eventTitle,
          event_type: eventType,
          event_date: eventDate,
          location,
          notes
        })
      });

      const data = await resp.json();

      if (!resp.ok) {
        alert(data.error || "Failed to create event");
        return;
      }

      scheduleForm.reset();
      await loadSchedule();
    } catch (err) {
      console.error("Error creating schedule event:", err);
      alert("Error creating schedule event");
    }
  }

  async function sendInvite(invitedUsername) {
    try {
      const resp = await fetch("/team_api/invite", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
          invited_username: invitedUsername,
          team_id: teamId
        })
      });

      const data = await resp.json();

      if (!resp.ok) {
        alert(data.error || "Failed to send invite");
        return;
      }

      alert(`Invite sent to ${invitedUsername}`);
      inviteForm.reset();
    } catch (err) {
      console.error("Invite error:", err);
      alert("Error sending invite");
    }
  }

  function formatDate(dateString) {
    if (!dateString) return "Unknown date";
    const date = new Date(dateString);
    return date.toLocaleString();
  }

  if (inviteForm) {
    inviteForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const invitedUsername = inviteUsernameInput.value.trim();

      if (!invitedUsername) {
        alert("Enter a username to invite.");
        return;
      }

      await sendInvite(invitedUsername);
    });
  }

  if (announcementForm) {
    announcementForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      await postAnnouncement();
    });
  }

  if (scheduleForm) {
    scheduleForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      await createScheduleEvent();
    });
  }

  await loadTeam();
  await loadAnnouncements();
  await loadSchedule();
});