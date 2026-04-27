/* ═══ AI Assistant – Gemini Powered ═══ */

let chatHistory = [
    { role: 'bot', text: '🤖 I\'m <b>ResQSync AI Assistant</b>, powered by Groq AI (Llama 3.3 70B).<br><br>Ask me about fire safety, medical emergencies, security threats, evacuation procedures, or first aid. Ultra-fast responses.', time: timestamp() }
];

function renderAssistant(container) {
    let chatHTML = chatHistory.map(m => `
        <div class="chat-msg ${m.role === 'user' ? 'user' : 'bot'}">
            <div class="chat-bubble">
                <div>${m.text}</div>
                <div class="chat-time">${m.time}</div>
            </div>
        </div>`).join('');

    container.innerHTML = `
    <div class="page-header">
        <div>
            <div class="page-title">AI Help Assistant</div>
            <div class="page-meta">POWERED BY GROQ AI (LLAMA 3.3 70B) • EMERGENCY GUIDANCE • ULTRA FAST</div>
        </div>
        <div class="badge badge-blue">
            <span class="material-icons-round" style="font-size:14px;">auto_awesome</span> GROQ AI
        </div>
    </div>

    <div class="chat-container" id="chatBox">${chatHTML}</div>

    <div class="section-title mt-16">QUICK QUESTIONS</div>
    <div class="grid grid-4 gap-8 mb-16">
        <button class="btn" onclick="askBot('What should I do in case of fire in a hotel?')">
            <span style="font-size:16px;">🔥</span> Fire safety
        </button>
        <button class="btn" onclick="askBot('How to handle a medical emergency? Give first aid steps.')">
            <span style="font-size:16px;">🏥</span> First aid
        </button>
        <button class="btn" onclick="askBot('What to do during an active security threat in a hotel?')">
            <span style="font-size:16px;">🚨</span> Security threat
        </button>
        <button class="btn" onclick="askBot('What is the evacuation procedure for a hotel during earthquake?')">
            <span style="font-size:16px;">🌍</span> Earthquake
        </button>
    </div>

    <div class="flex gap-8">
        <input class="input" id="chatInput" placeholder="Ask about any emergency procedure..." onkeydown="if(event.key==='Enter')sendChat()">
        <button class="btn btn-cyan btn-lg" onclick="sendChat()">
            <span class="material-icons-round" style="font-size:16px;">send</span> Send
        </button>
    </div>`;

    setTimeout(() => {
        const box = document.getElementById('chatBox');
        if (box) box.scrollTop = box.scrollHeight;
    }, 50);
}

async function askBot(text) {
    const now = timestamp();
    chatHistory.push({ role: 'user', text, time: now });

    // Show typing indicator
    chatHistory.push({ role: 'bot', text: '<span class="text-muted"><span class="material-icons-round" style="font-size:14px;vertical-align:middle;animation:spin 1s linear infinite;">autorenew</span> Thinking...</span>', time: now });
    renderAssistant(document.getElementById('mainContent'));

    // Call Gemini
    const response = await AIEngine.askGemini(text);

    // Replace typing with response
    chatHistory.pop();
    // Format markdown-like response
    const formatted = response
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
        .replace(/\*(.*?)\*/g, '<i>$1</i>')
        .replace(/\n/g, '<br>')
        .replace(/•/g, '&bull;');

    chatHistory.push({ role: 'bot', text: formatted, time: timestamp() });
    renderAssistant(document.getElementById('mainContent'));

    // Log to Firebase
    FireDB.logEvent('assistant_query', { question: text });
}

function sendChat() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;
    askBot(text);
}

// Spin animation for loading
const spinStyle = document.createElement('style');
spinStyle.textContent = '@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}';
document.head.appendChild(spinStyle);
