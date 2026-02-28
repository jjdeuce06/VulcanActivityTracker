
const map = L.map('map').setView([40.06428075146778, -79.8847461297468], 15); //pennwest california

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Example marker
L.marker([40.06428075146778, -79.8847461297468])
    .addTo(map)
    .bindPopup("PennWest California Campus")
    .openPopup();
//route lines
let routePoints = [];

map.on('click', function(e) {
    const latlng = [e.latlng.lat, e.latlng.lng];
    routePoints.push(latlng);
    console.log(`[${latlng[0]}, ${latlng[1]}],`);
    L.marker(latlng).addTo(map);

    if (routePoints.length > 1) {
        if (window.currentRoute) {
            map.removeLayer(window.currentRoute);
        }

        window.currentRoute = L.polyline(routePoints, {
            color: 'red',
            weight: 5
        }).addTo(map);
    }
});
function calculateDistanceMiles(coords) {
    let totalMeters = 0;

    for (let i = 1; i < coords.length; i++) {
        const prev = L.latLng(coords[i - 1]);
        const curr = L.latLng(coords[i]);
        totalMeters += prev.distanceTo(curr); // distance in meters
    }

    const miles = totalMeters / 1609.34; // convert meters → miles
    return miles.toFixed(2); // 2 decimal places
}
// Your loop coordinates (make sure first point is repeated at end)
var campusLoop = [
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

// Draw the loop
var routeLine = L.polyline(campusLoop, {
    color: '#ff3b30',
    weight: 5
}).addTo(map);

// Fit map to loop
map.fitBounds(routeLine.getBounds());

// Calculate distance in miles
var loopDistanceMiles = calculateDistanceMiles(campusLoop);

// Show on map
L.popup()
 .setLatLng(campusLoop[0])
 .setContent(`Campus Loop Distance: ${loopDistanceMiles} miles`)
 .openOn(map);

console.log("Campus Loop Distance:", loopDistanceMiles, "miles");