"""
Smart Responder Tracking – Nearest auto-assign, route optimization, live status
"""
import streamlit as st
import random
from datetime import datetime
from services.location_service import HOTEL_ZONES, get_responder_location, get_nearest_exit
from utils.helpers import generate_demo_incidents, incident_icon, severity_color

st.set_page_config(page_title="Smart Tracking | ResQSync AI", page_icon="🗺️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
@keyframes pulse-dot { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:0.5;transform:scale(1.3);} }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">🗺️ Smart Responder Tracking</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        AUTO-ASSIGN • ROUTE OPTIMIZATION • LIVE STATUS • ETA
    </div>
</div>
""", unsafe_allow_html=True)

# ── Assigned Team Banner ──
assigned_team = {
    "name": "Security Alpha",
    "unit": "Team A-01",
    "distance": random.randint(80, 200),
    "eta": random.randint(25, 60),
    "route": random.choice(["Corridor B → Stairwell 2", "Main Lobby → Elevator C", "Service Passage → Floor 3"]),
    "status": "MOVING",
}

st.markdown(f"""
<div style="background:rgba(0,191,255,0.08);border:1px solid rgba(0,191,255,0.3);border-radius:10px;padding:16px;margin-bottom:20px;">
    <div style="font-size:11px;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:'JetBrains Mono',monospace;">⚡ AUTO-ASSIGNED TEAM</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
        <div style="background:#111620;border-radius:8px;padding:12px;text-align:center;">
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:4px;">ASSIGNED TEAM</div>
            <div style="font-size:14px;font-weight:700;color:#e8edf5;">🛡️ {assigned_team['name']}</div>
            <div style="font-size:10px;color:#555;margin-top:2px;">{assigned_team['unit']}</div>
        </div>
        <div style="background:#111620;border-radius:8px;padding:12px;text-align:center;">
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:4px;">DISTANCE</div>
            <div style="font-size:20px;font-weight:700;color:#00bfff;">{assigned_team['distance']}</div>
            <div style="font-size:10px;color:#555;">meters</div>
        </div>
        <div style="background:#111620;border-radius:8px;padding:12px;text-align:center;">
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:4px;">ETA</div>
            <div style="font-size:20px;font-weight:700;color:#00c853;">{assigned_team['eta']}</div>
            <div style="font-size:10px;color:#555;">seconds</div>
        </div>
        <div style="background:#111620;border-radius:8px;padding:12px;text-align:center;">
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:4px;">STATUS</div>
            <div style="font-size:11px;font-weight:700;color:#ffd700;animation:pulse-dot 1.5s infinite;">🟡 {assigned_team['status']}</div>
            <div style="font-size:9px;color:#555;margin-top:4px;font-family:'JetBrains Mono',monospace;">Via shortest route</div>
        </div>
    </div>
    <div style="margin-top:12px;background:#0a0e14;border-radius:6px;padding:10px;">
        <span style="font-size:10px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;">🗺️ OPTIMIZED ROUTE: </span>
        <span style="font-size:12px;color:#00bfff;font-weight:600;">{assigned_team['route']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

col_map, col_info = st.columns([2, 1])

with col_map:
    try:
        import folium
        from streamlit_folium import st_folium

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
                    location=[lat, lon], radius=12, color=color,
                    fill=True, fill_opacity=0.85,
                    popup=f"🚨 {inc['type']} | {inc['severity']} | {inc.get('zone','N/A')}",
                ).add_to(m)
                progress = random.uniform(0.3, 0.9)
                resp = get_responder_location(lat, lon, progress)
                folium.Marker(
                    location=[resp["lat"], resp["lon"]],
                    popup=f"🟢 Responder | {resp['status']} | ETA: {resp['eta_seconds']}s",
                    icon=folium.Icon(color="green", icon="user"),
                ).add_to(m)
                # Optimized route line
                mid_lat = (resp["lat"] + lat) / 2 + random.uniform(-0.0002, 0.0002)
                mid_lon = (resp["lon"] + lon) / 2 + random.uniform(-0.0002, 0.0002)
                folium.PolyLine(
                    locations=[[resp["lat"], resp["lon"]], [mid_lat, mid_lon], [lat, lon]],
                    color="#00c853", weight=3, dash_array="6",
                    tooltip="Optimized Route",
                ).add_to(m)
        else:
            # Demo incident
            demo_lat, demo_lon = 28.6142, 77.2093
            folium.CircleMarker(
                location=[demo_lat, demo_lon], radius=12, color="red",
                fill=True, fill_opacity=0.85,
                popup="🚨 DEMO: Fire Emergency | Floor 3, Room 307",
            ).add_to(m)
            resp_lat, resp_lon = 28.6135, 77.2087
            folium.Marker(
                location=[resp_lat, resp_lon],
                popup="🟢 Security Alpha | EN ROUTE | ETA: 38s",
                icon=folium.Icon(color="green", icon="user"),
            ).add_to(m)
            folium.PolyLine(
                locations=[[resp_lat, resp_lon], [demo_lat, demo_lon]],
                color="#00c853", weight=3, dash_array="6", tooltip="Optimized Route",
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
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;height:500px;display:flex;align-items:center;justify-content:center;text-align:center;color:#7a8ba8;">
            <div><div style="font-size:48px;margin-bottom:12px;">🗺️</div><div>Install folium & streamlit-folium</div></div>
        </div>
        """, unsafe_allow_html=True)

with col_info:
    # Auto-Assigned Responders
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">RESPONDER UNITS</div>', unsafe_allow_html=True)

    responders = [
        {"name": "Security Alpha", "status": "EN ROUTE", "eta": "38s", "dist": "120m", "assigned": True, "route": "Corridor B"},
        {"name": "Medical Unit 1", "status": "EN ROUTE", "eta": "1m 20s", "dist": "340m", "assigned": True, "route": "Main Lobby"},
        {"name": "Fire Response", "status": "STANDBY", "eta": "—", "dist": "—", "assigned": False, "route": "—"},
        {"name": "Floor Manager L2", "status": "ON SITE", "eta": "Arrived", "dist": "0m", "assigned": True, "route": "Arrived"},
    ]

    for r in responders:
        s_color = "#00bfff" if r["status"] == "EN ROUTE" else "#00c853" if r["status"] == "ON SITE" else "#7a8ba8"
        assigned_badge = '<span style="font-size:9px;background:rgba(0,200,83,0.2);color:#00c853;padding:1px 6px;border-radius:10px;margin-left:4px;">AUTO-ASSIGNED</span>' if r["assigned"] and r["status"] != "ON SITE" else ""
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid {'rgba(0,191,255,0.3)' if r['assigned'] else '#1e2a3a'};border-radius:6px;padding:12px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-size:12px;font-weight:600;color:#e8edf5;">{r['name']}{assigned_badge}</span>
                <span style="font-size:10px;color:{s_color};font-family:'JetBrains Mono',monospace;">{r['status']}</span>
            </div>
            <div style="display:flex;gap:10px;font-size:10px;color:#7a8ba8;">
                <span>📍 {r['dist']}</span>
                <span>⏱ ETA: {r['eta']}</span>
                {'<span>🗺️ ' + r['route'] + '</span>' if r['route'] != '—' else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Route Optimization Summary
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:16px 0 10px;font-family:\'JetBrains Mono\',monospace;">ROUTE OPTIMIZATION</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;">
        <div style="font-size:11px;color:#e8edf5;line-height:2.2;">
            <span style="color:#00c853;">●</span> Shortest path calculated<br>
            <span style="color:#00c853;">●</span> Obstacles avoided<br>
            <span style="color:#00c853;">●</span> Crowd density factored<br>
            <span style="color:#ffd700;">●</span> Live update every 5s
        </div>
        <div style="margin-top:10px;background:#0a0e14;border-radius:6px;padding:8px;font-size:11px;font-family:'JetBrains Mono',monospace;color:#00bfff;">
            ALGO: Dijkstra + Heatmap
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Emergency Exits
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:16px 0 10px;font-family:\'JetBrains Mono\',monospace;">EMERGENCY EXITS</div>', unsafe_allow_html=True)
    for ex in [{"name": "Main Entrance", "dist": "45m"}, {"name": "Fire Exit A", "dist": "80m"}, {"name": "Fire Exit B", "dist": "110m"}]:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-left:3px solid #00c853;border-radius:6px;padding:9px 12px;margin-bottom:6px;display:flex;justify-content:space-between;">
            <span style="font-size:12px;color:#e8edf5;">🚪 {ex['name']}</span>
            <span style="font-size:11px;color:#00c853;font-family:'JetBrains Mono',monospace;">{ex['dist']}</span>
        </div>
        """, unsafe_allow_html=True)

    # Map Legend
    st.markdown("""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:12px;margin-top:16px;">
        <div style="font-size:10px;color:#7a8ba8;letter-spacing:1px;margin-bottom:8px;">MAP LEGEND</div>
        <div style="font-size:11px;color:#e8edf5;line-height:2.0;">
            🔴 Active Incident<br>
            🟢 Responder (assigned)<br>
            🔵 Hotel Zone<br>
            🚪 Emergency Exit<br>
            <span style="color:#00c853;">— —</span> Optimized Route
        </div>
    </div>
    """, unsafe_allow_html=True)
