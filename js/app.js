/* ═══════════════════════════════════════════
   App Controller – Navigation, Maps, Toast
   ═══════════════════════════════════════════ */

let currentPage = 'monitoring';
let leafletMaps = {};

const App = {
    async init() {
        await initData();
        this.setupNav();
        showPage('monitoring');

        // Real-time Firestore listener
        FireDB.onIncidents(data => {
            if (data && data.length > 0 && currentPage === 'monitoring') {
                // Silently update
            }
        });
    },

    setupNav() {
        document.querySelectorAll('.nav-item').forEach(el => {
            el.addEventListener('click', () => showPage(el.dataset.page));
        });
    },

    generateAlert() {
        const types = ['FIRE', 'MEDICAL', 'SECURITY'];
        const inc = {
            id: genId(),
            type: types[Math.floor(Math.random() * 3)],
            zone: genNode(),
            severity: 'CRITICAL',
            status: 'ACTIVE',
            timestamp: timestamp(),
            created_at_iso: new Date().toISOString(),
            lat: 28.6130 + Math.random() * 0.003,
            lon: 77.2080 + Math.random() * 0.003,
        };
        incidents.unshift(inc);
        FireDB.saveIncident(inc);
        FireDB.logEvent('alert_generated', { id: inc.id, type: inc.type });
        showToast(`🚨 ${inc.type} ALERT – ID: ${inc.id}`, 'danger');
        showPage(currentPage);
    }
};

async function showPage(page) {
    currentPage = page;
    if (!dataLoaded) await initData();

    document.querySelectorAll('.nav-item').forEach(el => {
        el.classList.toggle('active', el.dataset.page === page);
    });

    const main = document.getElementById('mainContent');
    switch (page) {
        case 'monitoring': renderMonitoring(main); break;
        case 'sos': renderSOS(main); break;
        case 'voice': renderVoice(main); break;
        case 'tracking': renderTracking(main); break;
        case 'dashboard': renderDashboard(main); break;
        case 'assistant': renderAssistant(main); break;
        case 'analytics': renderAnalytics(main); break;
    }
}

// ── Leaflet Map (Free, Dark Tiles, No API Key) ──
function initGoogleMap(containerId, center = { lat: 20, lng: 10 }, zoom = 2) {
    if (leafletMaps[containerId]) {
        leafletMaps[containerId].remove();
        delete leafletMaps[containerId];
    }

    setTimeout(() => {
        const el = document.getElementById(containerId);
        if (!el) return;

        const map = L.map(containerId, {
            center: [center.lat, center.lng || center.lon || 10],
            zoom,
            zoomControl: true,
            attributionControl: false,
        });

        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            maxZoom: 19,
        }).addTo(map);

        leafletMaps[containerId] = map;
    }, 150);
}

function getGMap(id) { return leafletMaps[id]; }

function addMarker(mapId, lat, lng, title, color = '#ef4444', scale = 8) {
    setTimeout(() => {
        const map = getGMap(mapId);
        if (!map) return;
        L.circleMarker([lat, lng], {
            radius: scale,
            fillColor: color,
            fillOpacity: 0.9,
            color: color,
            weight: 2,
        }).addTo(map).bindPopup(title);
    }, 300);
}

function addLine(mapId, from, to, color = '#06b6d4') {
    setTimeout(() => {
        const map = getGMap(mapId);
        if (!map) return;
        L.polyline([[from.lat, from.lng || from.lon], [to.lat, to.lng || to.lon]], {
            color,
            weight: 2,
            opacity: 0.7,
            dashArray: '6,8',
        }).addTo(map);
    }, 300);
}

// ── Toast ──
function showToast(msg, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icons = { danger: 'error', success: 'check_circle', info: 'info', warning: 'warning' };
    toast.innerHTML = `<span class="material-icons-round" style="font-size:16px;">${icons[type] || 'info'}</span> ${msg}`;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(50px)';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// ── Boot ──
document.addEventListener('DOMContentLoaded', () => App.init());
