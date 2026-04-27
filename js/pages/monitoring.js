/* ═══ Global Monitoring ═══ */

function renderMonitoring(container) {
    const health = generateHealth();

    let healthHTML = '';
    for (const [name, val] of Object.entries(health)) {
        const c = val >= 95 ? 'var(--green)' : val >= 85 ? 'var(--orange)' : 'var(--red)';
        healthHTML += `<div class="health-item">
            <div class="health-label"><span>${name}</span><span style="color:${c};font-weight:600">${val}%</span></div>
            <div class="health-track"><div class="health-fill" style="width:${val}%;background:${c}"></div></div>
        </div>`;
    }

    let intelHTML = incidents.slice(0, 5).map(inc => `
        <div class="intel-card ${sevClass(inc.severity)}">
            <div class="intel-header">
                <span class="intel-id">ID: ${inc.id}</span>
                <span class="intel-time">${inc.timestamp}</span>
            </div>
            <div class="intel-meta">
                ${incidentIcon(inc.type)} ${inc.type} • <span style="color:${severityColor(inc.severity)}">${inc.severity}</span>
            </div>
        </div>`).join('');

    let rowsHTML = incidents.map(inc => `
        <tr>
            <td style="font-weight:600">${incidentIcon(inc.type)} ${inc.type}</td>
            <td>${inc.zone}</td>
            <td><span style="color:${statusColor(inc.status)};font-weight:600">${inc.status}</span></td>
            <td style="color:var(--text-3)">${inc.timestamp}</td>
        </tr>`).join('');

    container.innerHTML = `
    <div class="page-header">
        <div>
            <div class="page-title">Command Overview</div>
            <div class="page-meta">📅 ${dateDisplay()} &nbsp;⇄ UPLINK ESTABLISHED &nbsp;🕐 ${new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}</div>
        </div>
        <div class="badge badge-green">● SYSTEM NOMINAL</div>
    </div>

    <div class="grid grid-main">
        <div>
            <div class="grid grid-map">
                <div class="map-container" id="monitorMap"></div>
                <div>
                    <div class="section-title">NETWORK HEALTH</div>
                    ${healthHTML}
                </div>
            </div>
            <div class="mt-24">
                <div class="section-title">RECENT EVENT LOG</div>
                <div class="table-wrap">
                    <table class="event-table">
                        <thead><tr><th>INCIDENT</th><th>ZONE</th><th>STATUS</th><th>TIMESTAMP</th></tr></thead>
                        <tbody>${rowsHTML}</tbody>
                    </table>
                </div>
            </div>
            <div class="flex gap-12 mt-16">
                <button class="btn btn-blue" onclick="dataLoaded=false;initData().then(()=>showPage('monitoring'))">
                    <span class="material-icons-round" style="font-size:14px">refresh</span> Refresh
                </button>
                <button class="btn btn-red" onclick="App.generateAlert()">
                    <span class="material-icons-round" style="font-size:14px">notification_important</span> Generate Alert
                </button>
                <button class="btn btn-green" onclick="incidents=incidents.filter(i=>i.status!=='RESOLVED');showPage('monitoring')">
                    <span class="material-icons-round" style="font-size:14px">check_circle</span> Clear Resolved
                </button>
            </div>
        </div>
        <div>
            <div class="section-title">TACTICAL INTEL STREAM</div>
            ${intelHTML}
        </div>
    </div>`;

    // Google Map
    initGoogleMap('monitorMap', { lat: 20, lng: 10 }, 2);
    incidents.slice(0, 6).forEach(inc => {
        const color = inc.severity === 'CRITICAL' ? '#ef4444' : inc.severity === 'PRIORITY' ? '#f59e0b' : '#22c55e';
        addMarker('monitorMap', inc.lat, inc.lon, `${inc.type} | ${inc.severity}`, color);
    });
}
