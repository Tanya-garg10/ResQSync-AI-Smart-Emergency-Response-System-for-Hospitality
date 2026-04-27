/* ═══ Settings – API Keys & Configuration ═══ */

function renderSettings(container) {
    const groqKey = getGroqKey();
    const maskedKey = groqKey ? groqKey.slice(0, 8) + '••••••••' + groqKey.slice(-4) : '';
    const hasKey = !!groqKey;

    container.innerHTML = `
    <div class="page-header">
        <div>
            <div class="page-title">Settings</div>
            <div class="page-meta">API KEYS • CONFIGURATION • SYSTEM STATUS</div>
        </div>
    </div>

    <!-- Groq API Key -->
    <div class="card mb-16">
        <div class="flex justify-between items-center mb-12">
            <div class="section-title" style="margin-bottom:0;">GROQ API KEY (AI ASSISTANT)</div>
            <div class="badge ${hasKey ? 'badge-green' : 'badge-red'}">
                ${hasKey ? '● CONNECTED' : '● NOT SET'}
            </div>
        </div>
        <p style="font-size:13px;color:var(--text-2);margin-bottom:14px;">
            Required for AI Assistant chatbot. Get a free key from
            <a href="https://console.groq.com/keys" target="_blank" style="color:var(--cyan);text-decoration:none;">console.groq.com/keys</a>
        </p>
        ${hasKey ? `<div style="font-size:12px;color:var(--text-3);margin-bottom:10px;font-family:'JetBrains Mono',monospace;">Current: ${maskedKey}</div>` : ''}
        <div class="flex gap-8">
            <input class="input" id="groqKeyInput" type="password" placeholder="Paste your Groq API key (gsk_...)" value="${groqKey}" style="flex:1;">
            <button class="btn btn-green" onclick="saveGroqKey()">
                <span class="material-icons-round" style="font-size:14px;">save</span> Save
            </button>
            ${hasKey ? `<button class="btn btn-red" onclick="clearGroqKey()">
                <span class="material-icons-round" style="font-size:14px;">delete</span> Clear
            </button>` : ''}
        </div>
        <div style="font-size:11px;color:var(--text-3);margin-top:10px;">
            <span class="material-icons-round" style="font-size:12px;vertical-align:middle;">lock</span>
            Key is stored in your browser's localStorage only — never sent to any server except Groq's API.
        </div>
    </div>

    <!-- Firebase Status -->
    <div class="card mb-16">
        <div class="flex justify-between items-center mb-12">
            <div class="section-title" style="margin-bottom:0;">FIREBASE</div>
            <div class="badge badge-green">● CONFIGURED</div>
        </div>
        <div style="font-size:13px;color:var(--text-2);line-height:2;">
            <div><span style="color:var(--text-3);width:120px;display:inline-block;">Project:</span> <span class="mono">resqsync-4feea</span></div>
            <div><span style="color:var(--text-3);width:120px;display:inline-block;">Firestore:</span> <span style="color:var(--green);">Enabled</span></div>
            <div><span style="color:var(--text-3);width:120px;display:inline-block;">Auth:</span> <span style="color:var(--green);">Anonymous</span></div>
        </div>
        <div style="font-size:11px;color:var(--text-3);margin-top:10px;">
            Firebase credentials are pre-configured. Enable Firestore + Anonymous Auth in
            <a href="https://console.firebase.google.com" target="_blank" style="color:var(--cyan);text-decoration:none;">Firebase Console</a>
            for real-time sync.
        </div>
    </div>

    <!-- Voice / Maps -->
    <div class="grid grid-2 mb-16">
        <div class="card">
            <div class="flex justify-between items-center mb-12">
                <div class="section-title" style="margin-bottom:0;">VOICE DETECTION</div>
                <div class="badge badge-green">● READY</div>
            </div>
            <div style="font-size:13px;color:var(--text-2);">
                Uses browser's built-in Web Speech API.<br>
                No API key needed. Works best in Chrome.
            </div>
        </div>
        <div class="card">
            <div class="flex justify-between items-center mb-12">
                <div class="section-title" style="margin-bottom:0;">MAPS</div>
                <div class="badge badge-green">● READY</div>
            </div>
            <div style="font-size:13px;color:var(--text-2);">
                Uses Leaflet.js + CartoDB Dark Tiles.<br>
                Free, no API key needed.
            </div>
        </div>
    </div>

    <!-- Quick Setup Guide -->
    <div class="card">
        <div class="section-title">QUICK SETUP GUIDE</div>
        <div style="font-size:13px;color:var(--text-2);line-height:2.2;">
            <div><span style="color:var(--green);">✅</span> <b>Step 1:</b> Open the app — works immediately with demo data</div>
            <div><span style="${hasKey ? 'color:var(--green)' : 'color:var(--orange)'};">${hasKey ? '✅' : '⏳'}</span> <b>Step 2:</b> Add Groq API key above for AI Assistant</div>
            <div><span style="color:var(--green);">✅</span> <b>Step 3:</b> Firebase is pre-configured (enable Firestore in console for live sync)</div>
            <div><span style="color:var(--green);">✅</span> <b>Step 4:</b> Voice & Maps work out of the box — no setup needed</div>
        </div>
    </div>`;
}

function saveGroqKey() {
    const key = document.getElementById('groqKeyInput').value.trim();
    if (!key) return showToast('Enter a valid API key', 'warning');
    if (!key.startsWith('gsk_')) return showToast('Groq keys start with gsk_', 'warning');
    setGroqKey(key);
    showToast('✅ Groq API key saved!', 'success');
    renderSettings(document.getElementById('mainContent'));
}

function clearGroqKey() {
    localStorage.removeItem('resqsync_groq_key');
    showToast('🗑️ Groq API key removed', 'info');
    renderSettings(document.getElementById('mainContent'));
}
