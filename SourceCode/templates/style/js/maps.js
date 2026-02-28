// Initialize map
const map = L.map('map').setView([40.06428075146778, -79.8847461297468], 15);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Global variables
let drawing = false;
let routePoints = [];
let currentPolyline;
let routeMarkers = [];
// --- Function to calculate miles ---
function calculateDistanceMiles(coords) {
    let totalMeters = 0;
    for (let i = 1; i < coords.length; i++) {
        const prev = L.latLng(coords[i - 1]);
        const curr = L.latLng(coords[i]);
        totalMeters += prev.distanceTo(curr);
    }
    return (totalMeters / 1609.34).toFixed(2);
}

// --- Campus Loop Default Route ---
const campusLoop = [
    [40.06347895019966, -79.88769654458297],
    [40.06293295629167, -79.88676851082606],
    [40.06264558931943, -79.8863071761261],
    [40.062091326122854, -79.88538982828464],
    [40.06183679800746, -79.88488021437189],
    [40.06166848050564, -79.88441887967194],
    [40.061142944245425, -79.88292758769988],
    [40.060859675082135, -79.88180643709185],
    [40.06097873038118, -79.88142556774653],
    [40.06150559456981, -79.88117350719692],
    [40.06197359942061, -79.88111986362716],
    [40.06271254790295, -79.88115204976903],
    [40.06366376868995, -79.88142555858849],
    [40.06416049484094, -79.88159721801175],
    [40.064841947965505, -79.88209073885356],
    [40.065356355402976, -79.88267551261956],
    [40.06571760216947, -79.88287935818462],
    [40.06611168736633, -79.88322267703113],
    [40.0663990397185, -79.88367328301713],
    [40.066652408334974, -79.88413994922729],
    [40.06714916975694, -79.88521819096277],
    [40.06739546809616, -79.88606575936502],
    [40.06730926377871, -79.88632324849988],
    [40.067140959796944, -79.88644126435335],
    [40.066915185509814, -79.8866612029894],
    [40.06375829063405, -79.88803985408825],
    [40.06355850923744, -79.8878789503646],
    [40.06347895019966, -79.88769654458297] // close loop
];


// --- Draw default campus loop ---
const routeLine = L.polyline(campusLoop, { color: '#007bff', weight: 5 }).addTo(map);
map.fitBounds(routeLine.getBounds());

// Show campus loop distance in miles
const loopDistanceMiles = calculateDistanceMiles(campusLoop);
L.popup()
  .setLatLng(campusLoop[0])
  .setContent(`Campus Loop Distance: ${loopDistanceMiles} miles`)
  .openOn(map);

// --- Default Routes List ---
const defaultRoutes = { "Campus Loop": campusLoop };
const defaultRoutesList = document.getElementById("defaultRoutesList");

for (let name in defaultRoutes) {
    const li = document.createElement("li");
    li.textContent = name;
    li.style.cursor = "pointer";
    li.addEventListener("click", () => {
        if (currentPolyline) map.removeLayer(currentPolyline);
        currentPolyline = L.polyline(defaultRoutes[name], { color: 'blue', weight: 5 }).addTo(map);
        map.fitBounds(currentPolyline.getBounds());

        const miles = calculateDistanceMiles(defaultRoutes[name]);
        document.getElementById("routeDistance").textContent = `Distance: ${miles} miles`;
    });
    defaultRoutesList.appendChild(li);
}

// --- Add New Route Functionality ---
document.getElementById("startRoute").addEventListener("click", () => {
    drawing = true;
    routePoints = [];
    
    // Remove current polyline if any
    if (currentPolyline) map.removeLayer(currentPolyline);

    // Clear UI
    document.getElementById("newRouteList").innerHTML = "";
    document.getElementById("routeDistance").textContent = "";

    // Remove any leftover markers
    routeMarkers.forEach(marker => map.removeLayer(marker));
    routeMarkers = [];
});

// Finish route button
document.getElementById("endRoute").addEventListener("click", () => {
    drawing = false;

    // Remove all markers now
    routeMarkers.forEach(marker => map.removeLayer(marker));
    routeMarkers = [];

    if (routePoints.length > 1) {
        currentPolyline = L.polyline(routePoints, { color: 'red', weight: 5 }).addTo(map);
        map.fitBounds(currentPolyline.getBounds());

        const miles = calculateDistanceMiles(routePoints);
        document.getElementById("routeDistance").textContent = `Distance: ${miles} miles`;

        // Save to My Routes list
        const li = document.createElement("li");
        const routeCount = document.getElementById("savedRoutesList").children.length + 1;
        li.textContent = `Route ${routeCount} (${miles} miles)`;
        li.style.cursor = "pointer";

        li.addEventListener("click", () => {
            if (currentPolyline) map.removeLayer(currentPolyline);
            currentPolyline = L.polyline(routePoints, { color: 'red', weight: 5 }).addTo(map);
            map.fitBounds(currentPolyline.getBounds());
            document.getElementById("routeDistance").textContent = `Distance: ${miles} miles`;
        });

        document.getElementById("savedRoutesList").appendChild(li);
    }
});

// --- Click on map to add points while drawing ---
map.on('click', (e) => {
    if (!drawing) return;
    const point = [e.latlng.lat, e.latlng.lng];
    routePoints.push(point);

    // Show marker while drawing
    const marker = L.marker(point).addTo(map);
    routeMarkers.push(marker);

    // Update live polyline
    if (currentPolyline) map.removeLayer(currentPolyline);
    currentPolyline = L.polyline(routePoints, { color: 'red', weight: 5 }).addTo(map);

    // Update live distance
    if (routePoints.length > 1) {
        const miles = calculateDistanceMiles(routePoints);
        document.getElementById("routeDistance").textContent = `Distance: ${miles} miles`;
    }
});