"""
Firebase Configuration – ResQSync AI
Real Firebase credentials integrated.
"""
import os
import streamlit as st

# ── Firebase Web Config ──
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyBWtjzd0NGiaCzmzrntQkQIe51OZlj8jFs",
    "authDomain": "resqsync-4feea.firebaseapp.com",
    "projectId": "resqsync-4feea",
    "storageBucket": "resqsync-4feea.firebasestorage.app",
    "messagingSenderId": "644169883094",
    "appId": "1:644169883094:web:9461036e6ccc4cf937d877",
    "measurementId": "G-KKD6Q95M63",
}

# Demo mode toggle – set to False when Firebase Admin SDK is configured
DEMO_MODE = os.getenv("RESQSYNC_DEMO", "true").lower() == "true"

_firestore_client = None
_firebase_initialized = False


def init_firebase():
    """Initialize Firebase Admin SDK (for server-side Firestore access)."""
    global _firebase_initialized, _firestore_client
    if _firebase_initialized:
        return _firestore_client

    if DEMO_MODE:
        _firebase_initialized = True
        return None

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        if not firebase_admin._apps:
            # Option 1: Service account JSON file
            sa_path = os.getenv(
                "GOOGLE_APPLICATION_CREDENTIALS",
                "config/serviceAccountKey.json",
            )
            if os.path.exists(sa_path):
                cred = credentials.Certificate(sa_path)
                firebase_admin.initialize_app(cred)
            else:
                # Option 2: Default credentials (Cloud Run, etc.)
                firebase_admin.initialize_app()

        _firestore_client = firestore.client()
        _firebase_initialized = True
        return _firestore_client
    except Exception as e:
        st.warning(f"Firebase init failed, running in demo mode: {e}")
        _firebase_initialized = True
        return None
