/* ═══ Voice Detection – Google Speech-to-Text (Web Speech API) ═══ */

let recognition = null;
let isListening = false;

function renderVoice(container) {
    container.innerHTML = `
    <div class="page-header">
        <div>
            <div class="page-title">AI Voice Detection</div>
            <div class="page-meta">GOOGLE SPEECH-TO-TEXT • REAL-TIME KEYWORD DETECTION • ENGLISH + HINDI</div>
        </div>
    </div>

    <div class="grid grid-2">
        <div>
            <div class="section-title">VOICE INPUT</div>

            <!-- Mic Button -->
            <div class="flex gap-12 items-center mb-16">
                <button class="btn btn-red btn-lg" id="micBtn" onclick="toggleMic()">
                    <span class="material-icons-round" style="font-size:20px" id="micIcon">mic</span>
                    <span id="micLabel">Start Microphone</span>
                </button>
                <div>
                    <select class="select" id="voiceLang" style="width:auto;padding:8px 12px;">
                        <option value="en-US">🇬🇧 English</option>
                        <option value="hi-IN">🇮🇳 Hindi</option>
                    </select>
                </div>
                <span id="micStatus" class="mono" style="font-size:11px;color:var(--text-3);"></span>
            </div>

            <!-- Waveform indicator -->
            <div id="waveform" class="hidden" style="display:flex;align-items:center;justify-content:center;gap:3px;height:40px;margin-bottom:16px;">
                ${Array(20).fill(0).map((_, i) => `<div style="width:3px;background:var(--red);border-radius:2px;animation:wave 0.8s ease-in-out ${i * 0.05}s infinite alternate;"></div>`).join('')}
            </div>
            <style>@keyframes wave { from{height:4px;} to{height:${20 + Math.random() * 20}px;} }</style>

            <textarea class="textarea" id="voiceInput" rows="5" placeholder="Speak or type your emergency..."></textarea>

            <div class="section-title mt-20">QUICK TEST PHRASES</div>
            <div class="grid grid-2 gap-8">
                <button class="btn" onclick="setVoice('Help! There is a fire in the hotel lobby, smoke everywhere!')">🔥 Fire in lobby</button>
                <button class="btn" onclick="setVoice('Someone is unconscious and bleeding in room 201, need ambulance!')">🏥 Medical emergency</button>
                <button class="btn" onclick="setVoice('There is an intruder with a weapon near the parking area!')">🚨 Security threat</button>
                <button class="btn" onclick="setVoice('Bachao! Aag lag gayi hai, bahut dhua aa raha hai, madad chahiye!')">🇮🇳 Hindi: Aag!</button>
            </div>

            <button class="btn btn-cyan btn-full btn-lg mt-16" onclick="processVoice()">
                <span class="material-icons-round" style="font-size:16px">psychology</span> Process Voice Input
            </button>
        </div>

        <div>
            <div class="section-title">ANALYSIS OUTPUT</div>
            <div id="voiceResult">
                <div class="card text-center" style="padding:50px 20px;">
                    <span class="material-icons-round" style="font-size:56px;color:var(--text-3);">mic</span>
                    <div style="color:var(--text-2);margin-top:12px;">Click microphone or type, then process</div>
                    <div style="font-size:11px;color:var(--text-3);margin-top:8px;">Supports English & Hindi via Google Speech API</div>
                </div>
            </div>
        </div>
    </div>`;
}

function setVoice(text) { document.getElementById('voiceInput').value = text; }

function toggleMic() {
    if (isListening) { stopMic(); return; }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        showToast('Speech API not supported – use Chrome', 'warning');
        return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = document.getElementById('voiceLang').value;
    recognition.interimResults = true;
    recognition.continuous = true;

    const btn = document.getElementById('micBtn');
    const icon = document.getElementById('micIcon');
    const label = document.getElementById('micLabel');
    const status = document.getElementById('micStatus');
    const wave = document.getElementById('waveform');

    recognition.onstart = () => {
        isListening = true;
        btn.classList.add('mic-active');
        icon.textContent = 'stop';
        label.textContent = 'Stop';
        status.textContent = '🔴 LISTENING...';
        status.style.color = 'var(--red)';
        wave.classList.remove('hidden');
        wave.style.display = 'flex';
    };

    recognition.onresult = (e) => {
        let transcript = '';
        for (let i = 0; i < e.results.length; i++) {
            transcript += e.results[i][0].transcript;
        }
        document.getElementById('voiceInput').value = transcript;
    };

    recognition.onerror = (e) => {
        status.textContent = `❌ ${e.error}`;
        status.style.color = 'var(--red)';
        stopMic();
    };

    recognition.onend = () => { if (isListening) stopMic(); };
    recognition.start();
}

