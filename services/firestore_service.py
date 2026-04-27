"""
Firestore Service – CRUD operations for incidents, users, analytics.
Falls back to session_state in demo mode.
"""
import streamlit as st
from datetime import datetime
from config.firebase_config import init_firebase, DEMO_MODE
from utils.helpers import generate_demo_incidents


def _get_db():
    """Get Firestore client."""
    return init_firebase()


# ═══════════════════════════════════════════
#  INCIDENTS
# ═══════════════════════════════════════════

def save_incident(incident: dict) -> bool:
    """Save incident to Firestore (or session_state in demo)."""
    incident["created_at"] = datetime.now().isoformat()
    db = _get_db()

    if db:
        try:
            db.collection("incidents").document(
                str(incident["id"])
            ).set(incident)
            return True
        except Exception as e:
            st.error(f"Firestore write failed: {e}")

    # Demo fallback
    if "incidents" not in st.session_state:
        st.session_state.incidents = []
    st.session_state.incidents.insert(0, incident)
    return True


def get_incidents(limit: int = 50) -> list:
    """Fetch incidents from Firestore or session_state."""
    db = _get_db()

    if db:
        try:
            docs = (
                db.collection("incidents")
                .order_by("created_at", direction="DESCENDING")
                .limit(limit)
                .stream()
            )
            return [doc.to_dict() for doc in docs]
        except Exception:
            pass

    # Demo fallback
    if "incidents" not in st.session_state:
        st.session_state.incidents = generate_demo_incidents(8)
    return st.session_state.incidents


def update_incident_status(incident_id, new_status: str) -> bool:
    """Update incident status."""
    db = _get_db()

    if db:
        try:
            db.collection("incidents").document(
                str(incident_id)
            ).update({"status": new_status})
            return True
        except Exception:
            pass

    # Demo fallback
    for inc in st.session_state.get("incidents", []):
        if str(inc.get("id")) == str(incident_id):
            inc["status"] = new_status
            return True
    return False
