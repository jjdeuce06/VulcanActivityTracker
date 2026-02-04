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

  // This holds the fetched leaderboard rows
  let data = [];

  async function getLeaderboardData() {
    const response = await fetch("/activity_api/publicleaderboard", { method: "GET" });
    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const payload = await response.json();
    console.log("Fetched leaderboard:", payload);

    return payload.leaderboard || [];
  }

  // async function getSpecificSportData(sport){
  //   pass;
  // }
  
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

    rows.forEach((row, idx) => {
      const bodytr = document.createElement("tr");

      if (sortSport.value == "all")
      {
        bodytr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${row.name ?? ""}</td>
          <td>${row.score ?? 0}</td>
          <td>${row.totalMinutes ?? 0}</td>
          <td>${row.totalActivities ?? 0}</td>
        `;
        tbody.appendChild(bodytr);
      }
      if (sortSport.value == "running")
      {
        if (row.allDetails && row.allDetails.includes("[run]"))
        {
            bodytr.innerHTML = `
              <td>${idx + 1}</td>
              <td>${row.allDetails.distance ?? ""}</td>
              <td>${row.score ?? 0}</td>
              <td>${row.totalMinutes ?? 0}</td>
              <td>${row.totalActivities ?? 0}</td>
            `;
        tbody.appendChild(bodytr);
        }
      
      }

    
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

  sortSport.addEventListener("change", () => {
  sortTableBySport(sortSport.value);
  sortAndRender();
});

  // ✅ Initial load: fetch -> store -> sort -> render
  (async function init() {
    try {
      sortTableBySport(sortSport.value || "all");
      data = await getLeaderboardData();
      sortAndRender();
    } catch (err) {
      console.error("Failed to load leaderboard:", err);
    }
  })();
});
