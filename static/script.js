// Initialize map
const map = L.map('map').setView([20.5937, 78.9629], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let markers = {};

async function fetchPositions() {
    try {
        const res = await fetch('/positions');
        const data = await res.json();

        data.forEach(d => {
            const { phone, latitude, longitude, updated_at } = d;
            if (markers[phone]) {
                markers[phone].setLatLng([latitude, longitude]);
                markers[phone].setPopupContent(`${phone}<br>${updated_at}`);
            } else {
                markers[phone] = L.marker([latitude, longitude])
                    .addTo(map)
                    .bindPopup(`${phone}<br>${updated_at}`);
            }
        });
    } catch (err) {
        console.error('Error fetching positions:', err);
    }
}

// Refresh every 5 seconds
setInterval(fetchPositions, 5000);
fetchPositions();
