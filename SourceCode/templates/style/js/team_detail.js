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

  async function loadTeamLeaderboard() {
  const table = document.getElementById("teamLeaderboard");
  if (!table) return;

  const tbody = table.querySelector("tbody");
  const thead = table.querySelector("thead") || table.createTHead();
  let headRow = thead.querySelector("tr");
  if (!headRow) headRow = thead.insertRow();

  const sortBy = document.getElementById("teamSortBy");
  const sortSport = document.getElementById("teamFilterSport");
  const sortDirBtn = document.getElementById("teamSortDir");

  let data = [];

  sortBy.value = "score";
  sortSport.value = "all";
  sortDirBtn.dataset.dir = "desc";
  sortDirBtn.textContent = "Desc";

  async function getLeaderboardData(leaderboardFilter) {
    const response = await fetch(
      `/team_api/leaderboard/${teamId}?sport_type=${leaderboardFilter}`,
      {
        method: "GET",
        credentials: "include"
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const payload = await response.json();
    return payload.leaderboard || [];
  }

  function normalizeSport(s) {
    if (!s) return "";
    const v = String(s).toLowerCase().trim();

    const aliases = {
      running: "run",
      cycling: "bike",
      biking: "bike",
      bike: "bike",
      swim: "swim",
      swimming: "swim",
      lifting: "lift",
      lift: "lift",
      walking: "walk",
      walk: "walk",
      yoga: "yoga",
      soccer: "soccer",
      baseball: "baseball",
      football: "football",
      tennis: "tennis",
      volleyball: "volleyball",
      basketball: "basketball",
      equestrian: "equestrian",
      hockey: "hockey"
    };

    return aliases[v] || v;
  }

  function sortTableBySport(sport) {
    const headersBySport = {
      all: ["Rank", "Name", "Score", "Total Duration (minutes)", "Total Activities"],
      run: ["Rank", "Name", "Miles Run", "Total Duration (minutes)", "Total Activities"],
      bike: ["Rank", "Name", "Miles Cycled", "Total Duration (minutes)", "Total Activities"],
      swim: ["Rank", "Name", "Miles Swam", "Total Duration (minutes)", "Total Activities"],
      lift: ["Rank", "Name", "Total Sets", "Total Duration (minutes)", "Total Activities"],
      yoga: ["Rank", "Name", "Total Intensity", "Total Duration (minutes)", "Total Activities"],
      walk: ["Rank", "Name", "Total Steps", "Total Duration (minutes)", "Total Activities"],
      soccer: ["Rank", "Name", "Total Goals", "Total Assists", "Total Duration (minutes)", "Total Activities"],
      baseball: ["Rank", "Name", "Total Hits", "Total Runs", "Total Duration (minutes)", "Total Activities"],
      football: ["Rank", "Name", "Total Touchdowns", "Total Duration (minutes)", "Total Activities"],
      tennis: ["Rank", "Name", "Total Score", "Total Duration (minutes)", "Total Activities"],
      volleyball: ["Rank", "Name", "Total Kills", "Total Duration (minutes)", "Total Activities"],
      basketball: ["Rank", "Name", "Total Points", "Total Rebounds", "Total Assists", "Total Duration (minutes)", "Total Activities"],
      equestrian: ["Rank", "Name", "Total Distance (miles)", "Total Duration (minutes)", "Total Activities"],
      hockey: ["Rank", "Name", "Total Goals", "Total Assists", "Total Duration (minutes)", "Total Activities"]
    };

    const normalizedSport = normalizeSport(sport);
    const headers = headersBySport[normalizedSport] || headersBySport.all;

    headRow.innerHTML = "";
    headers.forEach(text => {
      const th = document.createElement("th");
      th.textContent = text;
      headRow.appendChild(th);
    });
  }

  function parseActivities(row) {
    if (!row.activities) return [];

    try {
      const arr = JSON.parse(row.activities);

      return arr.map(a => {
        let details = a.details ?? a.Details ?? {};
        if (typeof details === "string") {
          try {
            details = JSON.parse(details);
          } catch {
            details = {};
          }
        }

        return {
          activityType: normalizeSport(
            a.activityType ?? a.ActivityType ?? a.activity_type
          ),
          duration: Number(a.duration ?? a.Duration ?? 0) || 0,
          details
        };
      });
    } catch (e) {
      console.error("Failed to parse activities for:", row.name, e);
      return [];
    }
  }

  function filterBySport(activities, sport) {
    const target = normalizeSport(sport);
    if (target === "all") return activities;
    return activities.filter(a => a.activityType === target);
  }

  function totalDuration(activities) {
    return activities.reduce((sum, a) => sum + (a.duration || 0), 0);
  }

  function totalDistance(activities) {
    return activities.reduce((sum, a) => sum + (Number(a.details?.distance) || 0), 0);
  }

  function totalSteps(activities) {
    return activities.reduce((sum, a) => sum + (Number(a.details?.steps) || 0), 0);
  }

  function totalSets(activities) {
    return activities.reduce((sum, a) => sum + (Number(a.details?.sets) || 0), 0);
  }

  function yogaStats(activities) {
    return {
      intensity: activities.reduce((acc, a) => acc + (Number(a.details?.intensity) || 0), 0)
    };
  }

  function soccerStats(activities) {
    return activities.reduce((acc, a) => {
      acc.goals += Number(a.details?.goals) || 0;
      acc.assists += Number(a.details?.assists) || 0;
      return acc;
    }, { goals: 0, assists: 0 });
  }

  function baseballStats(activities) {
    return activities.reduce((acc, a) => {
      acc.hits += Number(a.details?.hits) || 0;
      acc.runs += Number(a.details?.runs) || 0;
      return acc;
    }, { hits: 0, runs: 0 });
  }

  function footballStats(activities) {
    return activities.reduce((acc, a) => {
      acc.touchdowns += Number(a.details?.touchdowns) || 0;
      return acc;
    }, { touchdowns: 0 });
  }

  function volleyballStats(activities) {
    return activities.reduce((acc, a) => {
      acc.kills += Number(a.details?.kills) || 0;
      return acc;
    }, { kills: 0 });
  }

  function basketballStats(activities) {
    return activities.reduce((acc, a) => {
      acc.points += Number(a.details?.points) || 0;
      acc.rebounds += Number(a.details?.rebounds) || 0;
      acc.assists += Number(a.details?.assists) || 0;
      return acc;
    }, { points: 0, rebounds: 0, assists: 0 });
  }

  function hockeyStats(activities) {
    return activities.reduce((acc, a) => {
      acc.goals += Number(a.details?.goals) || 0;
      acc.assists += (Number(a.details?.primaryAssists) || 0) + (Number(a.details?.secondaryAssists) || 0);
      return acc;
    }, { goals: 0, assists: 0 });
  }

  function computeScore(row, sport) {
    const activities = parseActivities(row);
    const filtered = filterBySport(activities, sport);

    switch (normalizeSport(sport)) {
      case "run":
      case "bike":
      case "swim":
      case "equestrian":
        return totalDistance(filtered);
      case "walk":
        return totalSteps(filtered);
      case "yoga":
        return yogaStats(filtered).intensity;
      case "lift":
        return totalSets(filtered);
      case "soccer":
        return soccerStats(filtered);
      case "baseball":
        return baseballStats(filtered);
      case "football":
        return footballStats(filtered);
      case "tennis":
        return totalDuration(filtered);
      case "volleyball":
        return volleyballStats(filtered);
      case "basketball":
        return basketballStats(filtered);
      case "hockey":
        return hockeyStats(filtered);
      default:
        return totalDuration(filtered);
    }
  }

  function buildComputedRows(rawRows, sport) {
    const s = normalizeSport(sport);

    return rawRows.map(row => {
      const activities = parseActivities(row);
      const filtered = filterBySport(activities, s);

      const totalMinutes = totalDuration(filtered);
      const totalActivities = filtered.length;

      let score = 0;
      let extra = {};

      switch (s) {
        case "run":
        case "bike":
        case "swim":
        case "equestrian":
          score = totalDistance(filtered);
          break;
        case "walk":
          score = totalSteps(filtered);
          break;
        case "yoga":
          score = yogaStats(filtered).intensity;
          break;
        case "lift":
          score = totalSets(filtered);
          break;
        case "soccer": {
          const st = soccerStats(filtered);
          score = st.goals;
          extra = { assists: st.assists };
          break;
        }
        case "baseball": {
          const st = baseballStats(filtered);
          score = st.hits;
          extra = { runs: st.runs };
          break;
        }
        case "football": {
          const st = footballStats(filtered);
          score = st.touchdowns;
          break;
        }
        case "volleyball": {
          const st = volleyballStats(filtered);
          score = st.kills;
          break;
        }
        case "basketball": {
          const st = basketballStats(filtered);
          score = st.points;
          extra = { rebounds: st.rebounds, assists: st.assists };
          break;
        }
        case "hockey": {
          const st = hockeyStats(filtered);
          score = st.goals;
          extra = { assists: st.assists };
          break;
        }
        default:
          score = totalMinutes;
      }

      return {
        ...row,
        score,
        ...extra,
        totalMinutes,
        totalActivities
      };
    });
  }

  function render(rows) {
    tbody.innerHTML = "";
    const sport = normalizeSport(sortSport.value);

    rows.forEach((row, idx) => {
      const activities = parseActivities(row);
      const filtered = filterBySport(activities, sport);

      const score = computeScore(row, sport);
      const minutes = totalDuration(filtered);
      const count = filtered.length;
      const bodytr = document.createElement("tr");

      if (sport === "soccer") {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${score.goals ?? 0}</td>
          <td>${score.assists ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      } else if (sport === "baseball") {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${score.hits ?? 0}</td>
          <td>${score.runs ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      } else if (sport === "basketball") {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${score.points ?? 0}</td>
          <td>${score.rebounds ?? 0}</td>
          <td>${score.assists ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      } else if (sport === "yoga") {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${score.intensity ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      } else if (sport === "football") {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${score.touchdowns ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      } else if (sport === "volleyball") {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${score.kills ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      } else if (sport === "walk") {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${score ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      } else if (sport === "hockey") {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${score.goals ?? 0}</td>
          <td>${score.assists ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      } else {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${typeof score === "object" ? 0 : score ?? 0}</td>
          <td>${minutes ?? 0}</td>
          <td>${count ?? 0}</td>
        `;
      }

      tbody.appendChild(bodytr);
    });
  }

  function sortAndRender() {
    const sport = sortSport.value || "all";
    const key = sortBy.value;
    const dir = sortDirBtn.dataset.dir || "desc";

    const computed = buildComputedRows(data, sport);

    const tieBreakersByKey = {
      totalMinutes: ["score", "totalActivities", "name"],
      score: ["totalMinutes", "totalActivities", "name"],
      totalActivities: ["score", "totalMinutes", "name"],
      name: ["score", "totalMinutes", "totalActivities"]
    };

    const tieBreakers = tieBreakersByKey[key] || ["score", "totalMinutes", "totalActivities", "name"];

    function cmp(a, b, k, direction = dir) {
      const av = a[k];
      const bv = b[k];

      if (k === "name") {
        const res = String(av ?? "").localeCompare(String(bv ?? ""), undefined, {
          sensitivity: "base"
        });
        return direction === "asc" ? res : -res;
      }

      const res = (Number(av) || 0) - (Number(bv) || 0);
      return direction === "asc" ? res : -res;
    }

    const sorted = [...computed].sort((a, b) => {
      let res = cmp(a, b, key, dir);
      if (res !== 0) return res;

      for (const t of tieBreakers) {
        res = cmp(a, b, t, t === "name" ? "asc" : "desc");
        if (res !== 0) return res;
      }

      return 0;
    });

    render(sorted);
  }

  sortBy.addEventListener("change", sortAndRender);

  sortDirBtn.addEventListener("click", () => {
    const current = sortDirBtn.dataset.dir || "desc";
    const next = current === "desc" ? "asc" : "desc";

    sortDirBtn.dataset.dir = next;
    sortDirBtn.textContent = next === "desc" ? "Desc" : "Asc";

    sortAndRender();
  });

  sortSport.addEventListener("change", async () => {
    try {
      const sport = sortSport.value || "all";
      sortTableBySport(sport);
      data = await getLeaderboardData(sport);
      sortAndRender();
    } catch (e) {
      console.error(e);
    }
  });

  try {
    const sport = sortSport.value || "all";
    sortTableBySport(sport);
    data = await getLeaderboardData(sport);
    sortAndRender();
  } catch (err) {
    console.error("Failed to load team leaderboard:", err);
  }
}

  await loadTeam();
  await loadAnnouncements();
  await loadSchedule();
  await loadTeamLeaderboard();


  
});