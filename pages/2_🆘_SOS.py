"""
SOS Panic Button – One-tap emergency trigger
"""
import streamlit as st
import time
from datetime import datetime
from services.ai_classifier import full_analysis
from services.alert_service import trigger_alert
from services.evacuation import get_evacuation_plan
from services.firestore_service import save_incident
from utils.helpers import generate_incident_id, generate_node_id, incident_icon, severity_color

st.set_page_config(page_title="SOS | ResQSync AI", page_icon="🆘", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align:center;padding:10px 0 20px 0;">
    <div style="font-size:22px;font-weight:700;color:#e8edf5;">Emergency SOS</div>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">ONE-TAP EMERGENCY TRIGGER</div>
</div>
""", unsafe_allow_html=True)

# ── SOS Button ──
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("""
    <div style="display:flex;justify-content:center;padding:20px 0;">
        <div style="width:200px;height:200px;border-radius:50%;
            background:radial-gradient(circle,#ff4b4b 0%,#cc0000 70%,#990000 100%);
            border:4px solid rgba(255,75,75,0.4);color:white;font-size:36px;font-weight:800;
            display:flex;align-items:center;justify-content:center;
            box-shadow:0 0 40px rgba(255,75,75,0.3),0 0 80px rgba(255,75,75,0.1);
            animation:sos-pulse 2s infinite;letter-spacing:3px;">
            SOS
        </div>
    </div>
    <style>
    @keyframes sos-pulse {
        0%,100% { box-shadow:0 0 40px rgba(255,75,75,0.3);transform:scale(1); }
        50% { box-shadow:0 0 60px rgba(255,75,75,0.5);transform:scale(1.03); }
    }
    </style>
    """, unsafe_allow_html=True)

    # Actual trigger buttons
    sos_type = st.selectbox("Emergency Type", ["🔥 FIRE", "🏥 MEDICAL", "🚨 SECURITY"], label_visibility="collapsed")

    if st.button("🚨 TRIGGER SOS ALERT", use_container_width=True, type="primary"):
        etype = sos_type.split(" ")[1]
        inc_id = generate_incident_id()
        zone = generate_node_id()

        with st.spinner("⚡ Activating emergency protocol..."):
            time.sleep(1)

        # Create incident
        incident = {
            "id": inc_id,
            "type": etype,
            "zone": zone,
            "severity": "CRITICAL",
            "status": "ACTIVE",
            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
        }

        # Trigger alerts
        alerts = trigger_alert(incident)

        # Save to Firestore
        save_incident(incident)

        # Add to session
        if "incidents" not in st.session_state:
            st.session_state.incidents = []
        st.session_state.incidents.insert(0, incident)

        # Show confirmation
        st.markdown(f"""
        <div style="background:rgba(255,75,75,0.1);border:1px solid rgba(255,75,75,0.3);border-radius:8px;padding:20px;margin-top:16px;text-align:center;">
            <div style="font-size:24px;margin-bottom:8px;">🚨</div>
            <div style="font-size:16px;font-weight:700;color:#ff4b4b;">ALERT ACTIVATED</div>
            <div style="font-size:12px;color:#7a8ba8;margin-top:8px;font-family:'JetBrains Mono',monospace;">
                ID: {inc_id} | Type: {etype} | Zone: {zone}<br>
                Severity: CRITICAL | Status: ACTIVE
            </div>
            <div style="font-size:11px;color:#00c853;margin-top:12px;">
                ✅ {len(alerts)} notifications dispatched
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Evacuation guidance
        plan = get_evacuation_plan(etype, 28.6139, 77.2090)
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:16px;margin-top:12px;">
            <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">
                EVACUATION GUIDANCE
            </div>
            <div style="font-size:13px;color:#e8edf5;">
                🚪 Nearest Exit: <span style="color:#00bfff;font-weight:600;">{plan['nearest_exit']['name']}</span>
            </div>
            <div style="font-size:13px;color:#e8edf5;margin-top:4px;">
                📍 Assembly: <span style="color:#00c853;">{plan['assembly_point']}</span>
            </div>
            <div style="margin-top:10px;font-size:12px;color:#7a8ba8;">
                {'<br>'.join(plan['instructions'][:4])}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Quick Description Input ──
st.markdown("---")
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">DESCRIBE EMERGENCY (OPTIONAL)</div>', unsafe_allow_html=True)

desc = st.text_area("Describe what's happening...", height=80, label_visibility="collapsed",
                     placeholder="e.g., Fire in kitchen, someone is unconscious in lobby...")

if desc and st.button("🔍 Analyze & Alert", use_container_width=True):
    analysis = full_analysis(desc)
    sev_col = severity_color(analysis["severity"])

    st.markdown(f"""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-left:3px solid {sev_col};border-radius:8px;padding:16px;margin-top:12px;">
        <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">
            AI ANALYSIS RESULT
        </div>
        <div style="display:flex;gap:20px;flex-wrap:wrap;">
            <div>
                <div style="font-size:10px;color:#7a8ba8;">TYPE</div>
                <div style="font-size:16px;font-weight:700;color:#e8edf5;">{incident_icon(analysis['type'])} {analysis['type']}</div>
            </div>
            <div>
                <div style="font-size:10px;color:#7a8ba8;">SEVERITY</div>
                <div style="font-size:16px;font-weight:700;color:{sev_col};">{analysis['severity']}</div>
            </div>
            <div>
                <div style="font-size:10px;color:#7a8ba8;">CONFIDENCE</div>
                <div style="font-size:16px;font-weight:700;color:#00bfff;">{int(analysis['confidence']*100)}%</div>
            </div>
            <div>
                <div style="font-size:10px;color:#7a8ba8;">KEYWORDS</div>
                <div style="font-size:12px;color:#e8edf5;">{', '.join(analysis['keywords_detected']) or 'None'}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
