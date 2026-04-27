"""
Live Tracking – Real-time map with responder movement & ETA
"""
import streamlit as st
import random
from datetime import datetime
from services.location_service import HOTEL_ZONES, get_responder_location, get_nearest_exit
from utils.helpers import generate_demo_incidents, incident_icon, severity_color

st.set_page_config(page_title="Live Tracking | ResQSync AI", page_icon="🗺️", layout="wide")

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
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">Live Tracking</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        REAL-TIME LOCATION • RESPONDER ETA • EVACUATION ROUTES
    </div>
</div>
""", unsafe_allow_html=True)

# ── Map + Info Panel ──
col_map, col_info = st.columns([2, 1])

with col_map:
    try:
        import folium
        from streamlit_folium import st_folium

        # Hotel-centered map
        m = folium.Map(location=[28.6139, 77.2090], zoom_start=17, tiles="CartoDB dark_matter")

        # Hotel zones
        for name, loc in HOTEL_ZONES.items():
            folium.Marker(
                location=[loc["lat"], loc["lon"]],
                popup=f"{name} (Floor: {loc['floor']})",
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)

        # Active incidents
        if "incidents" in st.session_state:
            for inc in st.session_state.incidents[:4]:
                lat = 28.6139 + random.uniform(-0.001, 0.001)
                lon = 77.2090 + random.uniform(-0.001, 0.001)
                color = "red" if inc["severity"] == "CRITICAL" else "orange"
                folium.CircleMarker(
                    location=[lat, lon], radius=10, color=color,
                    fill=True, fill_opacity=0.8,
                    popup=f"🚨 {inc['type']} | {inc['severity']}",
                ).add_to(m)

                # Responder
                progress = random.uniform(0.3, 0.9)
                resp = get_responder_location(lat, lon, progress)
                folium.Marker(
                    location=[resp["lat"], resp["lon"]],
                    popup=f"Responder | {resp['status']} | ETA: {resp['eta_seconds']}s",
                    icon=folium.Icon(color="green", icon="user"),
                ).add_to(m)

                # Line from responder to incident
                folium.PolyLine(
                    locations=[[resp["lat"], resp["lon"]], [lat, lon]],
                    color="#00bfff", weight=2, dash_array="5",
                ).add_to(m)

        # Emergency exits
        exits = [
            {"name": "Main Entrance", "lat": 28.6136, "lon": 77.2089},
            {"name": "Fire Exit A", "lat": 28.6141, "lon": 77.2096},
            {"name": "Fire Exit B", "lat": 28.6137, "lon": 77.2083},
        ]
        for ex in exits:
            folium.Marker(
                location=[ex["lat"], ex["lon"]],
                popup=f"🚪 {ex['name']}",
                icon=folium.Icon(color="green", icon="log-out"),
            ).add_to(m)

        st_folium(m, height=500, use_container_width=True, returned_objects=[])

    except ImportError:
        st.markdown("""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;height:500px;display:flex;align-items:center;justify-content:center;">
            <div style="text-align:center;color:#7a8ba8;">
                <div style="font-size:48px;margin-bottom:12px;">🗺️</div>
                <div>Install folium & streamlit-folium for live map</div>
                <code style="font-size:11px;color:#555;">pip install folium streamlit-folium</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_info:
    # Active Units
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">ACTIVE RESPONDERS</div>', unsafe_allow_html=True)

    responders = [
        {"name": "Security Team Alpha", "status": "EN ROUTE", "eta": "45s"},
        {"name": "Medical Unit 1", "status": "EN ROUTE", "eta": "1m 20s"},
        {"name": "Fire Response", "status": "STANDBY", "eta": "—"},
        {"name": "Floor Manager L2", "status": "ON SITE", "eta": "Arrived"},
    ]

    for r in responders:
        s_color = "#00bfff" if r["status"] == "EN ROUTE" else "#00c853" if r["status"] == "ON SITE" else "#7a8ba8"
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:6px;padding:12px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:12px;font-weight:600;color:#e8edf5;">{r['name']}</span>
                <span style="font-size:10px;color:{s_color};font-family:'JetBrains Mono',monospace;">{r['status']}</span>
            </div>
            <div style="font-size:11px;color:#7a8ba8;margin-top:4px;">ETA: {r['eta']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Nearest Exits
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:20px 0 12px 0;font-family:\'JetBrains Mono\',monospace;">EMERGENCY EXITS</div>', unsafe_allow_html=True)

    for ex in exits if 'exits' in dir() else [{"name": "Main Entrance"}, {"name": "Fire Exit A"}, {"name": "Fire Exit B"}]:
        name = ex["name"] if isinstance(ex, dict) else ex
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-left:3px solid #00c853;border-radius:6px;padding:10px 12px;margin-bottom:6px;">
            <span style="font-size:12px;color:#e8edf5;">🚪 {name}</span>
        </div>
        """, unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;margin-top:20px;">
        <div style="font-size:10px;color:#7a8ba8;letter-spacing:1px;margin-bottom:8px;">MAP LEGEND</div>
        <div style="font-size:11px;color:#e8edf5;line-height:2;">
            🔴 Critical Incident<br>
            🟠 Priority Incident<br>
            🟢 Responder<br>
            🔵 Hotel Zone<br>
            🚪 Emergency Exit<br>
            - - - Responder Route
        </div>
    </div>
    """, unsafe_allow_html=True)
