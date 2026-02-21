document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("createChallengeForm");

    if (form) {
        form.addEventListener("submit", handleCreateChallenge);
    }

    loadChallenges();
});


async function handleCreateChallenge(event) {
    event.preventDefault();

    const username = localStorage.getItem("currentUser");

    if (!username) {
        alert("User not logged in.");
        return;
    }

    const data = {
        username: username,
        challengeName: document.getElementById("challengeName").value.trim(),
        description: document.getElementById("description").value.trim(),
        activityType: document.getElementById("activityType").value,
        metricType: document.getElementById("metricType").value,
        startDate: document.getElementById("startDate").value,
        endDate: document.getElementById("endDate").value
    };

    try {
        const response = await fetch("/challenges_api/createchallenge", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Challenge created successfully!");
            document.getElementById("createChallengeForm").reset();
        } else {
            alert(result.error || "Failed to create challenge.");
        }

    } catch (error) {
        console.error("Create challenge error:", error);
        alert("Server error while creating challenge.");
    }
}

async function loadChallenges() {
    try {
        const response = await fetch("/challenges_api/list");

        const challenges = await response.json();

        const list = document.getElementById("challengeList");
        list.innerHTML = "";

        if (!challenges.length) {
            list.innerHTML = "<p style='text-align:center;'>No active challenges yet.</p>";
            return;
        }

        challenges.forEach(challenge => {
            const item = document.createElement("div");
            item.className = "challenge-item";

            item.innerHTML = `
                <h4>${challenge.ChallengeName}</h4>
                <p>${challenge.Description || "No description provided."}</p>
                <p>
                    <strong>${challenge.ActivityType}</strong> • 
                    ${challenge.MetricType}
                </p>
                <p>
                    ${challenge.StartDate} → ${challenge.EndDate}
                </p>
                
                <div style="display: flex; gap: 8px;">
                <button class="secondary-btn">
                    View Details
                </button>
                </div>
            `;

            list.appendChild(item);
        });

    } catch (error) {
        console.error("Error loading challenges:", error);
    }
}