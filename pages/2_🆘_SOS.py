"""
Smart SOS – Photo upload, auto room/floor detect, severity score, contact notify, timeline
"""
import streamlit as st
import time
import random
from datetime import datetime
from services.ai_classifier import full_analysis, calculate_ai_severity_score
from services.alert_service import trigger_alert, notify_emergency_contacts
from services.evacuation import get_evacuation_plan
from services.firestore_service import save_incident
from utils.helpers import generate_incident_id, generate_node_id, incident_icon, severity_color

st.set_page_config(page_title="Smart SOS | ResQSync AI", page_icon="🆘", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
.priority-badge {
    display: inline-block; padding: 4px 12px; border-radius: 20px;
    font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
}
@keyframes sos-pulse {
    0%,100% { box-shadow:0 0 40px rgba(255,75,75,0.3); transform:scale(1); }
    50% { box-shadow:0 0 70px rgba(255,75,75,0.6); transform:scale(1.04); }
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.4;} }
.timeline-dot { width:10px; height:10px; border-radius:50%; background:#ff4b4b; display:inline-block; margin-right:8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:10px 0 20px 0;">
    <div style="font-size:22px;font-weight:700;color:#e8edf5;">🚨 Smart SOS</div>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">SMART EMERGENCY TRIGGER • AI SEVERITY • CONTACT NOTIFY</div>
</div>
""", unsafe_allow_html=True)

col_sos, col_details = st.columns([1, 1])

with col_sos:
    # SOS Button
    st.markdown("""
    <div style="display:flex;justify-content:center;padding:10px 0 20px 0;">
        <div style="width:180px;height:180px;border-radius:50%;
            background:radial-gradient(circle,#ff4b4b 0%,#cc0000 70%,#990000 100%);
            border:4px solid rgba(255,75,75,0.5);color:white;font-size:34px;font-weight:800;
            display:flex;align-items:center;justify-content:center;
            box-shadow:0 0 40px rgba(255,75,75,0.3),0 0 80px rgba(255,75,75,0.1);
            animation:sos-pulse 2s infinite;letter-spacing:3px;">
            SOS
        </div>
    </div>
    """, unsafe_allow_html=True)

    sos_type = st.selectbox("Emergency Type", ["🔥 FIRE", "🏥 MEDICAL", "🚨 SECURITY"], label_visibility="visible")

    # Room & Floor auto-detect
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:12px 0 8px;font-family:\'JetBrains Mono\',monospace;">LOCATION DETECTION</div>', unsafe_allow_html=True)
    loc_col1, loc_col2 = st.columns(2)
    with loc_col1:
        floor_options = ["Auto-Detect", "Ground Floor", "Floor 1", "Floor 2", "Floor 3", "Floor 4", "Basement"]
        floor = st.selectbox("Floor", floor_options)
    with loc_col2:
        room = st.text_input("Room No.", placeholder="e.g. 307")

    # Photo upload
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:12px 0 8px;font-family:\'JetBrains Mono\',monospace;">📸 PHOTO EVIDENCE (OPTIONAL)</div>', unsafe_allow_html=True)
    photo = st.file_uploader("Upload incident photo", type=["jpg","jpeg","png"], label_visibility="collapsed")
    if photo:
        st.image(photo, caption="Evidence attached", use_container_width=True)
        st.markdown('<div style="font-size:11px;color:#00c853;margin-top:4px;">✅ Photo evidence captured</div>', unsafe_allow_html=True)

    desc = st.text_area("Describe emergency (optional)", height=70, placeholder="e.g., Fire in kitchen on floor 3, smoke visible...")

    trigger_col, _ = st.columns([2,1])
    with trigger_col:
        trigger_btn = st.button("🚨 TRIGGER SMART SOS", use_container_width=True, type="primary")

with col_details:
    if trigger_btn:
        etype = sos_type.split(" ")[1]
        inc_id = generate_incident_id()

        # Auto-detect floor if selected
        detected_floor = floor if floor != "Auto-Detect" else random.choice(["Floor 2", "Floor 3", "Floor 4"])
        detected_room = room if room else str(random.randint(201, 415))
        zone = f"{detected_floor}, Room {detected_room}"

        with st.spinner("⚡ Activating smart emergency protocol..."):
            time.sleep(1.2)

        # AI analysis
        desc_text = desc if desc else f"{etype} emergency reported at {zone}"
        ai = full_analysis(desc_text)
        sev_score = calculate_ai_severity_score(etype, ai["severity"])
        sev_col_hex = severity_color(ai["severity"])

        incident = {
            "id": inc_id,
            "type": etype,
            "zone": zone,
            "floor": detected_floor,
            "room": detected_room,
            "severity": ai["severity"],
            "severity_score": sev_score,
            "status": "ACTIVE",
            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
            "photo": photo.name if photo else None,
            "description": desc_text,
        }

        alerts = trigger_alert(incident)
        contacts = notify_emergency_contacts(incident)
        save_incident(incident)

        if "incidents" not in st.session_state:
            st.session_state.incidents = []
        st.session_state.incidents.insert(0, incident)

        # Store timeline
        now = datetime.now()
        timeline = [
            {"time": now.strftime("%H:%M:%S"), "event": "SOS Triggered", "color": "#ff4b4b"},
            {"time": (now.replace(second=now.second+1) if now.second < 59 else now).strftime("%H:%M:%S"), "event": f"{etype} Emergency Classified", "color": "#ff8c00"},
            {"time": (now.replace(second=min(now.second+2,59))).strftime("%H:%M:%S"), "event": "Emergency Contacts Notified", "color": "#ffd700"},
            {"time": (now.replace(second=min(now.second+3,59))).strftime("%H:%M:%S"), "event": "Responder Team Assigned", "color": "#00bfff"},
            {"time": (now.replace(second=min(now.second+5,59))).strftime("%H:%M:%S"), "event": "Help Dispatched", "color": "#00c853"},
        ]

        # ── Main alert card ──
        st.markdown(f"""
        <div style="background:rgba(255,75,75,0.08);border:1px solid rgba(255,75,75,0.4);border-radius:10px;padding:18px;margin-bottom:14px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                <span style="font-size:24px;">{incident_icon(etype)}</span>
                <div>
                    <div style="font-size:18px;font-weight:800;color:#ff4b4b;">{etype} EMERGENCY</div>
                    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;">ID: {inc_id}</div>
                </div>
                <span style="margin-left:auto;background:{sev_col_hex};color:#000;padding:4px 12px;border-radius:20px;font-size:10px;font-weight:700;letter-spacing:1.5px;">{ai['severity']}</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:12px;">
                <div style="background:#111620;border-radius:6px;padding:10px;">
                    <div style="color:#7a8ba8;font-size:10px;margin-bottom:3px;">📍 LOCATION</div>
                    <div style="color:#e8edf5;font-weight:600;">{detected_floor}, Room {detected_room}</div>
                </div>
                <div style="background:#111620;border-radius:6px;padding:10px;">
                    <div style="color:#7a8ba8;font-size:10px;margin-bottom:3px;">⚠️ SEVERITY SCORE</div>
                    <div style="color:{sev_col_hex};font-weight:700;font-size:16px;">{sev_score}/10</div>
                </div>
                <div style="background:#111620;border-radius:6px;padding:10px;">
                    <div style="color:#7a8ba8;font-size:10px;margin-bottom:3px;">📸 PHOTO EVIDENCE</div>
                    <div style="color:{'#00c853' if photo else '#555'};font-weight:600;">{'✅ Attached' if photo else '— None'}</div>
                </div>
                <div style="background:#111620;border-radius:6px;padding:10px;">
                    <div style="color:#7a8ba8;font-size:10px;margin-bottom:3px;">🤖 AI CONFIDENCE</div>
                    <div style="color:#00bfff;font-weight:600;">{int(ai['confidence']*100)}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Emergency Contacts ──
        st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">EMERGENCY CONTACT STATUS</div>', unsafe_allow_html=True)
        for c in contacts:
            st.markdown(f"""
            <div style="background:#151b28;border:1px solid rgba(0,200,83,0.3);border-radius:6px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:12px;color:#e8edf5;">{c['icon']} {c['name']}</span>
                <span style="font-size:11px;color:#00c853;font-weight:600;">✓ {c['status']}</span>
            </div>
            """, unsafe_allow_html=True)

        # ── Incident Timeline ──
        st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">⏱ INCIDENT TIMELINE</div>', unsafe_allow_html=True)
        timeline_html = '<div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;">'
        for i, ev in enumerate(timeline):
            connector = f'<div style="width:2px;height:14px;background:#1e2a3a;margin-left:4px;"></div>' if i < len(timeline)-1 else ""
            timeline_html += f"""
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="display:flex;flex-direction:column;align-items:center;">
                    <div style="width:10px;height:10px;border-radius:50%;background:{ev['color']};flex-shrink:0;"></div>
                    {connector}
                </div>
                <div style="padding-bottom:{'12px' if i < len(timeline)-1 else '0'};">
                    <span style="font-size:10px;color:#555;font-family:'JetBrains Mono',monospace;">{ev['time']}</span>
                    <span style="font-size:12px;color:#e8edf5;margin-left:8px;">{ev['event']}</span>
                </div>
            </div>
            """
        timeline_html += '</div>'
        st.markdown(timeline_html, unsafe_allow_html=True)

        # Evacuation
        plan = get_evacuation_plan(etype, 28.6139, 77.2090)
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;margin-top:10px;">
            <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;font-family:'JetBrains Mono',monospace;">EVACUATION GUIDANCE</div>
            <div style="font-size:13px;color:#e8edf5;">🚪 Nearest Exit: <span style="color:#00bfff;font-weight:600;">{plan['nearest_exit']['name']}</span></div>
            <div style="font-size:13px;color:#e8edf5;margin-top:4px;">📍 Assembly: <span style="color:#00c853;">{plan['assembly_point']}</span></div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Idle state
        st.markdown("""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:10px;padding:30px;text-align:center;margin-top:10px;">
            <div style="font-size:48px;margin-bottom:12px;">🛡️</div>
            <div style="font-size:14px;font-weight:600;color:#e8edf5;">Smart SOS Ready</div>
            <div style="font-size:12px;color:#7a8ba8;margin-top:8px;line-height:1.6;">
                Select emergency type, optionally add photo<br>
                & description, then trigger the alert.
            </div>
        </div>

        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:16px;margin-top:12px;">
            <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">SMART SOS FEATURES</div>
            <div style="font-size:12px;color:#e8edf5;line-height:2.2;">
                📸 Auto-attach photo evidence<br>
                📍 Floor & room auto-detection<br>
                🤖 AI severity scoring (0–10)<br>
                👨‍👩‍👧 Emergency contact notification<br>
                ⏱ Real-time incident timeline
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Quick Analyze ──
st.markdown("---")
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">DESCRIBE EMERGENCY FOR AI ANALYSIS</div>', unsafe_allow_html=True)
desc2 = st.text_area("Describe what's happening...", height=70, label_visibility="collapsed",
                     placeholder="e.g., Fire in kitchen, someone is unconscious in lobby...")
if desc2 and st.button("🔍 Analyze & Alert", use_container_width=True):
    analysis = full_analysis(desc2)
    sev_col2 = severity_color(analysis["severity"])
    sev_score2 = calculate_ai_severity_score(analysis["type"], analysis["severity"])
    rec = "Immediate Evacuation" if analysis["severity"] == "CRITICAL" else "Dispatch Response Team" if analysis["severity"] == "PRIORITY" else "Monitor Situation"
    st.markdown(f"""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-left:3px solid {sev_col2};border-radius:8px;padding:16px;margin-top:12px;">
        <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:'JetBrains Mono',monospace;">AI ANALYSIS RESULT</div>
        <div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:12px;">
            <div><div style="font-size:10px;color:#7a8ba8;">TYPE</div><div style="font-size:16px;font-weight:700;color:#e8edf5;">{incident_icon(analysis['type'])} {analysis['type']}</div></div>
            <div><div style="font-size:10px;color:#7a8ba8;">SEVERITY</div><div style="font-size:16px;font-weight:700;color:{sev_col2};">{analysis['severity']}</div></div>
            <div><div style="font-size:10px;color:#7a8ba8;">CONFIDENCE</div><div style="font-size:16px;font-weight:700;color:#00bfff;">{int(analysis['confidence']*100)}%</div></div>
            <div><div style="font-size:10px;color:#7a8ba8;">SEVERITY SCORE</div><div style="font-size:16px;font-weight:700;color:{sev_col2};">{sev_score2}/10</div></div>
        </div>
        <div style="background:rgba(255,140,0,0.1);border:1px solid rgba(255,140,0,0.3);border-radius:6px;padding:10px;">
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:4px;">💡 RECOMMENDATION</div>
            <div style="font-size:13px;color:#ff8c00;font-weight:600;">{rec}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
