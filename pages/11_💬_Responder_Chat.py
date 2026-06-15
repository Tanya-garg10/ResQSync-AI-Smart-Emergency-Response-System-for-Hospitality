"""
Responder Coordination Chat – Real-time multi-user communication during active incidents
"""
import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Responder Chat | ResQSync AI", page_icon="💬", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
</style>
""", unsafe_allow_html=True)

# ── Responder roster ──
RESPONDERS = {
    "Security Alpha":  {"color": "#00bfff", "icon": "🛡️", "role": "Security",  "status": "EN ROUTE"},
    "Medical Unit 1":  {"color": "#00c853", "icon": "🏥", "role": "Medical",   "status": "ON SITE"},
    "Fire Response":   {"color": "#ff4b4b", "icon": "🔥", "role": "Fire",      "status": "STANDBY"},
    "Floor Manager":   {"color": "#ffd700", "icon": "🏨", "role": "Management","status": "ON SITE"},
    "Command Center":  {"color": "#ff8c00", "icon": "📡", "role": "Command",   "status": "ONLINE"},
}

MSG_TYPES = {
    "STATUS":  {"bg": "#0d1e2e", "border": "#1a3a50", "color": "#00bfff"},
    "ALERT":   {"bg": "#2e0d0d", "border": "#5a1a1a", "color": "#ff4b4b"},
    "REQUEST": {"bg": "#2e1a0d", "border": "#503010", "color": "#ff8c00"},
    "INFO":    {"bg": "#0d2e18", "border": "#1a5030", "color": "#00c853"},
    "SYSTEM":  {"bg": "#2e2a0d", "border": "#504520", "color": "#ffd700"},
}

def _ts(seconds_ago):
    return (datetime.now() - timedelta(seconds=seconds_ago)).strftime("%H:%M:%S")

DEMO_MESSAGES = [
    {"id": 1,  "sender": "Command Center",  "text": "🚨 INCIDENT ACTIVATED — Fire emergency Floor 3 Room 307. All units respond.",             "type": "ALERT",   "ts": _ts(310)},
    {"id": 2,  "sender": "Security Alpha",  "text": "Security Alpha acknowledged. En route via Corridor B. ETA 45 seconds.",                   "type": "STATUS",  "ts": _ts(295)},
    {"id": 3,  "sender": "Floor Manager",   "text": "Floor Manager on site. Initiating guest evacuation on Floor 3 now.",                       "type": "STATUS",  "ts": _ts(280)},
    {"id": 4,  "sender": "Fire Response",   "text": "Fire Response on standby. Awaiting hazard assessment before entry. Request visual.",       "type": "REQUEST", "ts": _ts(260)},
    {"id": 5,  "sender": "Medical Unit 1",  "text": "Medical Unit 1 arrived lobby. Any casualties reported?",                                   "type": "REQUEST", "ts": _ts(240)},
    {"id": 6,  "sender": "Command Center",  "text": "No casualties confirmed yet. Smoke detected in corridor only. Proceed with caution.",      "type": "INFO",    "ts": _ts(225)},
    {"id": 7,  "sender": "Security Alpha",  "text": "Arrived Floor 3. Corridor clear. Smoke visible near Room 307. No open flames yet.",        "type": "STATUS",  "ts": _ts(200)},
    {"id": 8,  "sender": "Fire Response",   "text": "Fire Response moving in. Deploying extinguishers. Stand clear of Rooms 305–309.",          "type": "ALERT",   "ts": _ts(175)},
    {"id": 9,  "sender": "Floor Manager",   "text": "14 guests evacuated from Floor 3. 2 guests unaccounted. Checking rooms 311 and 312.",       "type": "STATUS",  "ts": _ts(150)},
    {"id": 10, "sender": "Medical Unit 1",  "text": "Standing by at assembly point. No injuries reported so far. ✅",                           "type": "INFO",    "ts": _ts(120)},
    {"id": 11, "sender": "Command Center",  "text": "⚠️ PRIORITY — Guest with breathing difficulty near stairwell. Medical respond.",           "type": "ALERT",   "ts": _ts(90)},
    {"id": 12, "sender": "Medical Unit 1",  "text": "On my way to stairwell now. ETA 20 seconds.",                                              "type": "STATUS",  "ts": _ts(80)},
    {"id": 13, "sender": "Fire Response",   "text": "Fire contained. Source: faulty electrical Room 307. No structural damage. Ventilating.",   "type": "INFO",    "ts": _ts(50)},
    {"id": 14, "sender": "Security Alpha",  "text": "Floor 3 secured. All rooms checked. 16/16 guests accounted for. ✅",                       "type": "INFO",    "ts": _ts(30)},
    {"id": 15, "sender": "Command Center",  "text": "Incident moving to RESOLVED. Outstanding coordination. Standby for debrief.",              "type": "SYSTEM",  "ts": _ts(10)},
]

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = list(DEMO_MESSAGES)
    st.session_state.chat_msg_counter = len(DEMO_MESSAGES) + 1

if "chat_user" not in st.session_state:
    st.session_state.chat_user = "Command Center"

# ── Header ──
st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:18px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">💬 Responder Coordination</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        LIVE CHAT &nbsp;•&nbsp; MULTI-UNIT COORDINATION &nbsp;•&nbsp; INCIDENT COMMS
    </div>
</div>
""", unsafe_allow_html=True)

