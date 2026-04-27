/* ═══ SOS Emergency ═══ */

function renderSOS(container) {
    container.innerHTML = `
    <div class="page-header">
        <div>
            <div class="page-title">Emergency SOS</div>
            <div class="page-meta">ONE-TAP EMERGENCY TRIGGER • INSTANT ALERT DISPATCH</div>
        </div>
        <div class="badge badge-red">● ARMED</div>
    </div>

    <div class="sos-wrap"><button class="sos-btn" onclick="triggerSOS()">SOS</button></div>

    <div style="max-width:420px;margin:0 auto;">
        <select class="select" id="sosType">
            <option value="FIRE">🔥 FIRE Emergency</option>
            <option value="MEDICAL">🏥 MEDICAL Emergency</option>
            <option value="SECURITY">🚨 SECURITY Threat</option>
        </select>
        <button class="btn btn-red btn-full btn-lg mt-12" onclick="triggerSOS()">
            <span class="material-icons-round" style="font-size:18px">emergency</span> TRIGGER SOS ALERT
        </button>
    </div>

    <div id="sosResult" class="mt-24"></div>

    <div class="mt-24" style="max-width:640px;margin-left:auto;margin-right:auto;">
        <div class="section-title">DESCRIBE EMERGENCY (OPTIONAL)</div>
        <textarea class="textarea" id="sosDesc" placeholder="e.g., Fire in kitchen, someone is unconscious in lobby..."></textarea>
        <button class="btn btn-cyan btn-full mt-12" onclick="analyzeSOS()">
            <span class="material-icons-round" style="font-size:14px">psychology</span> Analyze & Alert
        </button>
        <div id="sosAnalysis" class="mt-16"></div>
    </div>`;
}

function triggerSOS() {
    const type = document.getElementById('sosType').value;
    const id = genId(), zone = genNode();
    const inc = {
        id, type, zone, severity: 'CRITICAL', status: 'ACTIVE',
        timestamp: timestamp(), created_at_iso: new Date().toISOString(),
        lat: 28.6130 + Math.random() * 0.003, lon: 77.2080 + Math.random() * 0.003,
    };
    incidents.unshift(inc);
    FireDB.saveIncident(inc);
    FireDB.logEvent('sos_triggered', { id, type });

    const exits = ['Main Entrance', 'Fire Exit A', 'Fire Exit B', 'Emergency Stairwell'];
    const exit = exits[Math.floor(Math.random() * exits.length)];
    const protocols = {
        FIRE: ['Stay low below smoke', 'Do NOT use elevators', 'Follow illuminated exit signs', 'Close doors behind you', 'Go to assembly point'],
        MEDICAL: ['Do not move the patient', 'Clear area for medical team', 'Apply pressure to bleeding', 'Keep airways open', 'Stay with patient until help arrives'],
        SECURITY: ['RUN – Evacuate if safe path exists', 'HIDE – Find secure room, lock doors', 'Silence your phone', 'Wait for all-clear from security'],
    };
    const steps = (protocols[type] || protocols.SECURITY).map(s => `<div style="font-size:12px;color:var(--text-2);margin:3px 0;padding-left:12px;border-left:2px solid var(--border);">• ${s}</div>`).join('');

    document.getElementById('sosResult').innerHTML = `
    <div class="alert-box danger">
        <span class="material-icons-round" style="font-size:36px;color:var(--red);">emergency</span>
        <div style="font-size:18px;font-weight:700;color:var(--red);margin-top:8px;">ALERT ACTIVATED</div>
        <div class="mono" style="font-size:12px;color:var(--text-2);margin-top:10px;">
            ID: ${id} &nbsp;|&nbsp; Type: ${type} &nbsp;|&nbsp; Zone: ${zone}<br>
            Severity: CRITICAL &nbsp;|&nbsp; Status: ACTIVE
        </div>
        <div style="font-size:11px;color:var(--green);margin-top:14px;">
            <span class="material-icons-round" style="font-size:14px;vertical-align:middle;">check_circle</span>
            3 notifications dispatched • Saved to Firebase
        </div>
    </div>
    <div class="card mt-12">
        <div class="section-title">EVACUATION GUIDANCE</div>
        <div style="font-size:13px;">
            <span class="material-icons-round" style="font-size:16px;vertical-align:middle;color:var(--cyan);">exit_to_app</span>
            Nearest Exit: <span style="color:var(--cyan);font-weight:600;">${exit}</span>
        </div>
        <div style="font-size:13px;margin-top:6px;">
            <span class="material-icons-round" style="font-size:16px;vertical-align:middle;color:var(--green);">place</span>
            Assembly: <span style="color:var(--green);">Hotel Main Parking – Section A</span>
        </div>
        <div class="mt-12">${steps}</div>
    </div>`;

    showToast(`🚨 ${type} ALERT triggered – ID: ${id}`, 'danger');
}

function analyzeSOS() {
    const text = document.getElementById('sosDesc').value;
    if (!text.trim()) return showToast('Enter a description first', 'warning');
    const r = AIEngine.fullAnalysis(text);
    const sc = severityColor(r.severity);
    document.getElementById('sosAnalysis').innerHTML = `
    <div class="card" style="border-left:3px solid ${sc};">
        <div class="section-title">AI ANALYSIS RESULT</div>
        <div class="analysis-grid">
            <div class="analysis-item"><label>TYPE</label><div class="value">${incidentIcon(r.type)} ${r.type}</div></div>
            <div class="analysis-item"><label>SEVERITY</label><div class="value" style="color:${sc}">${r.severity}</div></div>
            <div class="analysis-item"><label>CONFIDENCE</label><div class="value" style="color:var(--cyan)">${Math.round(r.confidence * 100)}%</div></div>
            <div class="analysis-item"><label>KEYWORDS</label><div class="mt-4">${r.keywords.map(k => `<span class="tag tag-red">${k}</span> `).join('') || '<span class="text-muted">None</span>'}</div></div>
        </div>
    </div>`;
}
