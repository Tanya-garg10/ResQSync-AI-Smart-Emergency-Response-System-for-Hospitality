/* ═══ Live Tracking – Leaflet Dark Map ═══ */

const HOTEL = {
    'LOBBY': { lat: 28.6139, lng: 77.2090, floor: 'Ground' },
    'POOL': { lat: 28.6145, lng: 77.2095, floor: 'Ground' },
    'RESTAURANT': { lat: 28.6142, lng: 77.2088, floor: '1st' },
    'ROOM-101': { lat: 28.6138, lng: 77.2092, floor: '1st' },
    'ROOM-201': { lat: 28.6140, lng: 77.2093, floor: '2nd' },
    'PARKING': { lat: 28.6135, lng: 77.2085, floor: 'Basement' },
    'CONFERENCE': { lat: 28.6143, lng: 77.2087, floor: '2nd' },
};

const EXITS = [
    { name: 'Main Entrance', lat: 28.6136, lng: 77.2089 },
    { name: 'Fire Exit A', lat: 28.6141, lng: 77.2096 },
    { name: 'Fire Exit B', lat: 28.6137, lng: 77.2083 },
];

const RESPONDERS = [
    { name: 'Security Team Alpha', status: 'EN ROUTE', eta: '45s', color: 'var(--cyan)' },
    { name: 'Medical Unit 1', status: 'EN ROUTE', eta: '1m 20s', color: 'var(--cyan)' },
    { name: 'Fire Response', status: 'STANDBY', eta: '—', color: 'var(--text-3)' },
    { name: 'Floor Manager L2', status: 'ON SITE', eta: 'Arrived', color: 'var(--green)' },
];

function renderTracking(container) {
    let respHTML = RESPONDERS.map(r => `
        <div class="responder-card">
            <div class="flex justify-between items-center">
                <span style="font-size:12px;font-weight:600;">${r.name}</span>
                <span class="mono" style="font-size:10px;color:${r.color}">${r.status}</span>
            </div>
            <div style="font-size:11px;color:var(--text-3);margin-top:4px;">ETA: ${r.eta}</div>
        </div>`).join('');

    let exitHTML = EXITS.map(e => `
        <div class="card" style="border-left:3px solid var(--green);padding:10px 14px;margin-bottom:6px;">
            <span class="material-icons-round" style="font-size:14px;vertical-align:middle;color:var(--green);">exit_to_app</span>
            <span style="font-size:12px;margin-left:4px;">${e.name}</span>
        </div>`).join('');

    container.innerHTML = `
    <div class="page-header">
        <div>
            <div class="page-title">Live Tracking</div>
            <div class="page-meta">DARK MAP • RESPONDER ETA • EVACUATION ROUTES</div>
        </div>
    </div>

    <div style="display:grid;grid-template-columns:2fr 1fr;gap:20px;">
        <div class="map-container map-container-lg" id="trackMap"></div>
        <div>
            <div class="section-title">ACTIVE RESPONDERS</div>
            ${respHTML}
            <div class="section-title mt-20">EMERGENCY EXITS</div>
            ${exitHTML}
            <div class="card mt-20">
                <div style="font-size:10px;color:var(--text-3);letter-spacing:1.5px;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">MAP LEGEND</div>
                <div style="font-size:11px;line-height:2.2;color:var(--text-2);">
                    🔴 Critical Incident<br>🟠 Priority Incident<br>
                    🟢 Responder<br>🔵 Hotel Zone<br>
                    🚪 Emergency Exit<br>--- Responder Route
                </div>
            </div>
        </div>
    </div>`;

    // Leaflet map
    initGoogleMap('trackMap', { lat: 28.6139, lng: 77.2090 }, 17);

    setTimeout(() => {
        const map = getGMap('trackMap');
        if (!map) return;

        // Hotel zones (blue markers)
        for (const [name, loc] of Object.entries(HOTEL)) {
            L.circleMarker([loc.lat, loc.lng], {
                radius: 6, fillColor: '#3b82f6', fillOpacity: 0.8,
                color: '#3b82f6', weight: 1,
            }).addTo(map).bindPopup(`<b>${name}</b><br>Floor: ${loc.floor}`);
        }

        // Exits (green arrows)
        EXITS.forEach(e => {
            L.marker([e.lat, e.lng], {
                icon: L.divIcon({
                    html: '<span style="font-size:18px;">🚪</span>',
                    className: '',
                    iconSize: [20, 20],
                    iconAnchor: [10, 10],
                })
            }).addTo(map).bindPopup(`Exit: ${e.name}`);
        });

        // Incidents + responders
        incidents.slice(0, 3).forEach(inc => {
            const lat = inc.lat, lng = inc.lon || inc.lng;
            const color = inc.severity === 'CRITICAL' ? '#ef4444' : '#f59e0b';

            L.circleMarker([lat, lng], {
                radius: 10, fillColor: color, fillOpacity: 0.9,
                color: color, weight: 2,
            }).addTo(map).bindPopup(`🚨 ${inc.type} | ${inc.severity}`);

            // Responder moving toward incident
            const p = 0.3 + Math.random() * 0.6;
            const rLat = 28.6139 + (lat - 28.6139) * p;
            const rLng = 77.2090 + (lng - 77.2090) * p;

            L.circleMarker([rLat, rLng], {
                radius: 7, fillColor: '#22c55e', fillOpacity: 0.9,
                color: '#22c55e', weight: 2,
            }).addTo(map).bindPopup('🏃 Responder | EN ROUTE');

            // Route line
            L.polyline([[rLat, rLng], [lat, lng]], {
                color: '#06b6d4', weight: 2, opacity: 0.6, dashArray: '6,8',
            }).addTo(map);
        });
    }, 300);
}