col_chat, col_sidebar = st.columns([3, 1])

# ════════════════════════════════════════
#  LEFT  — Chat panel
# ════════════════════════════════════════
with col_chat:

    # Active incident banner
    active_inc = (st.session_state.incidents[0]
                  if "incidents" in st.session_state and st.session_state.incidents
                  else {"id": 3821, "type": "FIRE", "zone": "Floor 3, Room 307",
                        "severity": "CRITICAL", "status": "ACTIVE"})

    st.markdown(f"""
    <div style="background:rgba(255,75,75,0.07);border:1px solid rgba(255,75,75,0.3);
                border-radius:8px;padding:10px 16px;margin-bottom:12px;
                display:flex;align-items:center;gap:12px;">
        <span style="font-size:18px;">🚨</span>
        <div style="flex:1;">
            <span style="font-size:12px;font-weight:700;color:#ff4b4b;">
                INCIDENT #{active_inc['id']} — {active_inc['type']}
            </span>
            <span style="font-size:11px;color:#7a8ba8;margin-left:10px;">
                {active_inc.get('zone','Floor 3, Room 307')}
            </span>
        </div>
        <span style="font-size:10px;background:rgba(255,75,75,0.2);color:#ff4b4b;
                     padding:3px 10px;border-radius:12px;font-weight:700;">
            ● {active_inc.get('status','ACTIVE')}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Build complete chat HTML for components.html ──
    msgs = st.session_state.chat_messages
    me   = st.session_state.chat_user

    bubbles_html = ""
    for msg in msgs:
        r_info  = RESPONDERS.get(msg["sender"], {"color": "#7a8ba8", "icon": "👤", "role": "User"})
        t_info  = MSG_TYPES.get(msg["type"], MSG_TYPES["INFO"])
        is_self = (msg["sender"] == me)
        align   = "flex-end" if is_self else "flex-start"
        br      = "8px 2px 8px 8px" if is_self else "2px 8px 8px 8px"
        bg      = "rgba(0,191,255,0.08)" if is_self else t_info["bg"]
        border  = "rgba(0,191,255,0.3)"  if is_self else t_info["border"]

        bubbles_html += f"""
        <div style="display:flex;flex-direction:column;align-items:{align};margin-bottom:10px;max-width:88%;">
            <div style="font-size:10px;color:#555;margin-bottom:3px;{'text-align:right' if is_self else ''};">
                {r_info['icon']}
                <span style="color:{r_info['color']};font-weight:600;margin-left:2px;">{msg['sender']}</span>
                <span style="background:{t_info['bg']};border:1px solid {t_info['border']};color:{t_info['color']};
                             padding:1px 6px;border-radius:8px;margin-left:5px;font-size:9px;
                             font-family:'JetBrains Mono',monospace;">{msg['type']}</span>
                <span style="margin-left:6px;font-family:'JetBrains Mono',monospace;font-size:9px;">{msg['ts']}</span>
            </div>
            <div style="background:{bg};border:1px solid {border};border-radius:{br};
                        padding:9px 13px;font-size:12px;color:#e8edf5;line-height:1.55;
                        max-width:100%;word-wrap:break-word;">
                {msg['text']}
            </div>
        </div>
        """

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: #0d1117;
            font-family: 'Inter', sans-serif;
            padding: 14px;
            overflow-y: auto;
        }}
        ::-webkit-scrollbar {{ width: 5px; }}
        ::-webkit-scrollbar-track {{ background: #0d1117; }}
        ::-webkit-scrollbar-thumb {{ background: #1e2a3a; border-radius: 3px; }}
    </style>
    </head>
    <body>
        {bubbles_html}
        <div id="bottom"></div>
    </body>
    <script>
        document.getElementById('bottom').scrollIntoView({{ behavior: 'smooth' }});
    </script>
    </html>
    """

    components.html(full_html, height=440, scrolling=True)

    # ── Input row ──
    st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
    inp_col1, inp_col2, inp_col3 = st.columns([4, 1, 1])
    with inp_col1:
        new_msg = st.text_input("Message", key="chat_input",
                                placeholder="Type coordination message...",
                                label_visibility="collapsed")
    with inp_col2:
        msg_type = st.selectbox("Type", ["STATUS", "ALERT", "REQUEST", "INFO"],
                                label_visibility="collapsed")
    with inp_col3:
        send_btn = st.button("📤 Send", use_container_width=True, type="primary")

    if send_btn and new_msg.strip():
        st.session_state.chat_messages.append({
            "id":     st.session_state.chat_msg_counter,
            "sender": st.session_state.chat_user,
            "text":   new_msg.strip(),
            "type":   msg_type,
            "ts":     datetime.now().strftime("%H:%M:%S"),
        })
        st.session_state.chat_msg_counter += 1
        st.rerun()

    # ── Quick messages ──
    st.markdown('<div style="font-size:10px;color:#555;letter-spacing:1px;margin:10px 0 6px;'
                'font-family:\'JetBrains Mono\',monospace;">QUICK MESSAGES</div>',
                unsafe_allow_html=True)
    q_cols = st.columns(4)
    quick_msgs = [
        ("✅ On my way",     "STATUS",  "On my way to the incident location."),
        ("📍 Arrived",       "STATUS",  "Arrived on scene. Assessing situation."),
        ("⚠️ Need backup",   "REQUEST", "Requesting immediate backup at current location."),
        ("🔒 Area secured",  "INFO",    "Area secured. No further threats detected."),
        ("🏥 Casualties?",   "REQUEST", "Any casualties reported? Medical unit standing by."),
        ("📻 All clear",     "INFO",    "All clear — incident contained. Standing down."),
        ("🚪 Evacuating",    "STATUS",  "Initiating floor evacuation. Directing guests to exits."),
        ("🔥 Fire out",      "INFO",    "Fire extinguished. Ventilating the area now."),
    ]
    for i, (label, qtype, qtext) in enumerate(quick_msgs):
        with q_cols[i % 4]:
            if st.button(label, use_container_width=True, key=f"quick_{i}"):
                st.session_state.chat_messages.append({
                    "id":     st.session_state.chat_msg_counter,
                    "sender": st.session_state.chat_user,
                    "text":   qtext,
                    "type":   qtype,
                    "ts":     datetime.now().strftime("%H:%M:%S"),
                })
                st.session_state.chat_msg_counter += 1
                st.rerun()

# ════════════════════════════════════════
#  RIGHT  — Sidebar panel
# ════════════════════════════════════════
with col_sidebar:

    # Identity selector
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:8px;'
                'font-family:\'JetBrains Mono\',monospace;">YOU ARE</div>',
                unsafe_allow_html=True)

    selected_user = st.selectbox(
        "Identity",
        list(RESPONDERS.keys()),
        label_visibility="collapsed",
        index=list(RESPONDERS.keys()).index(st.session_state.chat_user),
    )
    if selected_user != st.session_state.chat_user:
        st.session_state.chat_user = selected_user
        st.rerun()

    r_self = RESPONDERS[st.session_state.chat_user]
    st.markdown(f"""
    <div style="background:#151b28;border:1px solid {r_self['color']}55;border-radius:8px;
                padding:12px;text-align:center;margin-bottom:14px;">
        <div style="font-size:28px;">{r_self['icon']}</div>
        <div style="font-size:13px;font-weight:700;color:{r_self['color']};margin-top:4px;">
            {st.session_state.chat_user}
        </div>
        <div style="font-size:10px;color:#7a8ba8;margin-top:2px;">{r_self['role']}</div>
        <div style="font-size:10px;font-weight:600;color:{r_self['color']};margin-top:6px;">
            ● {r_self['status']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Online units
    st.markdown(f'<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                f'text-transform:uppercase;margin-bottom:10px;'
                f'font-family:\'JetBrains Mono\',monospace;">UNITS ONLINE ({len(RESPONDERS)})</div>',
                unsafe_allow_html=True)

    for name, info in RESPONDERS.items():
        is_me      = name == st.session_state.chat_user
        card_border = f"{info['color']}55" if is_me else "#1e2a3a"
        you_tag    = ' <span style="font-size:9px;color:#555;">← you</span>' if is_me else ""
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid {card_border};border-radius:6px;
                    padding:9px 10px;margin-bottom:6px;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:14px;">{info['icon']}</span>
                <div style="flex:1;min-width:0;">
                    <div style="font-size:11px;font-weight:600;color:#e8edf5;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                        {name}{you_tag}
                    </div>
                    <div style="font-size:9px;color:{info['color']};
                                font-family:'JetBrains Mono',monospace;">{info['status']}</div>
                </div>
                <div style="width:7px;height:7px;border-radius:50%;
                            background:{info['color']};flex-shrink:0;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Chat stats
    total_msgs  = len(st.session_state.chat_messages)
    alert_count = sum(1 for m in st.session_state.chat_messages if m["type"] == "ALERT")
    my_count    = sum(1 for m in st.session_state.chat_messages
                      if m["sender"] == st.session_state.chat_user)

    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin:14px 0 10px;'
                'font-family:\'JetBrains Mono\',monospace;">CHAT STATS</div>',
                unsafe_allow_html=True)

    for label, val, color in [
        ("Total Messages", total_msgs,  "#e8edf5"),
        ("🚨 Alerts",       alert_count, "#ff4b4b"),
        ("Your Messages",  my_count,    "#00bfff"),
    ]:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:6px;
                    padding:8px 12px;margin-bottom:6px;
                    display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:11px;color:#7a8ba8;">{label}</span>
            <span style="font-size:14px;font-weight:700;color:{color};">{val}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

    # Simulate incoming message
    if st.button("📡 Simulate Incoming", use_container_width=True):
        sim_senders  = [k for k in RESPONDERS if k != st.session_state.chat_user]
        sim_pool = [
            ("Requesting floor plan for Floor 3 — can Command share the layout?", "REQUEST"),
            ("Guest with asthma assisted. Moving to medical station now. ✅",      "INFO"),
            ("All exits on Floor 3 confirmed clear. Guest count updated.",          "STATUS"),
            ("Smoke dissipating. Air quality returning to normal levels.",           "INFO"),
            ("⚠️ Elevator out of service on Floor 3 — use stairs only.",            "ALERT"),
            ("Secondary check complete. No secondary ignition sources found.",      "STATUS"),
            ("Requesting additional fire extinguisher on south corridor.",           "REQUEST"),
            ("All clear on my sector. Moving to assist Medical Unit 1.",             "STATUS"),
        ]
        s        = random.choice(sim_senders)
        t, mtype = random.choice(sim_pool)
        st.session_state.chat_messages.append({
            "id":     st.session_state.chat_msg_counter,
            "sender": s,
            "text":   t,
            "type":   mtype,
            "ts":     datetime.now().strftime("%H:%M:%S"),
        })
        st.session_state.chat_msg_counter += 1
        st.rerun()

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.chat_msg_counter = 1
            st.rerun()
    with btn_col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.chat_messages = list(DEMO_MESSAGES)
            st.session_state.chat_msg_counter = len(DEMO_MESSAGES) + 1
            st.rerun()
