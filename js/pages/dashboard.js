/* ═══ Admin Dashboard ═══ */

function renderDashboard(container) {
    const active = incidents.filter(i => i.status === 'ACTIVE').length;
    const responding = incidents.filter(i => i.status === 'RESPONDING').length;
    const resolved = incidents.filter(i => i.status === 'RESOLVED').length;
    const critical = incidents.filter(i => i.severity === 'CRITICAL').length;

    container.innerHTML = `
    <div class="page-header">
        <div>
            <div class="page-title">Admin Dashboard</div>
            <div class="page-meta">INCIDENT MANAGEMENT • RESPONSE COORDINATION • FIREBASE SYNC</div>
        </div>
        <div class="badge badge-blue">
            <span class="material-icons-round" style="font-size:14px;">cloud_sync</span> FIREBASE LIVE
        </div>
    </div>

    <div class="grid grid-4 mb-16">
        <div class="metric-card red"><div class="metric-value" style="color:var(--red)">${active}</div><div class="metric-label">ACTIVE</div></div>
        <div class="metric-card orange"><div class="metric-value" style="color:var(--orange)">${responding}</div><div class="metric-label">RESPONDING</div></div>
        <div class="metric-card green"><div class="metric-value" style="color:var(--green)">${resolved}</div><div class="metric-label">RESOLVED</div></div>
        <div class="metric-card red"><div class="metric-value" style="color:var(--red)">${critical}</div><div class="metric-label">CRITICAL</div></div>
    </div>

    <div class="section-title">INCIDENT MANAGEMENT</div>
    <div class="grid grid-3 mb-12">
        <select class="select" id="fType" onchange="filterDash()">
            <option value="ALL">All Types</option>
            <option value="FIRE">🔥 Fire</option>
            <option value="MEDICAL">🏥 Medical</option>
            <option value="SECURITY">🚨 Security</option>
        </select>
        <select class="select" id="fStatus" onchange="filterDash()">
            <option value="ALL">All Status</option>
            <option value="ACTIVE">Active</option>
            <option value="RESPONDING">Responding</option>
            <option value="RESOLVED">Resolved</option>
        </select>
        <select class="select" id="fSev" onchange="filterDash()">
            <option value="ALL">All Severity</option>
            <option value="CRITICAL">Critical</option>
            <option value="PRIORITY">Priority</option>
            <option value="MODERATE">Moderate</option>
            <option value="LOW">Low</option>
        </select>
    </div>

    <div class="table-wrap">
        <table class="event-table">
            <thead><tr><th>ID</th><th>TYPE</th><th>ZONE</th><th>SEVERITY</th><th>STATUS</th><th>TIME</th><th>ACTION</th></tr></thead>
            <tbody id="dashBody"></tbody>
        </table>
    </div>

    <div class="flex gap-12 mt-16">
        <button class="btn btn-red" onclick="App.generateAlert()">
            <span class="material-icons-round" style="font-size:14px">notification_important</span> New Alert
        </button>
        <button class="btn btn-green" onclick="resolveAllDash()">
            <span class="material-icons-round" style="font-size:14px">done_all</span> Resolve All
        </button>
        <button class="btn btn-blue" onclick="dataLoaded=false;initData().then(()=>showPage('dashboard'))">
            <span class="material-icons-round" style="font-size:14px">cloud_download</span> Sync Firebase
        </button>
        <button class="btn" onclick="incidents=[];showPage('dashboard')">
            <span class="material-icons-round" style="font-size:14px">delete_sweep</span> Clear All
        </button>
    </div>`;

    filterDash();
}

function filterDash() {
    const t = document.getElementById('fType').value;
    const s = document.getElementById('fStatus').value;
    const sv = document.getElementById('fSev').value;
    let f = [...incidents];
    if (t !== 'ALL') f = f.filter(i => i.type === t);
    if (s !== 'ALL') f = f.filter(i => i.status === s);
    if (sv !== 'ALL') f = f.filter(i => i.severity === sv);

    document.getElementById('dashBody').innerHTML = f.map(i => `
        <tr>
            <td style="font-weight:600">${i.id}</td>
            <td>${incidentIcon(i.type)} ${i.type}</td>
            <td>${i.zone}</td>
            <td><span style="color:${severityColor(i.severity)};font-weight:600">${i.severity}</span></td>
            <td><span style="color:${statusColor(i.status)};font-weight:600">${i.status}</span></td>
            <td style="color:var(--text-3)">${i.timestamp}</td>
            <td>${i.status !== 'RESOLVED'
            ? `<button class="btn btn-green" style="padding:4px 10px;font-size:10px;" onclick="resolveOne(${i.id})">Resolve</button>`
            : '<span class="text-muted mono" style="font-size:10px;">Done</span>'}</td>
        </tr>`).join('');
}

function resolveOne(id) {
    const i = incidents.find(x => x.id === id);
    if (i) { i.status = 'RESOLVED'; FireDB.updateStatus(id, 'RESOLVED'); showToast(`✅ Incident ${id} resolved`, 'success'); filterDash(); }
}

function resolveAllDash() {
    incidents.forEach(i => { if (i.status === 'ACTIVE') { i.status = 'RESOLVED'; FireDB.updateStatus(i.id, 'RESOLVED'); } });
    showToast('✅ All active incidents resolved', 'success');
    showPage('dashboard');
}
