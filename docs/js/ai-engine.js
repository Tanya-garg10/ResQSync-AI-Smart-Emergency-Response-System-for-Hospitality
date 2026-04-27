/* ═══════════════════════════════════════════
   AI Engine – Classification + Groq AI Assistant
   ═══════════════════════════════════════════ */

// 🔑 Groq API Key – loaded from localStorage (user enters via Settings)
function getGroqKey() {
    return localStorage.getItem('resqsync_groq_key') || '';
}
function setGroqKey(key) {
    localStorage.setItem('resqsync_groq_key', key);
}

const KEYWORDS = {
    FIRE: ['fire', 'smoke', 'burning', 'flames', 'aag', 'jalana', 'dhua', 'jal'],
    MEDICAL: ['medical', 'heart', 'bleeding', 'unconscious', 'pain', 'doctor', 'ambulance', 'dard', 'tabiyat', 'bimaari', 'hurt', 'injured'],
    SECURITY: ['security', 'theft', 'attack', 'intruder', 'weapon', 'gun', 'threat', 'chor', 'hamla', 'khatra', 'robbery', 'suspicious'],
};

const SEV_WEIGHTS = {
    fire: 0.9, smoke: 0.7, burning: 0.95, flames: 0.95,
    heart: 0.9, bleeding: 0.85, unconscious: 0.95, pain: 0.5,
    attack: 0.9, weapon: 0.95, gun: 0.95, intruder: 0.8,
    theft: 0.6, help: 0.5, emergency: 0.7, bomb: 0.99,
};

const KW_EN = ['help', 'fire', 'emergency', 'ambulance', 'police', 'attack', 'bleeding', 'smoke', 'danger', 'save', 'sos', 'bomb', 'gun'];
const KW_HI = ['bachao', 'madad', 'aag', 'emergency', 'police', 'hamla', 'khoon', 'dhua', 'khatra', 'doctor', 'bomb', 'bandook'];
const ALL_KW = [...new Set([...KW_EN, ...KW_HI])];

const AIEngine = {
    classify(text) {
        const l = text.toLowerCase();
        const scores = {};
        for (const [type, kws] of Object.entries(KEYWORDS)) {
            const s = kws.filter(k => l.includes(k)).length;
            if (s > 0) scores[type] = s;
        }
        if (!Object.keys(scores).length) {
            if (['help', 'emergency', 'bachao', 'madad', 'sos'].some(w => l.includes(w)))
                return { type: 'SECURITY', confidence: 0.6 };
            return { type: 'UNKNOWN', confidence: 0 };
        }
        const best = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];
        return { type: best[0], confidence: Math.min(best[1] / 3, 1) };
    },

    severity(text) {
        const l = text.toLowerCase();
        let maxW = 0; const matched = [];
        for (const [w, wt] of Object.entries(SEV_WEIGHTS)) {
            if (l.includes(w)) { matched.push(w); maxW = Math.max(maxW, wt); }
        }
        let level = 'LOW';
        if (maxW >= 0.85) level = 'CRITICAL';
        else if (maxW >= 0.65) level = 'PRIORITY';
        else if (maxW >= 0.4) level = 'MODERATE';
        return { level, score: maxW, keywords: matched };
    },

    fullAnalysis(text) {
        const c = this.classify(text);
        const s = this.severity(text);
        return { text, type: c.type, confidence: c.confidence, severity: s.level, severityScore: s.score, keywords: s.keywords };
    },

    detectKeywords(text) {
        const l = text.toLowerCase();
        const found = ALL_KW.filter(k => l.includes(k));
        return { isEmergency: found.length > 0, keywords: found, count: found.length };
    },

    detectLang(text) {
        return KW_HI.some(w => text.toLowerCase().includes(w)) ? { code: 'hi', name: 'Hindi' } : { code: 'en', name: 'English' };
    },

    // ── Groq API for AI Assistant (Free + Ultra Fast) ──
    async askGemini(question) {
        try {
            if (!getGroqKey()) {
                console.warn('Groq API key not set, using offline mode');
                return this.getOfflineResponse(question);
            }

            const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getGroqKey()}`,
                },
                body: JSON.stringify({
                    model: 'llama-3.3-70b-versatile',
                    messages: [
                        {
                            role: 'system',
                            content: `You are ResQSync AI, an emergency response assistant for hotels and hospitality.
You help with fire safety, medical emergencies, security threats, evacuation procedures, and first aid.
Keep answers concise, actionable, and formatted with bullet points.
If the question is not about emergencies or safety, politely redirect to emergency topics.
Always respond in the same language the user asks in.`
                        },
                        {
                            role: 'user',
                            content: question
                        }
                    ],
                    temperature: 0.7,
                    max_tokens: 500,
                })
            });

            if (!res.ok) throw new Error(`Groq API ${res.status}`);
            const data = await res.json();
            const text = data.choices?.[0]?.message?.content;
            return text || this.getOfflineResponse(question);
        } catch (e) {
            console.warn('Groq API error:', e.message);
            return this.getOfflineResponse(question);
        }
    },

    // Offline fallback
    getOfflineResponse(q) {
        const l = q.toLowerCase();
        if (['fire', 'smoke', 'burning', 'aag'].some(w => l.includes(w)))
            return '🔥 **FIRE SAFETY:**\n• Pull fire alarm & call emergency\n• Evacuate via stairs, NOT elevators\n• Stay low below smoke\n• Close doors behind you\n• Stop, Drop, Roll if clothes catch fire\n• Go to assembly point\n• Do NOT re-enter building';
        if (['medical', 'hurt', 'bleeding', 'unconscious', 'heart', 'cpr', 'first aid'].some(w => l.includes(w)))
            return '🏥 **MEDICAL EMERGENCY:**\n• Check scene safety\n• Call for help / ambulance\n• Check responsiveness\n• Open airway (tilt head, lift chin)\n• CPR: 30 compressions, 2 breaths\n• Apply pressure to bleeding\n• Do NOT move patient unless in danger';
        if (['security', 'threat', 'intruder', 'weapon', 'attack'].some(w => l.includes(w)))
            return '🚨 **SECURITY THREAT – RUN HIDE FIGHT:**\n• RUN: Escape if safe path exists\n• HIDE: Lock door, barricade, silence phone\n• FIGHT: Last resort, act with aggression\n• Call security/police when safe';
        return '⚠️ **GENERAL EMERGENCY:**\n• Stay calm, assess situation\n• Call for help (staff/emergency)\n• Follow evacuation signs\n• Help others if safe\n• Go to assembly point\n• Wait for all-clear\n\n📞 Hotel Security: Ext 100 | Emergency: 112';
    }
};
