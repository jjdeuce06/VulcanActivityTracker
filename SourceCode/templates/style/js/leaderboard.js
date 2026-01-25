document.addEventListener("DOMContentLoaded", () => {
  const table = document.getElementById("leaderboard");
  if (!table) return;

  const tbody = table.querySelector("tbody");
  const sortBy = document.getElementById("sortBy");
  const sortDirBtn = document.getElementById("sortDir");

  // Replace this later with a fetch() call to your API endpoint
  let data = [
    { name: "Alice", score: 100 },
    { name: "Bob", score: 80 },
    { name: "Charlie", score: 60 },
    { name: "Diana", score: 120 },
  ];

  function render(rows) {
    tbody.innerHTML = "";

    rows.forEach((row, idx) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${row.name}</td>
        <td>${row.score}</td>
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
