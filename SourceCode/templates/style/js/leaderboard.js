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
    basketball: ["Rank", "Name", "Total Points", "Total Rebounds", "Total Assists", "Total Duration (minutes)", "Total Activities"],
    equestrian: ["Rank", "Name", "Total Distance (miles)", "Total Duration (minutes)", "Total Activities"],
  };




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

  async function getLeaderboardData() {
    const response = await fetch("/activity_api/publicleaderboard", { method: "GET" });
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const payload = await response.json();

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
    basketball: ["Rank", "Name", "Total Points", "Total Rebounds", "Total Assists", "Total Duration (minutes)", "Total Activities"],
    equestrian: ["Rank", "Name", "Total Distance (miles)", "Total Duration (minutes)", "Total Activities"],
  };


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
      }

      else if (sport === "baseball") 
        {
        bodytr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>
        <td>${score.hits ?? 0}</td>
        <td>${score.runs ?? 0}</td>
        <td>${minutes ?? 0}</td>
        <td>${count ?? 0}</td>
        `;
      }

      else if (sport === "basketball") {
        bodytr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>
        <td>${score.points ?? 0}</td>
        <td>${score.rebounds ?? 0}</td>
        <td>${score.assists ?? 0}</td>
        <td>${minutes ?? 0}</td>
        <td>${count ?? 0}</td>
        `;
      }

      else if (sport === "yoga") 
      {        
        bodytr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>
        <td>${score.intensity ?? 0}</td>
        <td>${minutes ?? 0}</td>
        <td>${count ?? 0}</td>
        `;
      }

      else if (sport === "football") 
      {
        bodytr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>
        <td>${score.touchdowns ?? 0}</td>
        <td>${minutes ?? 0}</td>
        <td>${count ?? 0}</td>
        `;
      }

      else if (sport === "volleyball")
      {
        bodytr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>
        <td>${score.kills ?? 0}</td>
        <td>${minutes ?? 0}</td>
        <td>${count ?? 0}</td>
        `;
      }

      else if (sport === "walking")
      {
        bodytr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>  
        <td>${score.steps ?? 0}</td>
        <td>${minutes ?? 0}</td>
        <td>${count ?? 0}</td>
        `;
      }

      else{
        bodytr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>
        <td>${score ?? 0}</td>
        <td>${minutes ?? 0}</td>
        <td>${count ?? 0}</td>
        `;
      }
      tbody.appendChild(bodytr);

    
    });
  }

  function sortAndRender() 
  {
    const sport = sortSport.value || "all";
    const key = sortBy.value;                  // score | name | totalMinutes | totalActivities
    const dir = sortDirBtn.dataset.dir || "desc";

    // compute the values that are actually displayed for this sport
    const computed = buildComputedRows(data, sport);

    const sorted = [...computed].sort((a, b) => {
      let av = a[key];
      let bv = b[key];

      if (key === "name") {
        const res = String(av ?? "").localeCompare(String(bv ?? ""), undefined, { sensitivity: "base" });
        return dir === "asc" ? res : -res;
      }

      const res = (Number(av) || 0) - (Number(bv) || 0);
      return dir === "asc" ? res : -res;
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
      running: "run",
      cycling: "bike",
      swim: "swimming",
      lifting: "lift",
      yoga: "yoga",
      walking: "walk",
      soccer: "soccer",
      baseball: "baseball",
      football: "football"
    };

    return aliases[v] || v;
  }

  function parseActivities(row) {
      if (!row.activities) return [];
      try {
        const arr = JSON.parse(row.activities);

        return arr.map(a => {
          let details = a.details ?? a.Details ?? {};
          if (typeof details === "string") {
            try { details = JSON.parse(details); } catch { details = {}; }
          }

          return {
            activityType: normalizeSport(a.activityType ?? a.ActivityType ?? a.activity_type),
            duration: Number(a.duration ?? a.Duration ?? 0) || 0,
            details
          };
        });
      } catch (e) {
        console.error("Failed to parse activities for:", row.name, e);
        return [];
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

      console.log("Computing: ", s);

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
          score = yogaStats(filtered);
          break;
        case "lift":
          score = totalSets(filtered);
          console.log("LIFT DEBUG user:", row.name);
          console.log("all activityTypes:", activities.map(a => a.activityType));
          console.log("filtered lift activities:", filtered);
          console.log("first lift details:", filtered[0]?.details);
          break;
        case "soccer":
          const st = soccerStats(filtered);
          score = st.goals;
          extra = {assists: st.assists};
          break;
        case "baseball":
          const bt = baseballStats(filtered);
          score = bt.hits;
          extra = {runs: bt.runs};
          break;
        case "football":
          const ft = footballStats(filtered);
          score = ft.touchdowns;
          break;
        case "tennis":
          //return tennisStats(filtered);
          score = totalDuration(filtered);
          break;
        case "volleyball":
          const vt = volleyballStats(filtered);
          score = vt.kills;
          break;
        case "basketball":
          const bbt = basketballStats(filtered);
          score = bbt.points;
          extra = {rebounds: bbt.rebounds, assists: bbt.assists};
          break;

        default:
          score = totalDuration(filtered);
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

  function filterBySport(activities, sport) {
    const target = normalizeSport(sport);
    if (target === "all") return activities;
    return activities.filter(a => a.activityType === target);
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
    return activities.reduce((sum, a) => sum + (Number(a.details?.distance) || 0), 0);
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

  function yogaStats(activities) {
    const intensity = activities.reduce((acc, a) => {
      acc.intensity += a.details?.intensity || 0;
      return acc;
    }, {intensity: 0});
    return {intensity: intensity.intensity};
}

  function soccerStats(activities) {
    const goals = activities.reduce(
      (acc, a) => {
        acc.goals += a.details?.goals || 0;
        return acc;
      },
      {goals: 0, assists: 0}
    );

    const assists = activities.reduce( 
      (acc, a) => {
        acc.assists += a.details?.assists || 0;
        return acc;
      },
      {goals: 0, assists: 0}
    );
    return {goals: goals.goals, assists: assists.assists};
  }

  function baseballStats(activities) {
    const hits = activities.reduce(
      (acc, a) => {
        acc.hits += a.details?.hits || 0;
        return acc;
      },
      {hits: 0, runs: 0}
    );

    const runs = activities.reduce(
      (acc, a) => {
        acc.runs += a.details?.runs || 0;
        return acc;
      },
      {hits: 0, runs: 0}
    );
    return {hits: hits.hits, runs: runs.runs};
  }

  function footballStats(activities) {
    const touchdowns = activities.reduce(
      (acc, a) => {
        acc.touchdowns += a.details?.touchdowns || 0;
        return acc;
      },
      {touchdowns: 0}
    );
    return {touchdowns: touchdowns.touchdowns};
  }

  function tennisStats(activities) {
  }

  function volleyballStats(activities) {
    const kills = activities.reduce(
      (acc, a)=> {
        acc.kills += a.details?.kills || 0;
        return acc;
      },
      {kills: 0}
    );
    return {kills: kills.kills};
  }

  function basketballStats(activities) {
    const points = activities.reduce(
      (acc, a) => {
        acc.points += a.details?.points || 0;
        return acc;
      }, {points: 0, rebounds: 0, assists: 0}
    );

    const rebounds = activities.reduce(
      (acc, a) => {
        acc.rebounds += a.details?.rebounds || 0;
        return acc;
      }, {points: 0, rebounds: 0, assists: 0}
    );

    const assists = activities.reduce(
      (acc, a) => {
        acc.assists += a.details?.assists || 0;
        return acc;
      }, {points: 0, rebounds: 0, assists: 0}
    );

    return {points: points.points, rebounds: rebounds.rebounds, assists: assists.assists};
  }

  function walkingStats(activities) {
    const steps = activities.reduce(
      (acc, a) => {
        acc.steps += a.details?.steps || 0;
        return acc;
      },
      {steps: 0}
    );
    return {steps: steps.steps};
  }

  function computeScore(row, sport) {
    const activities = parseActivities(row);
    const filtered = filterBySport(activities, sport);

    switch (sport) {
      case "running":
      case "cycling":
      case "swimming":
      case "equestrian":
        return totalDistance(filtered);
      case "walking":
        return totalSteps(filtered);
      case "yoga":
        return yogaStats(filtered);
      case "lifting":
        return totalSets(filtered);
      case "soccer":
        return soccerStats(filtered);
      case "baseball":
        return baseballStats(filtered);
      case "football":
        return footballStats(filtered);
      case "tennis":
        //return tennisStats(filtered);
        return totalDuration(filtered);
      case "volleyball":
        return volleyballStats(filtered);
      case "basketball":
        return basketballStats(filtered);

      default:
        return totalDuration(filtered);
    }
  }

  // ✅ Initial load: fetch -> store -> sort -> render
  (async function init() {
    try {
      sortTableBySport(sortSport.value || "all");

      data = await getLeaderboardData(sortSport.value || "all");

      data = await getLeaderboardData();

      data = await getLeaderboardData(sortSport.value || "all");
      sortAndRender();
    } catch (err) {
      console.error("Failed to load leaderboard:", err);
    }
  })();
});