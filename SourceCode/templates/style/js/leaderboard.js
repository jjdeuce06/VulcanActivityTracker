document.addEventListener("DOMContentLoaded", () => {
  const table = document.getElementById("leaderboard");
  if (!table) return;

  const tbody = table.querySelector("tbody");
  const thead = table.querySelector("thead") || table.createTHead();
  let headRow = thead.querySelector("tr");
  if (!headRow) headRow = thead.insertRow();
  const sortBy = document.getElementById("sortBy");
  const sortSport = document.getElementById("filterSport");
  const sortDirBtn = document.getElementById("sortDir");

  // Defaults
  sortBy.value = "score";
  sortSport.value = "all";
  sortDirBtn.dataset.dir = "desc";
  sortDirBtn.textContent = "Desc";

  leaderboard_filter = sortSport.value || "all";

  // This holds the fetched leaderboard rows
  let data = [];

  async function getLeaderboardData(leaderboard_filter) {
    const response = await fetch(`/activity_api/publicleaderboard?sport_type=${leaderboard_filter}`, { method: "GET" });
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const payload = await response.json();
    console.log("Fetched leaderboard:", payload);

    return payload.leaderboard || [];
  }

  function sortTableBySport(sport){
    const headersBySport = {
    all: ["Rank", "Name", "Score", "Total Duration (minutes)", "Total Activities"],
    running: ["Rank", "Name", "Miles Run", "Total Duration (minutes)", "Total Activities"],
    cycling: ["Rank", "Name", "Miles Cycled", "Total Duration (minutes)", "Total Activities"],
    swimming: ["Rank", "Name", "Miles Swam", "Total Duration (minutes)", "Total Activities"],
    lifting: ["Rank", "Name", "Total Sets", "Total Duration (minutes)", "Total Activities"],
    yoga: ["Rank", "Name", "Total Intensity", "Total Duration (minutes)", "Total Activities"],
    walking: ["Rank", "Name", "Total Steps", "Total Duration (minutes)", "Total Activities"],
    soccer: ["Rank", "Name", "Total Goals", "Total Assists", "Total Duration (minutes)", "Total Activities"],
    baseball: ["Rank", "Name", "Total Hits", "Total Runs", "Total Duration (minutes)", "Total Activities"],
    football: ["Rank", "Name", "Total Touchdowns", "Total Duration (minutes)", "Total Activities"],
    tennis: ["Rank", "Name", "Total Score", "Total Duration (minutes)", "Total Activities"],
    volleyball: ["Rank", "Name", "Total Kills", "Total Duration (minutes)", "Total Activities"],
    basketball: ["Rank", "Name", "Total Points", "Total Rebounds", "Total Duration (minutes)", "Total Activities"],
    equestrian: ["Rank", "Name", "Total Distance (miles)", "Total Duration (minutes)", "Total Activities"],
  };
 

  console.log("Setting headers for sport:", sport);

  const headers = headersBySport[sport] || headersBySport.all;

  // Clear existing header cells
  headRow.innerHTML = "";

  // Build header cells
  headers.forEach(text => {
    const th = document.createElement("th");
    th.textContent = text;
    headRow.appendChild(th);
  });
  }

  function render(rows) {
    tbody.innerHTML = "";
    const sport = sortSport.value;

    rows.forEach((row, idx) => {
      const activities = parseActivities(row);
      console.log("Parsed activities for", row.name, activities);
      const filtered = filterBySport(activities, sport);

      const score = computeScore(filtered, sport);
      const minutes = totalDuration(filtered);
      const count = filtered.length;
      const bodytr = document.createElement("tr");

      bodytr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>
        <td>${score ?? 0}</td>
        <td>${minutes ?? 0}</td>
        <td>${count ?? 0}</td>
        `;
      tbody.appendChild(bodytr);
      // if (sortSport.value == "running")
      // {
      //   if (row.allDetails && row.allDetails.includes("[run]"))
      //   {
      //       bodytr.innerHTML = `
      //         <td>${idx + 1}</td>
      //         <td>${row.allDetails.distance ?? ""}</td>
      //         <td>${row.score ?? 0}</td>
      //         <td>${row.totalMinutes ?? 0}</td>
      //         <td>${row.totalActivities ?? 0}</td>
      //       `;
      //   tbody.appendChild(bodytr);
      //   }
      
      // }

    
    });
  }

  function sortAndRender() {
    const key = sortBy.value;

    const dir = sortDirBtn.dataset.dir || "desc";
    sortDirBtn.dataset.dir = dir;

    const sorted = [...data].sort((a, b) => {
      let av = a[key];
      let bv = b[key];

      // name sort
      if (key === "name") {
        const res = String(av ?? "").localeCompare(String(bv ?? ""), undefined, {
          sensitivity: "base",
        });
        return dir === "asc" ? res : -res;
      }

      // numeric sort
      const numA = Number(av) || 0;
      const numB = Number(bv) || 0;
      return dir === "asc" ? numA - numB : numB - numA;
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
    sortTableBySport(sortSport.value);
    data = await getLeaderboardData(sortSport.value || "all");
    sortAndRender();
  } catch (e) {
    console.error(e);
  }
  });

    function normalizeSport(s) {
    if (!s) return "";
    const v = String(s).toLowerCase().trim();

    // Map DB values -> dropdown values
    const aliases = {
      run: "running",
      bike: "cycling",
      cycle: "cycling",
      swim: "swimming",
      lift: "lifting",
    };

    return aliases[v] || v;
  }

  function parseActivities(row) {
    if (!row.activities) return [];
    try {
      const arr = JSON.parse(row.activities);

      // Ensure each activity has parsed details + normalized type
      return arr.map(act => {
        let details = act.details;

        // If details is a JSON string (common with FOR JSON PATH), parse it
        if (typeof details === "string") {
          try { details = JSON.parse(details); } catch { details = {}; }
        }

        return {
          ...act,
          activityType: normalizeSport(act.activityType || act.ActivityType || act.activity_type),
          details: details || {}
        };
      });
    } catch (e) {
      console.error("Failed to parse activities for:", row.name, e);
      return [];
    }
  }

  function filterBySport(activities, sport) {
    const s = normalizeSport(sport);
    if (s === "all") return activities;
    return activities.filter(act => act.activityType === s);
  }

  //activity computation of totals
  function totalDuration(activities) {
    return activities.reduce(
      (sum, a) => sum + (a.duration || 0),
      0
    );
  }

  function totalCount(activities) {
    return activities.length;
  }

  function totalDistance(activities) {
    return activities.reduce(
      (sum, a) => sum + (a.details?.distance || 0),
      0
    );
  }

  function totalSteps(activities) {
    return activities.reduce(
      (sum, a) => sum + (a.details?.steps || 0),
      0
    );
  }

  function totalSets(activities) {
    return activities.reduce((sum, a) => sum + (a.details?.sets || 0), 0);
  }

  function soccerStats(activities) {
    return activities.reduce(
      (acc, a) => {
        acc.goals += a.details?.goals || 0;
        acc.assists += a.details?.assists || 0;
        return acc;
      },
      {goals: 0, assists: 0}
    );
  }

  function computeScore(row, sport) {
    const activities = parseActivities(row);
    const filtered = filterBySport(activities, sport);

    switch (sport) {
      case "running":
      case "cycling":
      case "swimming":
      case "equestrian":
        console.log("Computing distance score for", row.name, filtered);
        console.log("Distance", totalDistance(filtered));
        return totalDistance(filtered);
      case "walking":
        return totalSteps(filtered);
      case "lifting":
        return totalSets(filtered);
      case "soccer":
        return soccerStats(filtered).goals;

      default:
        return totalDuration(filtered);
    }
  }

  // ✅ Initial load: fetch -> store -> sort -> render
  (async function init() {
    try {
      sortTableBySport(sortSport.value || "all");
      data = await getLeaderboardData(sortSport.value || "all");
      sortAndRender();
    } catch (err) {
      console.error("Failed to load leaderboard:", err);
    }
  })();
});
