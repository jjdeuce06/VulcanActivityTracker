document.addEventListener("DOMContentLoaded", () => {

  // Fake club data (TEMP)
  const myClubs = [
    {
      id: 1,
      name: "Running Club",
      description: "Weekly campus runs",
      members: 8
    },
    {
      id: 2,
      name: "Weightlifting Club",
      description: "Strength training together",
      members: 12
    }
  ];

  const allClubs = [
    ...myClubs,
    {
      id: 3,
      name: "Yoga Club",
      description: "Relax, stretch, recover",
      members: 5
    },
    {
      id: 4,
      name: "Cycling Club",
      description: "Road and trail rides",
      members: 10
    }
  ];

  renderClubs("my-clubs-list", myClubs, true);
  renderClubs("all-clubs-list", allClubs, false);
});

function renderClubs(containerId, clubs, isMember) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  clubs.forEach(club => {
    const card = document.createElement("div");
    card.className = "club-item";

    card.innerHTML = `
      <h4>${club.name}</h4>
      <p>${club.description}</p>
      <p>${club.members} members</p>
      <button class="secondary-btn">
        ${isMember ? "View" : "Join"}
      </button>
    `;

    container.appendChild(card);
  });
}