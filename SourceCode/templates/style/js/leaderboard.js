document.addEventListener("DOMContentLoaded", () => {
  const table = document.getElementById("leaderboard");
  if (!table) return;

  const tbody = table.querySelector("tbody");
  const sortBy = document.getElementById("sortBy");
  const sortDirBtn = document.getElementById("sortDir");
  const username = localStorage.getItem("currentUser");


  // Replace this later with a fetch() call to API endpoint
  let data = [
    { name: "Alice", score: 100, totalMinutes: 250, totalActivities: 15 },
    { name: "Bob", score: 80, totalMinutes: 180, totalActivities: 10 },
    { name: "Charlie", score: 60, totalMinutes: 120, totalActivities: 8 },
    { name: "Diana", score: 120, totalMinutes: 300, totalActivities: 20 },
  ];

  

  async function getActivityData(username) {
    try {
      const response = await fetch("/actiivity_api/fillacitivity", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username })
      });

      if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const test_data = await response.json();

    //ensure array
    const activities = Array.isArray(test_data)
      ? test_data
      : test_data.activities;

      return activities;
    }
    catch (err) 
    {
      console.error("Failed to load activities:", err);
    }
    

  }
  async function render(rows) {
    tbody.innerHTML = "";

    rows.forEach((row, idx) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name}</td>
        <td>${row.score}</td>
        <td>${row.totalMinutes}</td>
        <td>${row.totalActivities}</td>
      `;
      tbody.appendChild(tr);
    });
  
    activities = await getActivityData(username);
    activities.forEach(activity => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${username}</td>
        <td>${activity.name}</td>
        <td>${activity.minutes}</td>
        <td>${activity.date}</td>
      `;
      tbody.appendChild(tr);
    });
  }
  

  function sortAndRender() {
    const key = sortBy.value;            // "score" or "name"
    const dir = sortDirBtn.dataset.dir;  // "asc" or "desc"

    const sorted = [...data].sort((a, b) => {
      let av = a[key];
      let bv = b[key];

      if (key === "name") {
        av = String(av).toLowerCase();
        bv = String(bv).toLowerCase();
        const res = av.localeCompare(bv);
        return dir === "asc" ? res : -res;
      }

      // numeric
      const res = (Number(av) || 0) - (Number(bv) || 0);
      return dir === "asc" ? res : -res;
    });

    render(sorted);
  }

  // Sort dropdown changes
  sortBy.addEventListener("change", sortAndRender);

  // Asc/Desc toggle
  sortDirBtn.addEventListener("click", () => {
    const next = sortDirBtn.dataset.dir === "desc" ? "asc" : "desc";
    sortDirBtn.dataset.dir = next;
    sortDirBtn.textContent = next === "desc" ? "Desc" : "Asc";
    sortAndRender();
  });

  // Initial render
  sortAndRender();
});
