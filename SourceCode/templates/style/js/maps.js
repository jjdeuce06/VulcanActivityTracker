document.addEventListener("DOMContentLoaded", async () => {
    await loadUserRoutes();
});

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

const coalcenter =[[40.07048014037708, -79.89926115272135], 
[40.0699302244132, -79.89979768347321], 
[40.070824861553206, -79.9014609288039], 
[40.07106288229943, -79.90189015340538], 
[40.07158816652017, -79.90132143080842],
[40.0710382595022, -79.90029129176489], 
[40.07043910202561, -79.89912165472587],
[40.0697906927908, -79.89803786260715],
[40.06967578418129, -79.89738329508991],
[40.06921614780468, -79.89694333987337],
[40.06921614780468, -79.89560201299378],
[40.06817374667178, -79.89465771887052],
[40.06782901207836, -79.89232917540754],
[40.06757456399751, -79.89055862392644],
[40.06743502754962, -79.88943190934756],
[40.067213410250844, -79.88744674556575],
[40.066450056258425, -79.886073226841], 
[40.06548969553724, -79.88692094542894],
[40.06443082058788, -79.88512893271778],
[40.06290404168797, -79.88655610451768],
[40.062862998772175, -79.88660975759285],
[40.06225556072761, -79.8855688879343],
[40.06183691784176, -79.88486066734184],
[40.06150856868034, -79.88389491198853], 
[40.061262305770846, -79.88309011586077],
[40.06110633880113, -79.88242481772849], 
[40.060942162657824, -79.88214582173752], 
[40.06093395384026, -79.88183463390145],
[40.0611309651885, -79.88125518068946],
[40.06181229170952, -79.88107276023382],
[40.06287941594145, -79.8811800663842], 
[40.063864438859056, -79.88149125422026], 
[40.06464423856862, -79.88187755636162], 
[40.06481661414192, -79.88207070743226], 
[40.06520240551124, -79.88246774018863], 
[40.065719526685726, -79.88289696479009],
[40.06615456209389, -79.88328326693143], 
[40.066794797830354, -79.88438852028024], 
[40.06732832301428, -79.88564400223954], 
[40.067426819514395, -79.88619126360643], 
[40.067155953796416, -79.88647025959737],
[40.06681942216161, -79.886652680053]
]

L.marker([40.06428075146778, -79.8847461297468])
    .addTo(map)
    .bindPopup("PennWest California Campus")
    .openPopup();


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
const defaultRoutes = { "Campus Loop": campusLoop, "Coal Center": coalcenter};
const defaultRoutesList = document.getElementById("defaultRoutesList");

