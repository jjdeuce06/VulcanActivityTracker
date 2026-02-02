document.addEventListener("DOMContentLoaded", () => {
  const table = document.getElementById("leaderboard");
  if (!table) return;

  const tbody = table.querySelector("tbody");
  const sortBy = document.getElementById("sortBy");
  const sortDirBtn = document.getElementById("sortDir");

  // Defaults
  sortBy.value = "score";
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

  function render(rows) {
    tbody.innerHTML = "";

    rows.forEach((row, idx) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name ?? ""}</td>
        <td>${row.score ?? 0}</td>
        <td>${row.totalMinutes ?? 0}</td>
        <td>${row.totalActivities ?? 0}</td>
      `;
      tbody.appendChild(tr);
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

  // ✅ Initial load: fetch -> store -> sort -> render
  (async function init() {
    try {
      data = await getLeaderboardData();
      sortAndRender();
    } catch (err) {
      console.error("Failed to load leaderboard:", err);
    }
  })();
});
