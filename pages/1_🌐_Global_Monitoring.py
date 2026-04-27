"""
Global Monitoring – Command Overview
Matches the dark command center UI with map, health bars, intel stream, event log.
"""
import streamlit as st
import random
from datetime import datetime
from utils.helpers import (
    generate_demo_incidents, generate_network_health,
    incident_icon, severity_color, status_color, get_timestamp, get_date_display,
)
from services.firestore_service import get_incidents

st.set_page_config(page_title="Global Monitoring | ResQSync AI", page_icon="🌐", layout="wide")

# Inject same dark CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg-primary: #0a0e14; --bg-secondary: #111620; --bg-card: #151b28;
    --border-color: #1e2a3a; --text-primary: #e8edf5; --text-secondary: #7a8ba8;
    --accent-red: #ff4b4b; --accent-green: #00c853; --accent-orange: #ff8c00;
    --accent-blue: #00bfff; --accent-yellow: #ffd700;
}
.stApp { background-color: var(--bg-primary) !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: var(--bg-secondary) !important; border-right: 1px solid var(--border-color) !important; }
</style>
""", unsafe_allow_html=True)

# ── Initialize demo data in session ──
if "incidents" not in st.session_state:
    st.session_state.incidents = get_incidents(20)
if "health" not in st.session_state:
    st.session_state.health = generate_network_health()

incidents = st.session_state.incidents
health = st.session_state.health

# ── Header Bar ──
now = datetime.now()
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;">
    <div>
        <span style="font-size:22px;font-weight:700;color:#e8edf5;letter-spacing:0.5px;">Command Overview</span>
        <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
            📅 {get_date_display()} &nbsp;&nbsp;⇄ UPLINK ESTABLISHED &nbsp;&nbsp;🕐 {now.strftime('%I:%M %p')}
        </div>
    </div>
    <div style="display:inline-flex;align-items:center;gap:6px;padding:4px 14px;border-radius:20px;font-size:11px;font-weight:600;
        font-family:'JetBrains Mono',monospace;letter-spacing:0.5px;background:rgba(0,200,83,0.15);color:#00c853;border:1px solid rgba(0,200,83,0.3);">
        ● SYSTEM NOMINAL
    </div>
</div>
""", unsafe_allow_html=True)

# ── Main Layout: Map + Health | Intel Stream ──
col_main, col_intel = st.columns([3, 1])

with col_main:
    # Map + Network Health row
    map_col, health_col = st.columns([1.2, 1])

    with map_col:
        # Dark world map using folium
        try:
            import folium
            from streamlit_folium import st_folium

            m = folium.Map(
                location=[20, 10],
                zoom_start=2,
                tiles="CartoDB dark_matter",
                width="100%",
                height=280,
            )
            # Add incident markers
            for inc in incidents[:6]:
                color = "red" if inc["severity"] == "CRITICAL" else "orange" if inc["severity"] == "PRIORITY" else "green"
                folium.CircleMarker(
                    location=[inc["lat"], inc["lon"]],
                    radius=6,
                    color=color,
                    fill=True,
                    fill_opacity=0.8,
                    popup=f"{inc['type']} | {inc['severity']}",
                ).add_to(m)

            st_folium(m, height=280, use_container_width=True, returned_objects=[])
        except ImportError:
            st.markdown("""
            <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;height:280px;display:flex;align-items:center;justify-content:center;">
                <div style="text-align:center;color:#7a8ba8;">
                    <div style="font-size:40px;margin-bottom:8px;">🗺️</div>
                    <div style="font-size:12px;">Install folium & streamlit-folium for live map</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with health_col:
        st.markdown('<div class="section-title" style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:16px;font-family:\'JetBrains Mono\',monospace;">NETWORK HEALTH</div>', unsafe_allow_html=True)

        for name, value in health.items():
            if value >= 95:
                bar_color = "#00c853"
            elif value >= 85:
                bar_color = "#ff8c00"
            else:
                bar_color = "#ff4b4b"

            st.markdown(f"""
            <div style="margin:12px 0;">
                <div style="display:flex;justify-content:space-between;font-size:11px;font-family:'JetBrains Mono',monospace;color:#7a8ba8;margin-bottom:4px;letter-spacing:0.5px;">
                    <span>{name}</span>
                    <span style="color:{bar_color};font-weight:600;">{value}%</span>
                </div>
                <div style="background:#1a2233;border-radius:3px;height:6px;overflow:hidden;">
                    <div style="height:100%;width:{value}%;background:{bar_color};border-radius:3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Recent Event Log ──
    st.markdown("""
    <div style="margin-top:24px;">
        <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:'JetBrains Mono',monospace;">
            RECENT EVENT LOG
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Build table HTML
    table_rows = ""
    for inc in incidents:
        status_cls = "active-status" if inc["status"] == "ACTIVE" else "responding-status"
        table_rows += f"""
        <tr>
            <td style="padding:10px 12px;color:#e8edf5;border-bottom:1px solid rgba(30,42,58,0.5);font-weight:600;">
                {incident_icon(inc['type'])} {inc['type']}
            </td>
            <td style="padding:10px 12px;color:#e8edf5;border-bottom:1px solid rgba(30,42,58,0.5);">{inc['zone']}</td>
            <td style="padding:10px 12px;border-bottom:1px solid rgba(30,42,58,0.5);">
                <span style="color:{'#00c853' if inc['status']=='ACTIVE' else '#ff8c00'};font-weight:600;">{inc['status']}</span>
            </td>
            <td style="padding:10px 12px;color:#7a8ba8;border-bottom:1px solid rgba(30,42,58,0.5);">{inc['timestamp']}</td>
        </tr>
        """

    st.markdown(f"""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;overflow:hidden;">
        <table style="width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:12px;">
            <thead>
                <tr>
                    <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">INCIDENT</th>
                    <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">ZONE</th>
                    <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">STATUS</th>
                    <th style="text-align:left;padding:10px 12px;color:#7a8ba8;font-weight:500;font-size:10px;letter-spacing:1px;text-transform:uppercase;border-bottom:1px solid #1e2a3a;">TIMESTAMP</th>
                </tr>
            </thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ── Tactical Intel Stream (Right Column) ──
with col_intel:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">TACTICAL INTEL STREAM</div>', unsafe_allow_html=True)

    for inc in incidents[:5]:
        sev = inc["severity"]
        sev_color = severity_color(sev)
        border_color = sev_color
        icon = incident_icon(inc["type"])

        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-left:3px solid {border_color};border-radius:6px;padding:12px 14px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:15px;font-weight:700;color:#e8edf5;">ID: {inc['id']}</span>
                <span style="font-size:10px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;">{inc['timestamp']}</span>
            </div>
            <div style="font-size:11px;color:#7a8ba8;margin-top:4px;display:flex;align-items:center;gap:6px;">
                {icon} <span>{inc['type']}</span> • <span style="color:{sev_color};">{sev}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Generate Alert Button ──
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.incidents = generate_demo_incidents(8)
        st.session_state.health = generate_network_health()
        st.rerun()
with col_btn2:
    if st.button("🚨 Generate Alert", use_container_width=True):
        new_inc = generate_demo_incidents(1)[0]
        new_inc["severity"] = "CRITICAL"
        new_inc["status"] = "ACTIVE"
        st.session_state.incidents.insert(0, new_inc)
        st.rerun()
with col_btn3:
    if st.button("✅ Clear Resolved", use_container_width=True):
        st.session_state.incidents = [i for i in st.session_state.incidents if i["status"] != "RESOLVED"]
        st.rerun()
