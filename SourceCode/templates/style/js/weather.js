// async function loadWeather() {
//     try {
//         const apiKey = "58c18f06ebfdd3ff8e3f178e47a11e35";
//         const city = "California,PA,US"; // or dynamically detect user location
//         const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=imperial&appid=${apiKey}`;

//         const response = await fetch(url);
//         const data = await response.json();

//         if(data && data.main) {
//             const temp = Math.round(data.main.temp);
//             const desc = data.weather[0].description;
//             const iconCode = data.weather[0].icon;

//             document.getElementById("weather-temp").textContent = `${temp}°F`;
//             document.getElementById("weather-desc").textContent = desc;

//             // Optional: replace emoji with API icon
//             document.querySelector(".weather-icon").innerHTML = `<img src="https://openweathermap.org/img/wn/${iconCode}.png" alt="${desc}" />`;
//         }
//     } catch(err) {
//         console.error("Error fetching weather:", err);
//         document.getElementById("weather-desc").textContent = "Unable to load weather";
//     }
// }

// // Call on page load
// loadWeather();



async function loadForecast() {
    const res = await fetch(
        "https://api.openweathermap.org/data/2.5/forecast?lat=40.0643&lon=-79.8847&units=imperial&appid=58c18f06ebfdd3ff8e3f178e47a11e35"
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