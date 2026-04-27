/* ═══════════════════════════════════════════
   Data Layer – Incidents, Helpers
   ═══════════════════════════════════════════ */

let incidents = [];
let dataLoaded = false;

function genId() { return Math.floor(1000 + Math.random() * 9000); }
function genNode() { return `NODE-${Math.floor(1000 + Math.random() * 9000)}`; }

function timestamp() {
    return new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}
function dateDisplay() {
    return new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
}

function incidentIcon(type) {
    return { FIRE: '🔥', MEDICAL: '🏥', SECURITY: '🚨', EVACUATION: '🚪' }[type] || '⚠️';
}
function severityColor(sev) {
    return { CRITICAL: 'var(--red)', PRIORITY: 'var(--orange)', MODERATE: 'var(--yellow)', LOW: 'var(--green)' }[sev] || 'var(--text-3)';
}
function statusColor(st) {
    return { ACTIVE: 'var(--green)', RESPONDING: 'var(--orange)', RESOLVED: 'var(--text-3)', 'EN ROUTE': 'var(--cyan)' }[st] || 'var(--text-3)';
}
function sevClass(sev) {
    return { CRITICAL: 'critical', PRIORITY: 'priority', MODERATE: 'moderate', LOW: 'low' }[sev] || '';
}

function generateDemoIncidents(count = 8) {
    const types = ['FIRE', 'MEDICAL', 'SECURITY', 'MEDICAL'];
    const sevs = ['CRITICAL', 'PRIORITY', 'MODERATE', 'LOW'];
    const stats = ['ACTIVE', 'RESPONDING', 'ACTIVE', 'RESOLVED'];
    const arr = [];
    for (let i = 0; i < count; i++) {
        arr.push({
            id: genId(),
            type: types[i % 4],
            zone: genNode(),
            severity: sevs[i % 4],
            status: stats[i % 4],
            timestamp: timestamp(),
            created_at_iso: new Date(Date.now() - i * 60000).toISOString(),
            lat: 28.6130 + Math.random() * 0.003,
            lon: 77.2080 + Math.random() * 0.003,
        });
    }
    return arr;
}

function generateHealth() {
    return {
        'DATABASE UPLINK': 88 + Math.floor(Math.random() * 12),
        'SATELLITE LINK-1': 80 + Math.floor(Math.random() * 15),
        'NEURAL CORE': 85 + Math.floor(Math.random() * 14),
        'VOICE ENGINE': 100,
    };
}

// Load from Firestore first, fallback to demo
async function initData() {
    if (dataLoaded) return;
    const remote = await FireDB.getIncidents(20);
    if (remote && remote.length > 0) {
        incidents = remote;
        console.log('📡 Loaded from Firestore:', incidents.length);
    } else {
        incidents = generateDemoIncidents(8);
        console.log('🔧 Using demo data');
    }
    dataLoaded = true;
}
