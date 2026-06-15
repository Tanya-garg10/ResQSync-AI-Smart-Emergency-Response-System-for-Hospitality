"""
Radio Comms – Push-to-talk simulation with waveform visualization and broadcast log
"""
import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Radio Comms | ResQSync AI", page_icon="📻", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ──
CHANNELS = {
    "CH-1  COMMAND":   {"freq": "462.550 MHz", "color": "#ff8c00", "icon": "📡", "desc": "All-units command"},
    "CH-2  SECURITY":  {"freq": "462.575 MHz", "color": "#00bfff", "icon": "🛡️", "desc": "Security only"},
    "CH-3  MEDICAL":   {"freq": "462.600 MHz", "color": "#00c853", "icon": "🏥", "desc": "Medical team"},
    "CH-4  FIRE":      {"freq": "462.625 MHz", "color": "#ff4b4b", "icon": "🔥", "desc": "Fire response"},
    "CH-5  MGMT":      {"freq": "462.650 MHz", "color": "#ffd700", "icon": "🏨", "desc": "Management"},
}

RESPONDERS = {
    "Security Alpha":  {"color": "#00bfff", "icon": "🛡️"},
    "Medical Unit 1":  {"color": "#00c853", "icon": "🏥"},
    "Fire Response":   {"color": "#ff4b4b", "icon": "🔥"},
    "Floor Manager":   {"color": "#ffd700", "icon": "🏨"},
    "Command Center":  {"color": "#ff8c00", "icon": "📡"},
}

def _ts(s=0):
    return (datetime.now() - timedelta(seconds=s)).strftime("%H:%M:%S")

DEMO_LOG = [
    {"id": 1,  "sender": "Command Center",  "ch": "CH-1  COMMAND",  "msg": "All units — FIRE alert Floor 3, Room 307. Please respond.",       "dur": "0:04", "ts": _ts(310), "signal": 95},
    {"id": 2,  "sender": "Security Alpha",  "ch": "CH-2  SECURITY", "msg": "Security Alpha copies. En route, ETA 45 seconds. Over.",           "dur": "0:03", "ts": _ts(295), "signal": 88},
    {"id": 3,  "sender": "Floor Manager",   "ch": "CH-1  COMMAND",  "msg": "Floor Manager on site. Beginning guest evacuation Floor 3.",       "dur": "0:04", "ts": _ts(280), "signal": 92},
    {"id": 4,  "sender": "Fire Response",   "ch": "CH-4  FIRE",     "msg": "Fire Response requesting visual confirm before entry. Over.",       "dur": "0:03", "ts": _ts(265), "signal": 79},
    {"id": 5,  "sender": "Medical Unit 1",  "ch": "CH-3  MEDICAL",  "msg": "Medical standing by at lobby. Any casualties confirmed? Over.",    "dur": "0:04", "ts": _ts(245), "signal": 91},
    {"id": 6,  "sender": "Command Center",  "ch": "CH-1  COMMAND",  "msg": "Negative on casualties. Smoke in corridor only. Proceed.",         "dur": "0:03", "ts": _ts(225), "signal": 97},
    {"id": 7,  "sender": "Security Alpha",  "ch": "CH-2  SECURITY", "msg": "On Floor 3. Corridor clear. Smoke near 307. No open flame. Over.", "dur": "0:05", "ts": _ts(200), "signal": 85},
    {"id": 8,  "sender": "Fire Response",   "ch": "CH-4  FIRE",     "msg": "Fire Response moving in. Deploying extinguishers. Stand clear.",   "dur": "0:04", "ts": _ts(175), "signal": 82},
    {"id": 9,  "sender": "Floor Manager",   "ch": "CH-5  MGMT",     "msg": "14 evacuated, 2 unaccounted. Checking 311 and 312 now.",           "dur": "0:04", "ts": _ts(145), "signal": 89},
    {"id": 10, "sender": "Fire Response",   "ch": "CH-4  FIRE",     "msg": "Fire contained. Electrical fault, Room 307. Ventilating now.",     "dur": "0:05", "ts": _ts(90),  "signal": 94},
    {"id": 11, "sender": "Security Alpha",  "ch": "CH-2  SECURITY", "msg": "Floor 3 clear. All 16 guests accounted for. Over and out.",        "dur": "0:04", "ts": _ts(55),  "signal": 90},
    {"id": 12, "sender": "Command Center",  "ch": "CH-1  COMMAND",  "msg": "Outstanding work team. Incident resolved. Return to base.",        "dur": "0:04", "ts": _ts(20),  "signal": 96},
]

