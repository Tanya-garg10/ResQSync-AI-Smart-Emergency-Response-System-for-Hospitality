"""
Hotel Floor Map – Visual floor plan with room, exits, responder locations
"""
import streamlit as st
import random
from utils.helpers import incident_icon, severity_color

st.set_page_config(page_title="Hotel Floor Map | ResQSync AI", page_icon="🏨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
.room-normal { background:#151b28; border:1px solid #1e2a3a; }
.room-fire { background:rgba(255,75,75,0.15); border:1px solid rgba(255,75,75,0.5); }
.room-exit { background:rgba(0,200,83,0.1); border:1px solid rgba(0,200,83,0.4); }
.room-responder { background:rgba(0,191,255,0.1); border:1px solid rgba(0,191,255,0.4); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">🏨 Hotel Floor Map</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        FLOOR PLAN • INCIDENT ZONES • EXIT ROUTES • RESPONDER POSITIONS
    </div>
</div>
""", unsafe_allow_html=True)

col_controls, col_map_main = st.columns([1, 3])

with col_controls:
    floor_select = st.selectbox("Select Floor", ["Ground Floor", "Floor 1", "Floor 2", "Floor 3 ⚠️", "Floor 4"])
    active_floor = "3" if "3" in floor_select else floor_select.split()[-1][0] if floor_select != "Ground Floor" else "G"

    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">MAP LEGEND</div>', unsafe_allow_html=True)
    legend_items = [
        ("🔴", "Incident Zone", "#ff4b4b"),
        ("🟢", "Emergency Exit", "#00c853"),
        ("🔵", "Responder", "#00bfff"),
        ("⬛", "Normal Room", "#7a8ba8"),
        ("🟡", "Elevator/Stair", "#ffd700"),
    ]
    for icon, label, color in legend_items:
        st.markdown(f'<div style="font-size:12px;color:#e8edf5;margin-bottom:6px;">{icon} <span style="color:{color};">{label}</span></div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:14px 0 8px;font-family:\'JetBrains Mono\',monospace;">FLOOR STATUS</div>', unsafe_allow_html=True)
    floor_statuses = {
        "Ground Floor": ("CLEAR", "#00c853"),
        "Floor 1": ("CLEAR", "#00c853"),
        "Floor 2": ("MONITORING", "#ffd700"),
        "Floor 3 ⚠️": ("ALERT", "#ff4b4b"),
        "Floor 4": ("CLEAR", "#00c853"),
    }
    for fl, (status, color) in floor_statuses.items():
        fl_name = fl.replace(" ⚠️", "")
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:5px;padding:6px 10px;margin-bottom:4px;display:flex;justify-content:space-between;">
            <span style="font-size:11px;color:#e8edf5;">{fl_name}</span>
            <span style="font-size:10px;color:{color};font-weight:600;">{status}</span>
        </div>
        """, unsafe_allow_html=True)

with col_map_main:
    # Determine incident room based on floor selection
    is_incident_floor = "3" in floor_select
    incident_room = "307" if is_incident_floor else None
    has_responder = is_incident_floor

    # Build floor plan grid
    floor_num = active_floor

    # Define rooms for this floor
    rooms_row1 = ["301", "302", "303", "304", "305"]
    rooms_row2 = ["306", "307", "308", "309", "310"]
    rooms_row3 = ["311", "312", "313", "314", "315"]

    floor_header_color = "#ff4b4b" if is_incident_floor else "#e8edf5"
    floor_badge = ' <span style="font-size:11px;background:rgba(255,75,75,0.2);color:#ff4b4b;padding:2px 8px;border-radius:10px;"> ⚠️ ACTIVE INCIDENT</span>' if is_incident_floor else ""

    st.markdown(f"""
    <div style="background:#151b28;border:1px solid {'rgba(255,75,75,0.4)' if is_incident_floor else '#1e2a3a'};border-radius:10px;padding:20px;">
        <div style="font-size:16px;font-weight:700;color:{floor_header_color};margin-bottom:18px;">
            Floor {floor_num}{floor_badge}
        </div>
    """, unsafe_allow_html=True)

    def render_room(room_num, incident_room=None, is_responder_room=None):
        if room_num == incident_room:
            bg = "rgba(255,75,75,0.15)"
            border = "1px solid rgba(255,75,75,0.6)"
            color = "#ff4b4b"
            icon = "🔴"
            extra = "<br><span style='font-size:9px;'>FIRE</span>"
        elif room_num == is_responder_room:
            bg = "rgba(0,191,255,0.1)"
            border = "1px solid rgba(0,191,255,0.5)"
            color = "#00bfff"
            icon = "🔵"
            extra = "<br><span style='font-size:9px;'>RESP.</span>"
        else:
            bg = "#111620"
            border = "1px solid #1e2a3a"
            color = "#7a8ba8"
            icon = ""
            extra = ""
        return f"""
        <div style="background:{bg};border:{border};border-radius:6px;padding:8px 4px;text-align:center;min-width:60px;">
            <div style="font-size:11px;font-weight:600;color:{color};">{icon}{room_num}</div>
            <div style="font-size:9px;color:#555;">{extra}</div>
        </div>
        """

    responder_room = "308" if is_incident_floor else None

    for row, rooms in [("ROW A (North Wing)", rooms_row1), ("ROW B (Central)", rooms_row2), ("ROW C (South Wing)", rooms_row3)]:
        st.markdown(f'<div style="font-size:10px;color:#555;letter-spacing:1px;margin:10px 0 6px;font-family:\'JetBrains Mono\',monospace;">{row}</div>', unsafe_allow_html=True)
        room_cols = st.columns(len(rooms) + 2)
        for i, room in enumerate(rooms):
            with room_cols[i]:
                st.markdown(render_room(room, incident_room, responder_room), unsafe_allow_html=True)
        # Stairwell and elevator
        with room_cols[-2]:
            st.markdown("""
            <div style="background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.3);border-radius:6px;padding:8px 4px;text-align:center;">
                <div style="font-size:14px;">🛗</div>
                <div style="font-size:9px;color:#ffd700;">ELEV.</div>
            </div>
            """, unsafe_allow_html=True)
        with room_cols[-1]:
            st.markdown("""
            <div style="background:rgba(0,200,83,0.1);border:1px solid rgba(0,200,83,0.3);border-radius:6px;padding:8px 4px;text-align:center;">
                <div style="font-size:14px;">🚪</div>
                <div style="font-size:9px;color:#00c853;">EXIT</div>
            </div>
            """, unsafe_allow_html=True)

    # Corridor
    st.markdown("""
    <div style="background:#0d1117;border:1px dashed #1e2a3a;border-radius:4px;padding:8px;text-align:center;margin:10px 0;font-size:11px;color:#555;letter-spacing:2px;font-family:'JetBrains Mono',monospace;">
        ━━━━━━━  MAIN CORRIDOR  ━━━━━━━
    </div>
    """, unsafe_allow_html=True)

    # Exit row
    exit_col1, exit_col2, exit_col3 = st.columns([1,1,1])
    with exit_col1:
        st.markdown("""
        <div style="background:rgba(0,200,83,0.1);border:1px solid rgba(0,200,83,0.4);border-radius:6px;padding:10px;text-align:center;">
            <div style="font-size:18px;">🚪</div>
            <div style="font-size:11px;color:#00c853;font-weight:600;">Exit A</div>
            <div style="font-size:9px;color:#555;">North Stairwell</div>
        </div>
        """, unsafe_allow_html=True)
    with exit_col2:
        st.markdown("""
        <div style="background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.3);border-radius:6px;padding:10px;text-align:center;">
            <div style="font-size:18px;">🛗</div>
            <div style="font-size:11px;color:#ffd700;font-weight:600;">Elevator Bank</div>
            <div style="font-size:9px;color:#555;">Central</div>
        </div>
        """, unsafe_allow_html=True)
    with exit_col3:
        st.markdown("""
        <div style="background:rgba(0,200,83,0.1);border:1px solid rgba(0,200,83,0.4);border-radius:6px;padding:10px;text-align:center;">
            <div style="font-size:18px;">🚪</div>
            <div style="font-size:11px;color:#00c853;font-weight:600;">Exit B</div>
            <div style="font-size:9px;color:#555;">South Stairwell</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Active incident info for floor 3
    if is_incident_floor:
        st.markdown("""
        <div style="background:rgba(255,75,75,0.08);border:1px solid rgba(255,75,75,0.3);border-radius:8px;padding:14px;margin-top:12px;">
            <div style="font-size:11px;font-weight:600;color:#ff4b4b;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">🔴 ACTIVE INCIDENT — FLOOR 3</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;font-size:12px;">
                <div><div style="color:#7a8ba8;font-size:10px;">INCIDENT</div><div style="color:#e8edf5;font-weight:600;">🔥 FIRE EMERGENCY</div></div>
                <div><div style="color:#7a8ba8;font-size:10px;">LOCATION</div><div style="color:#ff4b4b;font-weight:600;">Room 307</div></div>
                <div><div style="color:#7a8ba8;font-size:10px;">NEAREST EXIT</div><div style="color:#00c853;font-weight:600;">🚪 Exit A (North)</div></div>
                <div><div style="color:#7a8ba8;font-size:10px;">RESPONDER</div><div style="color:#00bfff;font-weight:600;">🔵 Room 308</div></div>
                <div><div style="color:#7a8ba8;font-size:10px;">ETA TO SCENE</div><div style="color:#ffd700;font-weight:600;">~38 seconds</div></div>
                <div><div style="color:#7a8ba8;font-size:10px;">EVACUATE VIA</div><div style="color:#00c853;font-weight:600;">Exit A or Exit B</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
