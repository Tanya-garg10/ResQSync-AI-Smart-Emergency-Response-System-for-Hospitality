# 🚨 ResQSync AI – Smart Emergency Response System for Hospitality

AI-powered emergency detection, classification, and coordinated response system for hotels, resorts, and large accommodation facilities.

Built with pure HTML/CSS/JS + Firebase + Groq AI + Leaflet Maps.

![Dark Command Center UI](https://img.shields.io/badge/UI-Dark_Command_Center-0a0e14?style=for-the-badge)
![Firebase](https://img.shields.io/badge/Firebase-Firestore_+_Auth-FFCA28?style=for-the-badge&logo=firebase)
![Groq AI](https://img.shields.io/badge/AI-Groq_Llama_3.3_70B-00C853?style=for-the-badge)
![Speech API](https://img.shields.io/badge/Voice-Web_Speech_API-4285F4?style=for-the-badge)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🆘 SOS Panic Button | One-tap emergency trigger with pulsing animation |
| 🎙️ Voice Detection | Real-time speech-to-text with English + Hindi support |
| 🧠 AI Classification | Auto-classify: Fire 🔥 Medical 🏥 Security 🚨 |
| ⚡ Severity Scoring | CRITICAL / PRIORITY / MODERATE / LOW |
| 🗺️ Live Tracking | Dark Leaflet map with responder ETA & routes |
| 📊 Admin Dashboard | Filter, manage, resolve incidents in real-time |
| 🤖 AI Assistant | Groq-powered chatbot for emergency guidance |
| 📈 Analytics | 30-day trends, donut charts, severity breakdown |
| 🚪 Evacuation Guide | Nearest exit + safety protocols per incident type |
| 🔥 Firebase Sync | Real-time Firestore read/write + anonymous auth |
| 🌐 Multi-Language | English & Hindi voice keyword detection |
| 📡 Offline Fallback | Works without API keys using built-in knowledge base |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Firebase Firestore + Authentication |
| AI Assistant | Groq API (Llama 3.3 70B Versatile) |
| Voice | Web Speech API (Chrome built-in) |
| Maps | Leaflet.js + CartoDB Dark Tiles |
| Icons | Google Material Icons |
| Fonts | Inter + JetBrains Mono |

---

## 📁 Project Structure

```
resqsync-ai/
├── index.html              # Main entry point
├── css/
│   └── style.css           # Dark command center theme
├── js/
│   ├── firebase-config.js  # Firebase init + Firestore CRUD
│   ├── data.js             # Data layer + demo incidents
│   ├── ai-engine.js        # AI classification + Groq API
│   ├── app.js              # Navigation + map helpers + toast
│   └── pages/
│       ├── monitoring.js   # Global Monitoring (command overview)
│       ├── sos.js          # SOS Panic Button
│       ├── voice.js        # Voice Detection
│       ├── tracking.js     # Live Tracking Map
│       ├── dashboard.js    # Admin Dashboard
│       ├── assistant.js    # AI Help Assistant
│       └── analytics.js    # Incident Analytics
└── data/
    └── sample_incidents.json
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Tanya-garg10/ResQSync-AI-Smart-Emergency-Response-System-for-Hospitality.git
cd ResQSync-AI-Smart-Emergency-Response-System-for-Hospitality
```

### 2. Add your Groq API Key (free)
- Go to [console.groq.com/keys](https://console.groq.com/keys) → Create free account → Generate API key
- Open `js/ai-engine.js` → Paste your key on line 7:
```js
const GROQ_API_KEY = 'gsk_your_key_here';
```

### 3. Run locally
```bash
# Any simple HTTP server works:
python -m http.server 8080
# OR
npx serve .
```

### 4. Open in browser
```
http://localhost:8080
```

That's it! The app works immediately with demo data. Firebase and Groq enhance it with real-time sync and AI responses.

---

## 🔧 Firebase Setup (Optional)

Firebase is pre-configured. To enable real-time data sync:

1. Go to [Firebase Console](https://console.firebase.google.com) → Project `resqsync-4feea`
2. **Firestore Database** → Create database → Start in test mode
3. **Authentication** → Sign-in method → Enable **Anonymous**

Incidents will now save/load from Firestore automatically.

---

## 📸 Pages Overview

| Page | What it does |
|------|-------------|
| 🌐 Global Monitoring | World map + health bars + intel stream + event log |
| 🆘 SOS Emergency | Big red panic button + evacuation guidance |
| 🎙️ Voice Detection | Microphone input + keyword detection + AI analysis |
| 🗺️ Live Tracking | Hotel map + responder markers + route lines |
| 📊 Dashboard | Metrics + filters + incident table + quick actions |
| 🤖 AI Assistant | Chat with Groq AI about emergency procedures |
| 📈 Analytics | Bar charts + line graphs + donut chart + severity bars |

---

## 🎯 Use Case

Designed for hackathons and demos — shows how AI can reduce emergency response time and improve coordination in hospitality settings.

**Demo-ready:** Works out of the box with zero configuration. Just open `index.html`.

---

## 📄 License

MIT