# ── Session init ──
if "radio_log"      not in st.session_state: st.session_state.radio_log      = list(DEMO_LOG)
if "radio_counter"  not in st.session_state: st.session_state.radio_counter  = len(DEMO_LOG) + 1
if "radio_user"     not in st.session_state: st.session_state.radio_user     = "Command Center"
if "radio_channel"  not in st.session_state: st.session_state.radio_channel  = "CH-1  COMMAND"
if "ptt_active"     not in st.session_state: st.session_state.ptt_active     = False
if "last_tx"        not in st.session_state: st.session_state.last_tx        = None

# ── Header ──
st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:18px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">📻 Radio Comms</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        PUSH-TO-TALK &nbsp;•&nbsp; MULTI-CHANNEL &nbsp;•&nbsp; BROADCAST LOG &nbsp;•&nbsp; WAVEFORM
    </div>
</div>
""", unsafe_allow_html=True)

col_radio, col_log = st.columns([1, 2])

# ════════════════════════════════
#  LEFT — Radio unit
# ════════════════════════════════
with col_radio:

    cur_ch   = CHANNELS[st.session_state.radio_channel]
    cur_user = RESPONDERS[st.session_state.radio_user]

    # Radio body HTML
    is_ptt   = st.session_state.ptt_active
    ptt_col  = "#ff4b4b" if is_ptt else "#1e2a3a"
    ptt_glow = "0 0 24px rgba(255,75,75,0.6)" if is_ptt else "none"
    tx_label = "● TRANSMITTING" if is_ptt else "○ STANDBY"
    tx_color = "#ff4b4b" if is_ptt else "#7a8ba8"

    # Animated waveform bars
    bars = 36
    wave_html = ""
    for i in range(bars):
        if is_ptt:
            h  = random.randint(10, 38)
            op = "1.0"
            spd = f"{0.2 + (i % 6) * 0.07:.2f}s"
            anim = f"animation:wave {spd} ease-in-out infinite alternate;"
        else:
            h  = 4
            op = "0.3"
            anim = ""
        wave_html += (
            f'<div style="width:4px;background:{cur_ch["color"]};border-radius:2px;'
            f'height:{h}px;opacity:{op};{anim}"></div>'
        )

    signal_pct = random.randint(78, 98)
    bars_lit   = round(signal_pct / 10)

    signal_bars = "".join([
        f'<div style="width:5px;border-radius:1px;background:{"#00c853" if j < bars_lit else "#1e2a3a"};'
        f'height:{8 + j * 3}px;"></div>'
        for j in range(10)
    ])

    components.html(f"""
    <!DOCTYPE html><html><head>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
      * {{ box-sizing:border-box; margin:0; padding:0; }}
      body {{ background:#0d1117; display:flex; justify-content:center; padding:8px; }}
      @keyframes wave {{
        from {{ transform: scaleY(0.4); opacity:0.6; }}
        to   {{ transform: scaleY(1.0); opacity:1.0; }}
      }}
      @keyframes blink {{ 0%,100%{{opacity:1;}} 50%{{opacity:0.2;}} }}
      @keyframes glow  {{
        0%,100% {{ box-shadow: 0 0 20px rgba(255,75,75,0.4); }}
        50%     {{ box-shadow: 0 0 40px rgba(255,75,75,0.8); }}
      }}
    </style>
    </head><body>
    <div style="background:#111620;border:1px solid #1e2a3a;border-radius:16px;
                padding:20px 18px;width:100%;max-width:320px;font-family:'JetBrains Mono',monospace;">

      <!-- LCD display -->
      <div style="background:#060d0a;border:1px solid #0d2a1a;border-radius:8px;
                  padding:14px 16px;margin-bottom:16px;">
        <div style="font-size:9px;color:#00c853;letter-spacing:2px;margin-bottom:6px;opacity:0.7;">
          ResQSync TACTICAL RADIO v2
        </div>
        <div style="font-size:16px;font-weight:700;color:{cur_ch['color']};letter-spacing:1px;">
          {st.session_state.radio_channel}
        </div>
        <div style="font-size:10px;color:#00c853;opacity:0.7;margin-top:2px;">
          {cur_ch['freq']}  ·  {cur_ch['desc']}
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px;">
          <span style="font-size:11px;color:{tx_color};
                       {'animation:blink 0.8s infinite;' if is_ptt else ''}">{tx_label}</span>
          <div style="display:flex;gap:3px;align-items:flex-end;">{signal_bars}</div>
        </div>
      </div>

      <!-- Waveform -->
      <div style="background:#060d0a;border:1px solid #0d2a1a;border-radius:8px;
                  height:60px;display:flex;align-items:center;justify-content:center;
                  gap:3px;margin-bottom:16px;padding:0 10px;overflow:hidden;">
        {wave_html}
      </div>

      <!-- User / channel info -->
      <div style="display:flex;gap:10px;margin-bottom:16px;">
        <div style="flex:1;background:#0a0e14;border:1px solid #1e2a3a;border-radius:6px;padding:10px;">
          <div style="font-size:9px;color:#555;letter-spacing:1px;margin-bottom:4px;">OPERATOR</div>
          <div style="font-size:11px;color:{cur_user['color']};font-weight:700;">
            {cur_user['icon']} {st.session_state.radio_user}
          </div>
        </div>
        <div style="flex:1;background:#0a0e14;border:1px solid #1e2a3a;border-radius:6px;padding:10px;">
          <div style="font-size:9px;color:#555;letter-spacing:1px;margin-bottom:4px;">SIGNAL</div>
          <div style="font-size:16px;font-weight:700;color:#00c853;">{signal_pct}%</div>
        </div>
      </div>

      <!-- PTT button -->
      <div style="display:flex;justify-content:center;padding:6px 0 4px;">
        <div style="width:110px;height:110px;border-radius:50%;
                    background:{'radial-gradient(circle,#ff4b4b,#990000)' if is_ptt else 'radial-gradient(circle,#1e2a3a,#0d1117)'};
                    border:3px solid {ptt_col};
                    box-shadow:{ptt_glow};
                    display:flex;flex-direction:column;align-items:center;justify-content:center;
                    {'animation:glow 0.6s infinite;' if is_ptt else ''}">
          <div style="font-size:26px;">{'🔴' if is_ptt else '🎙️'}</div>
          <div style="font-size:10px;font-weight:700;color:{'#ff4b4b' if is_ptt else '#555'};
                      margin-top:4px;letter-spacing:1px;">
            {'TX ACTIVE' if is_ptt else 'PUSH TO TX'}
          </div>
        </div>
      </div>

    </div>
    </body></html>
    """, height=430, scrolling=False)

    # Controls below component
    st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)

    # Operator & channel pickers
    sel_user = st.selectbox("Operator", list(RESPONDERS.keys()),
                            index=list(RESPONDERS.keys()).index(st.session_state.radio_user),
                            label_visibility="collapsed")
    if sel_user != st.session_state.radio_user:
        st.session_state.radio_user = sel_user
        st.rerun()

    sel_ch = st.selectbox("Channel", list(CHANNELS.keys()),
                          index=list(CHANNELS.keys()).index(st.session_state.radio_channel),
                          label_visibility="collapsed")
    if sel_ch != st.session_state.radio_channel:
        st.session_state.radio_channel = sel_ch
        st.session_state.ptt_active = False
        st.rerun()

    # PTT message input
    ptt_text = st.text_input("Broadcast message",
                             placeholder="Type message to broadcast...",
                             label_visibility="collapsed",
                             key="ptt_input")

    ptt_col1, ptt_col2 = st.columns(2)
    with ptt_col1:
        if st.button("🎙️ Transmit", use_container_width=True, type="primary"):
            if ptt_text.strip():
                st.session_state.radio_log.append({
                    "id":     st.session_state.radio_counter,
                    "sender": st.session_state.radio_user,
                    "ch":     st.session_state.radio_channel,
                    "msg":    ptt_text.strip(),
                    "dur":    f"0:0{random.randint(2,6)}",
                    "ts":     datetime.now().strftime("%H:%M:%S"),
                    "signal": random.randint(78, 98),
                })
                st.session_state.radio_counter += 1
                st.session_state.ptt_active = True
                st.session_state.last_tx    = ptt_text.strip()
                st.rerun()

    with ptt_col2:
        if st.button("📡 Incoming", use_container_width=True):
            sim_senders = [k for k in RESPONDERS if k != st.session_state.radio_user]
            sim_chs     = list(CHANNELS.keys())
            sim_msgs = [
                "Requesting backup on Floor 2 corridor. Over.",
                "All exits confirmed clear. Guest assembly complete. Over.",
                "Fire extinguisher deployed. Smoke dissipating. Over.",
                "Medical: no injuries at assembly point. Over.",
                "Elevator bank offline on Floor 3. Use stairs. Over.",
                "Perimeter secured. No secondary threats. Over.",
                "Water supply confirmed active. Sprinklers armed. Over.",
                "Guest with medical condition escorted to lobby. Over.",
            ]
            s = random.choice(sim_senders)
            m = random.choice(sim_msgs)
            c = st.session_state.radio_channel
            st.session_state.radio_log.append({
                "id":     st.session_state.radio_counter,
                "sender": s,
                "ch":     c,
                "msg":    m,
                "dur":    f"0:0{random.randint(2,5)}",
                "ts":     datetime.now().strftime("%H:%M:%S"),
                "signal": random.randint(75, 95),
            })
            st.session_state.radio_counter += 1
            st.session_state.ptt_active = False
            st.rerun()

    if st.session_state.ptt_active and st.session_state.last_tx:
        st.markdown(f"""
        <div style="background:rgba(255,75,75,0.08);border:1px solid rgba(255,75,75,0.3);
                    border-radius:6px;padding:8px 10px;margin-top:6px;text-align:center;">
            <div style="font-size:10px;color:#ff4b4b;font-weight:600;">📡 LAST TRANSMISSION</div>
            <div style="font-size:11px;color:#aab4c8;margin-top:3px;">
                "{st.session_state.last_tx[:60]}{'…' if len(st.session_state.last_tx)>60 else ''}"
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════
#  RIGHT — Broadcast log
# ════════════════════════════════
with col_log:

    # Channel filter + stats row
    hdr_c1, hdr_c2 = st.columns([2, 1])
    with hdr_c1:
        filter_ch = st.selectbox("Filter channel", ["All Channels"] + list(CHANNELS.keys()),
                                 label_visibility="collapsed")
    with hdr_c2:
        if st.button("🗑️ Clear Log", use_container_width=True):
            st.session_state.radio_log     = []
            st.session_state.radio_counter = 1
            st.session_state.ptt_active    = False
            st.rerun()

    # Quick-broadcast buttons
    st.markdown('<div style="font-size:10px;color:#555;letter-spacing:1px;margin:6px 0 6px;'
                'font-family:\'JetBrains Mono\',monospace;">QUICK BROADCAST</div>',
                unsafe_allow_html=True)
    qb_cols = st.columns(4)
    quick_broadcasts = [
        ("✅ Copy that",    "Copy that. Understood. Over."),
        ("📍 On scene",     "On scene. Assessing situation. Over."),
        ("⚠️ Stand by",    "All units stand by. Over."),
        ("🔒 Secure",       "Area secured. No threats. Over."),
        ("🏥 Medic needed", "Medical assistance required at my location. Over."),
        ("🚪 Evacuate",     "Initiating evacuation. All units assist. Over."),
        ("🔥 Fire out",     "Fire extinguished. Area safe. Over."),
        ("📻 All clear",    "All clear. Incident resolved. Return to base. Over."),
    ]
    for i, (label, qtext) in enumerate(quick_broadcasts):
        with qb_cols[i % 4]:
            if st.button(label, use_container_width=True, key=f"qb_{i}"):
                st.session_state.radio_log.append({
                    "id":     st.session_state.radio_counter,
                    "sender": st.session_state.radio_user,
                    "ch":     st.session_state.radio_channel,
                    "msg":    qtext,
                    "dur":    f"0:0{random.randint(2,4)}",
                    "ts":     datetime.now().strftime("%H:%M:%S"),
                    "signal": random.randint(85, 98),
                })
                st.session_state.radio_counter += 1
                st.session_state.ptt_active = True
                st.session_state.last_tx    = qtext
                st.rerun()

    # Transmission count badge
    filtered_log = (st.session_state.radio_log if filter_ch == "All Channels"
                    else [m for m in st.session_state.radio_log if m["ch"] == filter_ch])

    total_tx   = len(st.session_state.radio_log)
    active_chs = len({m["ch"] for m in st.session_state.radio_log})
    my_tx      = sum(1 for m in st.session_state.radio_log if m["sender"] == st.session_state.radio_user)

    m1, m2, m3 = st.columns(3)
    for col, label, val, color in [
        (m1, "TRANSMISSIONS", total_tx,   "#e8edf5"),
        (m2, "ACTIVE CHANNELS", active_chs, "#00bfff"),
        (m3, "YOUR TX",       my_tx,     "#ff8c00"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:7px;
                        padding:10px;text-align:center;margin:8px 0;">
                <div style="font-size:9px;color:#7a8ba8;letter-spacing:1.5px;">{label}</div>
                <div style="font-size:20px;font-weight:700;color:{color};margin-top:2px;">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    # Build transmission log HTML
    if not filtered_log:
        st.markdown("""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;
                    padding:40px;text-align:center;color:#7a8ba8;">
            <div style="font-size:36px;margin-bottom:10px;">📻</div>
            <div>No transmissions on this channel</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        entries_html = ""
        for tx in reversed(filtered_log):
            r_info  = RESPONDERS.get(tx["sender"], {"color": "#7a8ba8", "icon": "👤"})
            ch_info = CHANNELS.get(tx["ch"], {"color": "#7a8ba8", "icon": "📻"})
            is_me   = tx["sender"] == st.session_state.radio_user
            sig     = tx.get("signal", 85)
            sig_col = "#00c853" if sig >= 90 else "#ffd700" if sig >= 75 else "#ff4b4b"

            # Mini signal bars
            sig_bars_lit = round(sig / 10)
            sig_bars = "".join([
                f'<div style="width:3px;height:{5+j*2}px;border-radius:1px;'
                f'background:{"#00c853" if j < sig_bars_lit else "#1e2a3a"};"></div>'
                for j in range(10)
            ])

            # Tiny waveform for each tx
            mini_wave = "".join([
                f'<div style="width:2px;height:{random.randint(4,16)}px;'
                f'background:{r_info["color"]};border-radius:1px;opacity:0.6;"></div>'
                for _ in range(24)
            ])

            highlight = f"border-left:3px solid {r_info['color']};" if is_me else ""
            entries_html += f"""
            <div style="background:#151b28;border:1px solid #1e2a3a;{highlight}
                        border-radius:7px;padding:11px 14px;margin-bottom:8px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap;">
                <span style="font-size:13px;">{r_info['icon']}</span>
                <span style="font-size:12px;font-weight:700;color:{r_info['color']};">{tx['sender']}</span>
                <span style="font-size:9px;background:{ch_info['color']}22;
                             border:1px solid {ch_info['color']}44;color:{ch_info['color']};
                             padding:1px 7px;border-radius:8px;font-family:'JetBrains Mono',monospace;">
                  {ch_info['icon']} {tx['ch']}
                </span>
                <span style="margin-left:auto;font-size:9px;color:#555;
                             font-family:'JetBrains Mono',monospace;">{tx['ts']}</span>
              </div>
              <div style="font-size:12px;color:#e8edf5;margin-bottom:8px;line-height:1.5;">{tx['msg']}</div>
              <div style="display:flex;align-items:center;gap:12px;">
                <div style="display:flex;gap:2px;align-items:flex-end;">{sig_bars}</div>
                <span style="font-size:9px;color:{sig_col};font-family:'JetBrains Mono',monospace;">
                  {sig}% signal
                </span>
                <div style="display:flex;gap:1px;align-items:center;margin-left:4px;">{mini_wave}</div>
                <span style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-left:auto;">
                  ⏱ {tx['dur']}
                </span>
              </div>
            </div>
            """

        log_html = f"""
        <!DOCTYPE html><html><head>
        <style>
          @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;600;700&display=swap');
          * {{ box-sizing:border-box; margin:0; padding:0; }}
          body {{ background:#0d1117; padding:4px; overflow-y:auto; font-family:'Inter',sans-serif; }}
          ::-webkit-scrollbar {{ width:5px; }}
          ::-webkit-scrollbar-track {{ background:#0d1117; }}
          ::-webkit-scrollbar-thumb {{ background:#1e2a3a; border-radius:3px; }}
        </style></head><body>
        {entries_html}
        </body></html>
        """
        components.html(log_html, height=520, scrolling=True)
