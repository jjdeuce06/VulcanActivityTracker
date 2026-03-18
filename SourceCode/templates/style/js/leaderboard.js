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

  let data = [];

  // Defaults
  sortBy.value = "score";
  sortSport.value = "all";
  sortDirBtn.dataset.dir = "desc";
  sortDirBtn.textContent = "Desc";

  async function getLeaderboardData(leaderboardFilter) {
    const response = await fetch(
      `/activity_api/publicleaderboard?sport_type=${leaderboardFilter}`,
      { method: "GET" }
    );

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const payload = await response.json();
    return payload.leaderboard || [];
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
          <td>${score ?? 0}</td>
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

    const tieBreakers = tieBreakersByKey[key] || [
      "score",
      "totalMinutes",
      "totalActivities",
      "name"
    ];

    function cmp(a, b, k, direction = dir) {
      const av = a[k];
      const bv = b[k];

      if (k === "name") {
        const res = String(av ?? "").localeCompare(
          String(bv ?? ""),
          undefined,
          { sensitivity: "base" }
        );
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

        case "yoga": {
          const ys = yogaStats(filtered);
          score = ys.intensity;
          break;
        }

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
          const bt = baseballStats(filtered);
          score = bt.hits;
          extra = { runs: bt.runs };
          break;
        }

        case "football": {
          const ft = footballStats(filtered);
          score = ft.touchdowns;
          break;
        }

        case "tennis":
          score = totalDuration(filtered);
          break;

        case "volleyball": {
          const vt = volleyballStats(filtered);
          score = vt.kills;
          break;
        }

        case "basketball": {
          const bbt = basketballStats(filtered);
          score = bbt.points;
          extra = {
            rebounds: bbt.rebounds,
            assists: bbt.assists
          };
          break;
        }

        case "hockey": {
          const ht = hockeyStats(filtered);
          score = ht.goals;
          extra = { assists: ht.assists };
          break;
        }

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

  function totalDuration(activities) {
    return activities.reduce((sum, a) => sum + (a.duration || 0), 0);
  }

  function totalDistance(activities) {
    return activities.reduce(
      (sum, a) => sum + (Number(a.details?.distance) || 0),
      0
    );
  }

  function totalSteps(activities) {
    return activities.reduce(
      (sum, a) => sum + (Number(a.details?.steps) || 0),
      0
    );
  }

  function totalSets(activities) {
    return activities.reduce(
      (sum, a) => sum + (Number(a.details?.sets) || 0),
      0
    );
  }

  function yogaStats(activities) {
    const intensity = activities.reduce((acc, a) => {
      acc.intensity += Number(a.details?.intensity) || 0;
      return acc;
    }, { intensity: 0 });

    return { intensity: intensity.intensity };
  }

  function soccerStats(activities) {
    const totals = activities.reduce(
      (acc, a) => {
        acc.goals += Number(a.details?.goals) || 0;
        acc.assists += Number(a.details?.assists) || 0;
        return acc;
      },
      { goals: 0, assists: 0 }
    );

    return totals;
  }

  function baseballStats(activities) {
    const totals = activities.reduce(
      (acc, a) => {
        acc.hits += Number(a.details?.hits) || 0;
        acc.runs += Number(a.details?.runs) || 0;
        return acc;
      },
      { hits: 0, runs: 0 }
    );

    return totals;
  }

  function footballStats(activities) {
    const totals = activities.reduce(
      (acc, a) => {
        acc.touchdowns += Number(a.details?.touchdowns) || 0;
        return acc;
      },
      { touchdowns: 0 }
    );

    return totals;
  }

  function volleyballStats(activities) {
    const totals = activities.reduce(
      (acc, a) => {
        acc.kills += Number(a.details?.kills) || 0;
        return acc;
      },
      { kills: 0 }
    );

    return totals;
  }

  function basketballStats(activities) {
    const totals = activities.reduce(
      (acc, a) => {
        acc.points += Number(a.details?.points) || 0;
        acc.rebounds += Number(a.details?.rebounds) || 0;
        acc.assists += Number(a.details?.assists) || 0;
        return acc;
      },
      { points: 0, rebounds: 0, assists: 0 }
    );

    return totals;
  }

  function hockeyStats(activities) {
    const totals = activities.reduce(
      (acc, a) => {
        acc.goals += Number(a.details?.goals) || 0;
        acc.assists +=
          (Number(a.details?.primaryAssists) || 0) +
          (Number(a.details?.secondaryAssists) || 0);
        return acc;
      },
      { goals: 0, assists: 0 }
    );

    return totals;
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

  (async function init() {
    try {
      const sport = sortSport.value || "all";
      sortTableBySport(sport);
      data = await getLeaderboardData(sport);
      sortAndRender();
    } catch (err) {
      console.error("Failed to load leaderboard:", err);
    }
  })();
});