for (let name in defaultRoutes) {

    const li = document.createElement("li");

    const miles = calculateDistanceMiles(defaultRoutes[name]);

    li.innerHTML = `

        <div class="route-icon">📍</div>
        <div class="route-title">${name}</div>
        <div class="route-hover-info">${miles} miles</div>
    `;

    li.addEventListener("click", () => {
        if (currentPolyline) map.removeLayer(currentPolyline);

        currentPolyline = L.polyline(defaultRoutes[name], {
            color: 'blue',
            weight: 5
        }).addTo(map);

        map.fitBounds(currentPolyline.getBounds());

        document.getElementById("routeDistance").textContent =
            `Distance: ${miles} miles`;
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

    const container = document.getElementById("routeNameContainer");
    container.innerHTML = ""; // clear previous

    const input = document.createElement("input");
    input.type = "text";
    input.id = "routeNameInput";
    input.placeholder = "Enter route name";
    input.classList.add("route-input");
    container.appendChild(input);

    input.focus(); // auto focus for better UX
});


// Finish route button
document.getElementById("endRoute").addEventListener("click", async (e) => {
    drawing = false;

    routeMarkers.forEach(marker => map.removeLayer(marker));
    routeMarkers = [];

    const nameInput = document.getElementById("routeNameInput");
    const routeName = nameInput ? nameInput.value.trim() : "";

    if (routePoints.length > 1) {

        if (!routeName) {
            alert("Please enter a route name.");
            return;
        }

        currentPolyline = L.polyline(routePoints, { color: 'red', weight: 5 }).addTo(map);
        map.fitBounds(currentPolyline.getBounds());

        const miles = calculateDistanceMiles(routePoints);
        document.getElementById("routeDistance").textContent = `Distance: ${miles} miles`;

        const li = document.createElement("li");
        li.classList.add("route-item");
        li.innerHTML = `
            <div class="route-icon">📍</div>
            <span class="route-title">${routeName}</span>
            <div class="route-hover-info">${miles} miles</div>
            <button class="delete-btn">🗑</button>
        `;
        await deleteRoute(li, routeName);
       
        li.style.cursor = "pointer";

        const savedPoints = [...routePoints];

        li.addEventListener("click", () => {
            if (currentPolyline) map.removeLayer(currentPolyline);
            currentPolyline = L.polyline(savedPoints, { color: 'red', weight: 5 }).addTo(map);
            map.fitBounds(currentPolyline.getBounds());
            document.getElementById("routeDistance").textContent = `Distance: ${miles} miles`;
        });

        document.getElementById("savedRoutesList").appendChild(li);
        document.getElementById("routeNameContainer").innerHTML = "";

        await storeRoutes(routePoints, routeName);
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

async function storeRoutes(routePoints, route_name) {
    try {
        const response = await fetch('/map_api/store_map_routes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: route_name,
                distance: calculateDistanceMiles(routePoints),
                coordinates: routePoints
            })
        });
        const data = await response.json();
        console.log('Route saved:', data);
    } catch (error) {
        console.error('Error saving route:', error);
    }
}

async function loadUserRoutes() {
    try{
        const response = await fetch('/map_api/get_user_routes');
        const data = await response.json();
        console.log("Load Maps Data", data);

        if(data.success){
            displayMaps(data.maps.routes);
        }
    }catch(error){
        console.error("error loading maps", error);
    } 
}

function displayMaps(routes) {
    if (!routes || !Array.isArray(routes)) {
        console.warn("No routes to display:", routes);
        return;
    }

    const container = document.getElementById("savedRoutesList");
    container.innerHTML = "";

    routes.forEach(async route => {
        const li = document.createElement("li");
        li.classList.add("route-item");
        li.innerHTML = `
            <div class="route-icon">📍</div>
            <span class="route-title">${route.name}</span>
            <div class="route-hover-info">${route.distance} miles</div>
            <button class="delete-btn">🗑</button>
        `;
        li.style.cursor = "pointer";

        await deleteRoute(li, route.name);

        li.addEventListener("click", () => {
            if (window.currentPolyline) map.removeLayer(window.currentPolyline);
            window.currentPolyline = L.polyline(route.coordinates, { color: 'blue', weight: 5 }).addTo(map);
            map.fitBounds(window.currentPolyline.getBounds());
            document.getElementById("routeDistance").textContent = `Distance: ${route.distance} miles`;
        });

        container.appendChild(li);
    });
}

async function deleteRoute(li, routeName) {
    const deleteBtn = li.querySelector(".delete-btn");

    deleteBtn.addEventListener("click", async (e) => {
        e.stopPropagation(); //prevents route click

        // Remove from UI
        li.remove();

        // Remove polyline if it's currently active
        if (currentPolyline) {
            map.removeLayer(currentPolyline);
            currentPolyline = null;
        }

        // Clear distance display
        document.getElementById("routeDistance").textContent = "";

        // Remove from backend
        await deleteRouteFromStorage(routeName);
    });
}

//technically could delete routes of same name unique not implemented
async function deleteRouteFromStorage(routeName) {
    try {
        const response = await fetch('/map_api/delete_route', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: routeName })
        });
        const data = await response.json();
        console.log('Route deleted:', data);
    } catch (error) {
        console.error('Error deleting route:', error);
    }
}