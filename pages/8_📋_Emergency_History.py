"""
Emergency History – View past and active incidents with status
"""
import streamlit as st
import random
from datetime import datetime, timedelta
from utils.helpers import generate_incident_id, generate_node_id, incident_icon, severity_color, status_color

st.set_page_config(page_title="Emergency History | ResQSync AI", page_icon="📋", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">📋 Emergency History</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        PAST INCIDENTS • ACTIVE ALERTS • RESOLVED CASES
    </div>
</div>
""", unsafe_allow_html=True)

# ── Build history from session + demo data ──
now = datetime.now()

DEMO_HISTORY = [
    {"id": 3821, "type": "FIRE", "zone": "Floor 3, Room 307", "severity": "CRITICAL", "status": "RESOLVED",
     "timestamp": (now - timedelta(hours=2, minutes=14)).strftime("%I:%M %p"), "date": (now - timedelta(hours=2)).strftime("%b %d"), "responder": "Fire Response Team", "duration": "8 min"},
    {"id": 2974, "type": "MEDICAL", "zone": "Floor 1, Room 112", "severity": "PRIORITY", "status": "RESOLVED",
     "timestamp": (now - timedelta(hours=5, minutes=43)).strftime("%I:%M %p"), "date": (now - timedelta(hours=5)).strftime("%b %d"), "responder": "Medical Unit 1", "duration": "12 min"},
    {"id": 4401, "type": "SECURITY", "zone": "Parking Level B2", "severity": "PRIORITY", "status": "RESOLVED",
     "timestamp": (now - timedelta(days=1, hours=1)).strftime("%I:%M %p"), "date": (now - timedelta(days=1)).strftime("%b %d"), "responder": "Security Alpha", "duration": "5 min"},
    {"id": 1156, "type": "MEDICAL", "zone": "Ground Floor, Lobby", "severity": "MODERATE", "status": "RESOLVED",
     "timestamp": (now - timedelta(days=1, hours=7)).strftime("%I:%M %p"), "date": (now - timedelta(days=1)).strftime("%b %d"), "responder": "Medical Unit 2", "duration": "15 min"},
    {"id": 5533, "type": "FIRE", "zone": "Floor 2, Kitchen", "severity": "CRITICAL", "status": "RESOLVED",
     "timestamp": (now - timedelta(days=2, hours=3)).strftime("%I:%M %p"), "date": (now - timedelta(days=2)).strftime("%b %d"), "responder": "Fire Response Team", "duration": "22 min"},
    {"id": 6644, "type": "SECURITY", "zone": "Floor 4, Corridor", "severity": "LOW", "status": "RESOLVED",
     "timestamp": (now - timedelta(days=3, hours=2)).strftime("%I:%M %p"), "date": (now - timedelta(days=3)).strftime("%b %d"), "responder": "Security Beta", "duration": "3 min"},
]

# Merge with session state incidents (mark as ACTIVE)
session_incidents = []
if "incidents" in st.session_state:
    for inc in st.session_state.incidents:
        session_incidents.append({
            **inc,
            "date": now.strftime("%b %d"),
            "responder": "Auto-Assigned Team",
            "duration": "Active",
        })

all_incidents = session_incidents + DEMO_HISTORY

# ── Summary Metrics ──
total = len(all_incidents)
active = sum(1 for i in all_incidents if i["status"] == "ACTIVE")
resolved = sum(1 for i in all_incidents if i["status"] == "RESOLVED")
fire_count = sum(1 for i in all_incidents if i["type"] == "FIRE")
medical_count = sum(1 for i in all_incidents if i["type"] == "MEDICAL")
security_count = sum(1 for i in all_incidents if i["type"] == "SECURITY")

col1, col2, col3, col4 = st.columns(4)
metrics = [
    (col1, "TOTAL INCIDENTS", str(total), "#e8edf5"),
    (col2, "🔴 ACTIVE", str(active), "#ff4b4b"),
    (col3, "✅ RESOLVED", str(resolved), "#00c853"),
    (col4, "AVG RESPONSE", "8.2 min", "#00bfff"),
]
for col, label, value, color in metrics:
    with col:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;text-align:center;">
            <div style="font-size:10px;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;">{label}</div>
            <div style="font-size:26px;font-weight:700;color:{color};">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin:16px 0;'></div>", unsafe_allow_html=True)

# ── Filter Bar ──
f_col1, f_col2, f_col3 = st.columns([1, 1, 1])
with f_col1:
    filter_type = st.selectbox("Type", ["All Types", "🔥 FIRE", "🏥 MEDICAL", "🚨 SECURITY"])
with f_col2:
    filter_status = st.selectbox("Status", ["All", "ACTIVE", "RESOLVED"])
with f_col3:
    filter_sev = st.selectbox("Severity", ["All", "CRITICAL", "PRIORITY", "MODERATE", "LOW"])

# Apply filters
filtered = all_incidents
if "FIRE" in filter_type:
    filtered = [i for i in filtered if i["type"] == "FIRE"]
elif "MEDICAL" in filter_type:
    filtered = [i for i in filtered if i["type"] == "MEDICAL"]
elif "SECURITY" in filter_type:
    filtered = [i for i in filtered if i["type"] == "SECURITY"]
if filter_status != "All":
    filtered = [i for i in filtered if i["status"] == filter_status]
if filter_sev != "All":
    filtered = [i for i in filtered if i["severity"] == filter_sev]

st.markdown(f'<div style="font-size:11px;color:#7a8ba8;margin-bottom:12px;">{len(filtered)} incidents found</div>', unsafe_allow_html=True)

# ── Incident Cards ──
for inc in filtered:
    sev_col_hex = severity_color(inc["severity"])
    st_col_hex = "#ff4b4b" if inc["status"] == "ACTIVE" else "#00c853"
    icon = incident_icon(inc["type"])

    active_badge = ""
    if inc["status"] == "ACTIVE":
        active_badge = '<span style="font-size:9px;background:rgba(255,75,75,0.2);color:#ff4b4b;padding:2px 8px;border-radius:10px;margin-left:6px;animation:blink 1.5s infinite;">● ACTIVE</span>'

    with st.expander(f"{icon} {inc['type']} — {inc['zone']} | ID: {inc['id']} | {inc['status']}", expanded=(inc["status"]=="ACTIVE")):
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.markdown(f'<div style="font-size:10px;color:#7a8ba8;">SEVERITY</div><div style="font-size:16px;font-weight:700;color:{sev_col_hex};">{inc["severity"]}</div>', unsafe_allow_html=True)
        with d2:
            st.markdown(f'<div style="font-size:10px;color:#7a8ba8;">LOCATION</div><div style="font-size:13px;font-weight:600;color:#e8edf5;">{inc["zone"]}</div>', unsafe_allow_html=True)
        with d3:
            st.markdown(f'<div style="font-size:10px;color:#7a8ba8;">TIME</div><div style="font-size:13px;font-weight:600;color:#e8edf5;">{inc["date"]} {inc["timestamp"]}</div>', unsafe_allow_html=True)
        with d4:
            st.markdown(f'<div style="font-size:10px;color:#7a8ba8;">RESPONDER</div><div style="font-size:13px;font-weight:600;color:#00bfff;">{inc.get("responder","—")}</div>', unsafe_allow_html=True)

        if inc["status"] == "ACTIVE":
            st.markdown(f"""
            <div style="margin-top:10px;background:rgba(255,75,75,0.08);border:1px solid rgba(255,75,75,0.3);border-radius:6px;padding:10px;text-align:center;">
                <span style="font-size:12px;color:#ff4b4b;font-weight:600;">🔴 INCIDENT ACTIVE — Response in Progress</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="margin-top:10px;background:rgba(0,200,83,0.05);border:1px solid rgba(0,200,83,0.2);border-radius:6px;padding:10px;text-align:center;">
                <span style="font-size:12px;color:#00c853;font-weight:600;">✅ RESOLVED — Duration: {inc.get('duration','—')}</span>
            </div>
            """, unsafe_allow_html=True)

# ── Incident Type Chart ──
st.markdown("---")
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">INCIDENT BREAKDOWN</div>', unsafe_allow_html=True)

try:
    import plotly.graph_objects as go
    fig = go.Figure(data=[go.Pie(
        labels=["🔥 Fire", "🏥 Medical", "🚨 Security"],
        values=[fire_count, medical_count, security_count],
        hole=0.5,
        marker=dict(colors=["#ff4b4b", "#00bfff", "#ff8c00"]),
        textfont=dict(color="#e8edf5"),
    )])
    fig.update_layout(
        paper_bgcolor="#151b28", plot_bgcolor="#151b28",
        font=dict(color="#e8edf5"), showlegend=True,
        legend=dict(font=dict(color="#e8edf5")),
        margin=dict(t=10, b=10, l=10, r=10), height=250,
    )
    st.plotly_chart(fig, use_container_width=True)
except ImportError:
    st.markdown(f"""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:16px;text-align:center;">
        <span style="color:#7a8ba8;">🔥 Fire: {fire_count} | 🏥 Medical: {medical_count} | 🚨 Security: {security_count}</span>
    </div>
    """, unsafe_allow_html=True)
