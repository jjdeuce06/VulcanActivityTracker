async function loadForecast() {
   // Get API key from Flask
    const keyRes = await fetch("/map_api/send-weatherkey", {
        method: "POST"
    });

    const keyData = await keyRes.json();
    const API_KEY = keyData.key;

    // Now call OpenWeather
    const res = await fetch(
        `https://api.openweathermap.org/data/2.5/forecast?q=California,PA,US&units=imperial&appid=${API_KEY}`
    );

    const data = await res.json();


    const container = document.getElementById("forecastContainer");
    container.innerHTML = "";

    // Grab one forecast per day (every 8th item = 24 hrs)
    const daily = data.list.filter((_, index) => index % 8 === 0);

    let bestScore = -1;
    let bestIndex = -1;

    daily.forEach((day, i) => {
        const temp = day.main.temp;
        const wind = day.wind.speed;
        const rain = day.weather[0].main;

        let score = 0;
        if (temp > 45 && temp < 70) score += 2;
        if (wind < 12) score += 1;
        if (rain !== "Rain") score += 2;

        if (score > bestScore) {
            bestScore = score;
            bestIndex = i;
        }
    });

    daily.forEach((day, i) => {
        const div = document.createElement("div");
        div.className = "forecast-day";

        if (i === bestIndex) {
            div.classList.add("best-day");
        }

        const date = new Date(day.dt * 1000);
        const icon = day.weather[0].icon;

        div.innerHTML = `
            <h4>${date.toLocaleDateString("en-US", { weekday: "short" })}</h4>
            <img src="https://openweathermap.org/img/wn/${icon}@2x.png">
            <p>${Math.round(day.main.temp)}°F</p>
            <p>💨 ${day.wind.speed} mph</p>
        `;

        container.appendChild(div);
    });
}

loadForecast();