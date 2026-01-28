document.addEventListener("DOMContentLoaded", async () => {
  const dropdown = document.querySelector(".dropdown");
  const fieldsContainer = document.getElementById("dynamic-fields");
  const activityTypeInput = document.getElementById("activity_type");
  const form = document.getElementById("activity-form");
  const selectedActivityBtn = document.querySelector(".selected-activity");
  const clearBtn = document.querySelector(".clr-dropbtn");
  const username = localStorage.getItem("currentUser");

  const templates = {
    run: `
      <label>Distance (miles)</label>
      <input type="number" step="0.01" name="distance" required>

      <label>Avg Pace (mm:ss per mile)</label>
      <input type="text" name="pace" placeholder="e.g. 7:45">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>

      <label>Route</label>
      <input type="text" name="route">
    `,
    lifting: `
      <label>Muscle Group</label>
      <input type="text" name="muscle_group" required>

      <label>Exercise</label>
      <input type="text" name="exercise" required>

      <label>Sets</label>
      <input type="number" name="sets" min="1" required>

      <label>Reps</label>
      <input type="number" name="reps" min="1" required>

      <label>Weight (lbs)</label>
      <input type="number" name="weight" step="0.5">
    `,
    bike: `
      <label>Distance (miles)</label>
      <input type="number" step="0.01" name="distance" required>

      <label>Elevation Gain (ft)</label>
      <input type="number" name="elevation">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>

      <label>Route</label>
      <input type="text" name="route">
    `,
    swim: `
      <label>Distance</label>
      <input type="number" name="distance" required>

      <label>Unit</label>
      <select name="unit">
        <option value="yards">Yards</option>
        <option value="meters">Meters</option>
      </select>

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>
    `,
    yoga: `
      <label>Type</label>
      <input type="text" name="yoga_type" placeholder="Vinyasa, Power, etc.">

      <label>Intensity (1-10)</label>
      <input type="number" name="intensity" min="1" max="10">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>
    `,
    walk: `
      <label>Distance (miles)</label>
      <input type="number" step="0.01" name="distance">

      <label>Steps</label>
      <input type="number" name="steps">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>

      <label>Route</label>
      <input type="text" name="route">
    `,
    soccer: `
      <label>Position</label>
      <input type="text" name="position">

      <label>Goals</label>
      <input type="number" name="goals" min="0">

      <label>Assists</label>
      <input type="number" name="assists" min="0">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>

      <label>Field</label>
      <input type="text" name="field">
    `,
    baseball: `
      <label>Position</label>
      <input type="text" name="position">

      <label>Hits</label>
      <input type="number" name="hits" min="0">

      <label>Runs</label>
      <input type="number" name="runs" min="0">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>
    `,
    football: `
      <label>Position</label>
      <input type="text" name="position">

      <label>Touchdowns</label>
      <input type="number" name="touchdowns" min="0">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>

      <label>Field</label>
      <input type="text" name="field">
    `,
    tennis: `
      <label>Match Type</label>
      <select name="match_type">
        <option value="singles">Singles</option>
        <option value="doubles">Doubles</option>
      </select>

      <label>Score</label>
      <input type="text" name="score" placeholder="e.g. 6-4, 3-6, 10-8">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>
    `,
    volleyball: `
      <label>Games Played</label>
      <input type="number" name="games" min="0">

      <label>Kills</label>
      <input type="number" name="kills" min="0">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>
    `,
    basketball: `
      <label>Points</label>
      <input type="number" name="points" min="0">

      <label>Rebounds</label>
      <input type="number" name="rebounds" min="0">

      <label>Assists</label>
      <input type="number" name="assists" min="0">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>
    `,
    equestrian: `
      <label>Discipline</label>
      <select name="discipline">
        <option>Trail Riding</option>
        <option>Dressage</option>
        <option>Jumping</option>
        <option>Eventing</option>
        <option>Barrel Racing</option>
        <option>Western Pleasure</option>
        <option>Endurance</option>
        <option>Other</option>
      </select>

      <label>Distance (miles)</label>
      <input type="number" step="0.01" name="distance">

      <label>Route / Location</label>
      <input type="text" name="route">

      <label>Notes</label>
      <textarea name="notes" rows="3"></textarea>

      <label>Horse Name</label>
      <input type="text" name="horse_name" required>

      <label>Horse Condition</label>
      <select name="horse_condition">
        <option>Excellent</option>
        <option>Good</option>
        <option>Okay</option>
        <option>Tired</option>
        <option>Off</option>
      </select>
    `,
  };

  function setFields(activityKey) {
    activityTypeInput.value = activityKey;
    fieldsContainer.innerHTML = templates[activityKey] || "";
  }

  // Click handling (only respond to menu items)
  dropdown.addEventListener("click", (e) => {
    const link = e.target.closest(".dropdown-content a");
    if (!link) return;

    e.preventDefault();

    const activityKey = link.dataset.activity;
    console.log("Selected:", activityKey);

    setFields(activityKey);
    selectedActivityBtn.textContent = link.textContent;
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = collectSportData(form);
    console.log("Form submit data:", data);
    try {
            //const username = localStorage.getItem("currentUser");
            const response = await sendActivityData(data, username);
            console.log("Response:", response);
            e.preventDefault();
            activityTypeInput.value = "";
            fieldsContainer.innerHTML = "";
            form.reset();
            selectedActivityBtn.textContent = "None Selected";
        } catch (err) {
            console.error("Error sending activity data:", err);
        }
  });

  //Clear button
  clearBtn.addEventListener("click", (e) => {
    e.preventDefault();
    activityTypeInput.value = "";
    fieldsContainer.innerHTML = "";
    form.reset();
    selectedActivityBtn.textContent = "None Selected";
  });

  await fillActivityTable(username);
});


function collectSportData(form) {
  if (!form) throw new Error("Form element not provided");

  const data = {};
  form.querySelectorAll("input, textarea, select").forEach(field => {
    if (field.type === "number") data[field.name] = field.value ? parseFloat(field.value) : null;
    else data[field.name] = field.value || "";
  });
  return data;
}


async function sendActivityData(data, username){
    const response = await fetch("/activity_api/enteractivity", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            form: data,
            username: username
        })
    });
    if(!response.ok){ throw new Error(`HTTP error ${response.status}`);}
        return await response.json();
}


//fill activities data
async function fillActivityTable(username) {
  try {
    const response = await fetch("/activity_api/fillactivity", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username })
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();

    //ensure array
    const activities = Array.isArray(data)
      ? data
      : data.activities;

    populateActivityTable(data.activities);


    return activities;

  } catch (err) {
    console.error("Failed to load activities:", err);
  }
}


function populateActivityTable(data){
  const activityTable = document.querySelector("#activities-body");
  activityTable.innerHTML = "";

  data.forEach(activity => {
    // Support merged OR split payloads
    const common = activity.common ?? activity;
    const sport  = activity.sport  ?? activity;

    let extra = "";

    // Sport-specific display
    if (common.activity_type === "swim" && sport.distance) {
      extra = `${sport.distance} ${sport.unit}`;
    }
    const dateObj = new Date(common.date);
    const formattedDate = dateObj.toLocaleDateString("en-US", { year:"numeric", month:"short", day:"numeric" });

    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${formattedDate}</td>
      <td>${common.activity_type}</td>
      <td>${common.duration} min</td>
      <td>${common.calories_burned}</td>
      <td>${extra}</td>
      <td>${common.visibility}</td>
      <td>${common.notes ?? ""}</td>
    `;

    activityTable.appendChild(row);
  });

}