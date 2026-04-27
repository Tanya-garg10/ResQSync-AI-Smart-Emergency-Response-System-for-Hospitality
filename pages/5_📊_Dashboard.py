"""
Admin Dashboard – Active emergencies, coordination, response management
"""
import streamlit as st
import random
from datetime import datetime, timedelta
from utils.helpers import generate_demo_incidents, incident_icon, severity_color, status_color
from services.firestore_service import get_incidents, update_incident_status

st.set_page_config(page_title="Dashboard | ResQSync AI", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">Admin Dashboard</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        INCIDENT MANAGEMENT • RESPONSE COORDINATION • SYSTEM CONTROL
    </div>
</div>
""", unsafe_allow_html=True)

if "incidents" not in st.session_state:
    st.session_state.incidents = get_incidents(50)

incidents = st.session_state.incidents

# ── Metric Cards ──
active = len([i for i in incidents if i["status"] == "ACTIVE"])
responding = len([i for i in incidents if i["status"] == "RESPONDING"])
resolved = len([i for i in incidents if i["status"] == "RESOLVED"])
critical = len([i for i in incidents if i["severity"] == "CRITICAL"])

m1, m2, m3, m4 = st.columns(4)

metrics = [
    ("ACTIVE", active, "#ff4b4b"),
    ("RESPONDING", responding, "#ff8c00"),
    ("RESOLVED", resolved, "#00c853"),
    ("CRITICAL", critical, "#ff4b4b"),
]

for col, (label, value, color) in zip([m1, m2, m3, m4], metrics):
    with col:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-top:3px solid {color};border-radius:8px;padding:20px;text-align:center;">
            <div style="font-size:32px;font-weight:700;color:{color};font-family:'JetBrains Mono',monospace;">{value}</div>
            <div style="font-size:10px;color:#7a8ba8;text-transform:uppercase;letter-spacing:1.5px;margin-top:4px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Incident Management Table ──
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">INCIDENT MANAGEMENT</div>', unsafe_allow_html=True)

# Filters
f1, f2, f3 = st.columns(3)
with f1:
    filter_type = st.selectbox("Filter Type", ["ALL", "FIRE", "MEDICAL", "SECURITY"])
with f2:
    filter_status = st.selectbox("Filter Status", ["ALL", "ACTIVE", "RESPONDING", "RESOLVED"])
with f3:
    filter_severity = st.selectbox("Filter Severity", ["ALL", "CRITICAL", "PRIORITY", "MODERATE", "LOW"])

filtered = incidents
if filter_type != "ALL":
    filtered = [i for i in filtered if i["type"] == filter_type]
if filter_status != "ALL":
    filtered = [i for i in filtered if i["status"] == filter_status]
if filter_severity != "ALL":
    filtered = [i for i in filtered if i["severity"] == filter_severity]

# Table
rows_html = ""
for inc in filtered:
    sev_col = severity_color(inc["severity"])
    stat_col = status_color(inc["status"])
    icon = incident_icon(inc["type"])

    rows_html += f"""
    <tr>
        <td style="padding:10px 12px;color:#e8edf5;border-bottom:1px solid rgba(30,42,58,0.5);font-family:'JetBrains Mono',monospace;font-weight:600;">
            {inc['id']}
        </td>
        <td style="padding:10px 12px;color:#e8edf5;border-bottom:1px solid rgba(30,42,58,0.5);">
            {icon} {inc['type']}
        </td>
        <td style="padding:10px 12px;color:#e8edf5;border-bottom:1px solid rgba(30,42,58,0.5);">{inc['zone']}</td>
        <td style="padding:10px 12px;border-bottom:1px solid rgba(30,42,58,0.5);">
            <span style="color:{sev_col};font-weight:600;">{inc['severity']}</span>
        </td>
        <td style="padding:10px 12px;border-bottom:1px solid rgba(30,42,58,0.5);">
            <span style="color:{stat_col};font-weight:600;">{inc['status']}</span>
        </td>
        <td style="padding:10px 12px;color:#7a8ba8;border-bottom:1px solid rgba(30,42,58,0.5);">{inc['timestamp']}</td>
    </tr>
    """

st.markdown(f"""
<div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;overflow:hidden;">
    <table style="width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:12px;">
        <thead>
            <tr>
                <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">ID</th>
                <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">TYPE</th>
                <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">ZONE</th>
                <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">SEVERITY</th>
                <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">STATUS</th>
                <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">TIME</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# ── Quick Actions ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">QUICK ACTIONS</div>', unsafe_allow_html=True)

a1, a2, a3, a4 = st.columns(4)
with a1:
    if st.button("🚨 New Alert", use_container_width=True):
        new = generate_demo_incidents(1)[0]
        new["severity"] = "CRITICAL"
        st.session_state.incidents.insert(0, new)
        st.rerun()
with a2:
    if st.button("✅ Resolve All Active", use_container_width=True):
        for i in st.session_state.incidents:
            if i["status"] == "ACTIVE":
                i["status"] = "RESOLVED"
                update_incident_status(i.get("id"), "RESOLVED")
        st.rerun()
with a3:
    if st.button("🔄 Refresh", use_container_width=True):
        st.session_state.incidents = generate_demo_incidents(8)
        st.rerun()
with a4:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.incidents = []
        st.rerun()
