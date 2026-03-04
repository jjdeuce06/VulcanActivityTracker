async function loadWeather() {
    try {
        const apiKey = "58c18f06ebfdd3ff8e3f178e47a11e35";
        const city = "California,PA,US"; // or dynamically detect user location
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=imperial&appid=${apiKey}`;

        const response = await fetch(url);
        const data = await response.json();

        if(data && data.main) {
            const temp = Math.round(data.main.temp);
            const desc = data.weather[0].description;
            const iconCode = data.weather[0].icon;

            document.getElementById("weather-temp").textContent = `${temp}°F`;
            document.getElementById("weather-desc").textContent = desc;

            // Optional: replace emoji with API icon
            document.querySelector(".weather-icon").innerHTML = `<img src="https://openweathermap.org/img/wn/${iconCode}.png" alt="${desc}" />`;
        }
    } catch(err) {
        console.error("Error fetching weather:", err);
        document.getElementById("weather-desc").textContent = "Unable to load weather";
    }
}

// Call on page load
loadWeather();