function stopMic() {
    if (recognition) recognition.stop();
    isListening = false;
    const btn = document.getElementById('micBtn');
    if (btn) {
        btn.classList.remove('mic-active');
        document.getElementById('micIcon').textContent = 'mic';
        document.getElementById('micLabel').textContent = 'Start Microphone';
        document.getElementById('micStatus').textContent = '✅ Captured';
        document.getElementById('micStatus').style.color = 'var(--green)';
        const wave = document.getElementById('waveform');
        if (wave) { wave.classList.add('hidden'); wave.style.display = 'none'; }
    }
}

function processVoice() {
    const text = document.getElementById('voiceInput').value;
    if (!text.trim()) return showToast('Speak or type something first', 'warning');

    const voice = AIEngine.detectKeywords(text);
    const lang = AIEngine.detectLang(text);
    const ai = AIEngine.fullAnalysis(text);
    const sc = severityColor(ai.severity);

    const isE = voice.isEmergency;
    const eBg = isE ? 'var(--red-glow)' : 'var(--green-glow)';
    const eBorder = isE ? 'rgba(239,68,68,0.25)' : 'rgba(34,197,94,0.25)';
    const eIcon = isE ? 'emergency' : 'check_circle';
    const eText = isE ? 'EMERGENCY DETECTED' : 'NO EMERGENCY DETECTED';
    const eColor = isE ? 'var(--red)' : 'var(--green)';

    document.getElementById('voiceResult').innerHTML = `
    <div style="background:${eBg};border:1px solid ${eBorder};border-radius:var(--radius);padding:18px;text-align:center;margin-bottom:14px;">
        <span class="material-icons-round" style="font-size:28px;color:${eColor};">${eIcon}</span>
        <div style="font-size:16px;font-weight:700;color:${eColor};margin-top:6px;">${eText}</div>
    </div>

    <div class="card mb-12">
        <div class="section-title">VOICE ANALYSIS</div>
        <div class="grid grid-2">
            <div><div style="font-size:10px;color:var(--text-3);">LANGUAGE</div><div style="font-size:15px;font-weight:600;color:var(--cyan);margin-top:4px;">${lang.name}</div></div>
            <div><div style="font-size:10px;color:var(--text-3);">KEYWORDS FOUND</div><div style="font-size:15px;font-weight:600;color:var(--orange);margin-top:4px;">${voice.count}</div></div>
        </div>
        <div class="mt-12">
            <div style="font-size:10px;color:var(--text-3);">DETECTED KEYWORDS</div>
            <div class="mt-8 flex flex-wrap gap-8">${voice.keywords.map(k => `<span class="tag tag-red">${k}</span>`).join('') || '<span class="text-muted">None</span>'}</div>
        </div>
    </div>

    <div class="card" style="border-left:3px solid ${sc};">
        <div class="section-title">AI CLASSIFICATION</div>
        <div class="grid grid-3">
            <div><div style="font-size:10px;color:var(--text-3);">TYPE</div><div style="font-size:20px;font-weight:700;margin-top:4px;">${incidentIcon(ai.type)} ${ai.type}</div></div>
            <div><div style="font-size:10px;color:var(--text-3);">SEVERITY</div><div style="font-size:20px;font-weight:700;color:${sc};margin-top:4px;">${ai.severity}</div></div>
            <div><div style="font-size:10px;color:var(--text-3);">CONFIDENCE</div><div style="font-size:20px;font-weight:700;color:var(--cyan);margin-top:4px;">${Math.round(ai.confidence * 100)}%</div></div>
        </div>
    </div>`;

    if (isE) showToast('🚨 Emergency keywords detected!', 'danger');
}
