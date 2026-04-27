# 🚨 ResQSync AI – Smart Emergency Response System for Hospitality

AI-powered emergency detection, classification, and coordinated response system for hotels, resorts, and large accommodation facilities.

## Features

- **SOS Panic Button** – One-tap emergency trigger with instant alert
- **AI Voice Detection** – Detect keywords like "help", "fire", "emergency" via speech-to-text
- **Smart Emergency Classification** – Fire 🔥 | Medical 🏥 | Security 🚨
- **AI Severity Scoring** – High / Medium / Low priority
- **Real-Time Location Tracking** – Map-based incident visualization
- **Instant Alerts** – Push notifications + SMS fallback
- **Live Responder Tracking** – ETA and status display
- **Admin Dashboard** – Active emergencies, coordination, analytics
- **Auto-Evacuation Guidance** – Nearest exit + safe route
- **Offline Emergency Mode** – SMS fallback when no internet
- **Multi-Language Support** – English & Hindi voice commands
- **AI Help Assistant** – Emergency guidance chatbot
- **Incident Logging & Analytics** – Response time trends
- **Role-Based Access** – Guest / Staff / Admin views

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (Web App) |
| Backend | Firebase (Firestore, Auth, Cloud Messaging) |
| AI | Google Speech-to-Text, Vertex AI, Gemini |
| Maps | Folium + OpenStreetMap |
| Notifications | Firebase Cloud Messaging + Twilio SMS |
| Dashboard | Streamlit with Plotly charts |

## Project Structure


```
resqsync-ai/
├── app.py                  # Main Streamlit app (entry point)
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit theme config
├── config/
│   └── firebase_config.py  # Firebase initialization
├── pages/
│   ├── 1_🆘_SOS.py         # SOS Panic Button page
│   ├── 2_🎙️_Voice.py       # AI Voice Detection page
│   ├── 3_🗺️_Tracking.py    # Live Map Tracking page
│   ├── 4_📊_Dashboard.py   # Admin Dashboard page
│   ├── 5_🤖_Assistant.py   # AI Help Assistant page
│   └── 6_📈_Analytics.py   # Incident Analytics page
├── services/
│   ├── ai_classifier.py    # Emergency classification + severity
│   ├── alert_service.py    # Notifications (FCM + SMS)
│   ├── location_service.py # Location tracking utilities
│   ├── voice_service.py    # Speech-to-text processing
│   └── evacuation.py       # Evacuation route logic
├── utils/
│   ├── auth.py             # Role-based authentication
│   └── helpers.py          # Common utility functions
├── data/
│   └── sample_incidents.json # Demo data for hackathon
└── assets/
    └── logo.png            # App logo
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Firebase
- Firebase project `resqsync-4feea` is already configured
- For Firestore server-side access: download service account key from Firebase Console → Project Settings → Service Accounts
- Save as `config/serviceAccountKey.json`
- Enable Firestore Database, Authentication, and Cloud Messaging in Firebase Console

### 3. Set Environment Variables
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
export TWILIO_ACCOUNT_SID="your-twilio-sid"
export TWILIO_AUTH_TOKEN="your-twilio-token"
export TWILIO_PHONE="your-twilio-phone"
```

### 4. Run the App
```bash
streamlit run app.py
```

### 5. Demo Mode
The app works in demo mode without Firebase — perfect for hackathon presentations.

## Deployment

### Streamlit Cloud
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect repo and deploy

### Firebase Hosting (optional)
```bash
firebase init hosting
firebase deploy
```

## License
MIT
