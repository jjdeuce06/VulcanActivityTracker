document.addEventListener("DOMContentLoaded", () => {
  const dropdown = document.querySelector(".dropdown");
  const fieldsContainer = document.getElementById("dynamic-fields");
  const activityTypeInput = document.getElementById("activity_type");
  const form = document.getElementById("activity-form");
  const selectedActivityBtn = document.querySelector(".selected-activity");
  const clearBtn = document.querySelector(".clr-dropbtn");

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

      <label>Duration (minutes)</label>
      <input type="number" name="duration" required>

      <label>Distance (miles)</label>
      <input type="number" step="0.01" name="distance">

      <label>Elevation Gain (ft)</label>
      <input type="number" name="elevation">

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

      <label>Tack Used</label>
      <input type="text" name="tack">
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

  // OPTIONAL: stop default submit while you're testing
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    console.log("Form submit data:", data);
  });

  // Optional default state
  // setFields("run");

  //Clear button
  clearBtn.addEventListener("click", (e) => {
    e.preventDefault();
    activityTypeInput.value = "";
    fieldsContainer.innerHTML = "";
    form.reset();
    selectedActivityBtn.textContent = "None Selected";
  });

});




