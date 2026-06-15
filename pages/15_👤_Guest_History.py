"""
Guest SOS History – Per-guest alert timeline, check-in status, room details, emergency notes
"""
import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Guest History | ResQSync AI", page_icon="👤", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ──
now = datetime.now()
def _ts(s=0): return (now - timedelta(seconds=s)).strftime("%H:%M:%S")
def _date(d=0): return (now - timedelta(days=d)).strftime("%b %d, %Y")

GUESTS = [
    {
        "id": "G-307",
        "name": "Rohan Sharma",
        "room": "307",
        "floor": 3,
        "check_in":  _date(2),
        "check_out": _date(-1),
        "status": "CHECKED IN",
        "nationality": "🇮🇳 Indian",
        "phone": "+91 98765 43210",
        "emergency_contact": "Priya Sharma (Wife) · +91 98700 11122",
        "notes": "Diabetic — insulin in room safe. VIP loyalty member.",
        "avatar": "RS",
        "avatar_color": "#ff4b4b",
        "sos_count": 1,
        "alerts": [
            {
                "id": "SOS-3821", "ts": _ts(310), "type": "FIRE",
                "description": "Fire alarm triggered. Smoke detected in north corridor.",
                "severity": "CRITICAL", "sev_color": "#ff4b4b",
                "status": "RESOLVED", "response_time": "4m 50s",
                "responder": "Fire Response + Security Alpha",
                "outcome": "Guest safely evacuated. No injuries.",
                "photo": True,
            },
        ],
    },
    {
        "id": "G-412",
        "name": "Aisha Khan",
        "room": "412",
        "floor": 4,
        "check_in":  _date(1),
        "check_out": _date(-2),
        "status": "CHECKED IN",
        "nationality": "🇦🇪 UAE",
        "phone": "+971 50 123 4567",
        "emergency_contact": "Ahmed Khan (Husband) · +971 50 987 6543",
        "notes": "Requested late checkout. Nut allergy — flagged with F&B.",
        "avatar": "AK",
        "avatar_color": "#00bfff",
        "sos_count": 2,
        "alerts": [
            {
                "id": "SOS-3790", "ts": _ts(86400), "type": "MEDICAL",
                "description": "Guest reported dizziness and shortness of breath.",
                "severity": "HIGH", "sev_color": "#ff8c00",
                "status": "RESOLVED", "response_time": "3m 12s",
                "responder": "Medical Unit 1",
                "outcome": "Minor allergic reaction. Antihistamine administered. Guest stable.",
                "photo": False,
            },
            {
                "id": "SOS-3810", "ts": _ts(3600), "type": "SECURITY",
                "description": "Reported suspicious individual loitering near room.",
                "severity": "MODERATE", "sev_color": "#ffd700",
                "status": "RESOLVED", "response_time": "2m 05s",
                "responder": "Security Alpha",
                "outcome": "Area checked and cleared. No threat found.",
                "photo": False,
            },
        ],
    },
    {
        "id": "G-201",
        "name": "David Chen",
        "room": "201",
        "floor": 2,
        "check_in":  _date(3),
        "check_out": _date(-1),
        "status": "CHECKED IN",
        "nationality": "🇨🇳 Chinese",
        "phone": "+86 138 0013 8000",
        "emergency_contact": "Lin Chen (Mother) · +86 138 5555 1234",
        "notes": "Business traveller. Requires Mandarin-speaking staff if available.",
        "avatar": "DC",
        "avatar_color": "#00c853",
        "sos_count": 0,
        "alerts": [],
    },
    {
        "id": "G-515",
        "name": "Sarah Williams",
        "room": "515",
        "floor": 5,
        "check_in":  _date(0),
        "check_out": _date(-3),
        "status": "CHECKED IN",
        "nationality": "🇬🇧 British",
        "phone": "+44 7700 900123",
        "emergency_contact": "Tom Williams (Partner) · +44 7700 900456",
        "notes": "Honeymoon package. Do not disturb unless emergency.",
        "avatar": "SW",
        "avatar_color": "#a78bfa",
        "sos_count": 1,
        "alerts": [
            {
                "id": "SOS-3800", "ts": _ts(7200), "type": "MEDICAL",
                "description": "Guest called for assistance — severe headache and nausea.",
                "severity": "MODERATE", "sev_color": "#ffd700",
                "status": "RESOLVED", "response_time": "5m 30s",
                "responder": "Medical Unit 1",
                "outcome": "Paracetamol provided. Guest resting. Follow-up scheduled.",
                "photo": False,
            },
        ],
    },
    {
        "id": "G-108",
        "name": "Mikhail Petrov",
        "room": "108",
        "floor": 1,
        "check_in":  _date(5),
        "check_out": _date(-0),
        "status": "CHECKED OUT",
        "nationality": "🇷🇺 Russian",
        "phone": "+7 495 000 0000",
        "emergency_contact": "Olga Petrov (Wife) · +7 495 111 2222",
        "notes": "Frequent guest. Gold member. Prefers non-smoking floor.",
        "avatar": "MP",
        "avatar_color": "#ffd700",
        "sos_count": 0,
        "alerts": [],
    },
]

# ── Session state ──
if "selected_guest" not in st.session_state:
    st.session_state.selected_guest = "G-307"
if "guest_notes" not in st.session_state:
    st.session_state.guest_notes = {g["id"]: g["notes"] for g in GUESTS}

# ── Header ──
st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">👤 Guest SOS History</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        PER-GUEST TIMELINE &nbsp;•&nbsp; ALERT HISTORY &nbsp;•&nbsp; CHECK-IN STATUS &nbsp;•&nbsp; EMERGENCY NOTES
    </div>
</div>
""", unsafe_allow_html=True)

# ── Summary stats ──
total_guests  = len(GUESTS)
checked_in    = sum(1 for g in GUESTS if g["status"] == "CHECKED IN")
total_sos     = sum(g["sos_count"] for g in GUESTS)
high_risk     = sum(1 for g in GUESTS if g["sos_count"] >= 2)

mc = st.columns(4)
for col, lbl, val, color in zip(mc,
    ["TOTAL GUESTS", "CHECKED IN", "SOS INCIDENTS", "HIGH RISK GUESTS"],
    [total_guests, checked_in, total_sos, high_risk],
    ["#e8edf5", "#00c853", "#ff8c00", "#ff4b4b"]):
    with col:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;
                    padding:14px;text-align:center;">
          <div style="font-size:26px;font-weight:800;color:{color};
                      font-family:'JetBrains Mono',monospace;">{val}</div>
          <div style="font-size:9px;color:#555;letter-spacing:1.5px;margin-top:4px;">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

col_list, col_detail = st.columns([1, 2])

# ════════════════════════════════
#  LEFT — Guest list
# ════════════════════════════════
with col_list:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:10px;'
                'font-family:\'JetBrains Mono\',monospace;">GUEST DIRECTORY</div>',
                unsafe_allow_html=True)

    search = st.text_input("Search guests", placeholder="🔍  Search by name or room…",
                           label_visibility="collapsed")

    visible = [g for g in GUESTS
               if not search or search.lower() in g["name"].lower()
               or search in g["room"]]

    for g in visible:
        is_sel    = g["id"] == st.session_state.selected_guest
        sos_badge = (f'<span style="background:rgba(255,139,0,0.15);border:1px solid rgba(255,139,0,0.4);'
                     f'color:#ff8c00;font-size:9px;padding:1px 6px;border-radius:8px;'
                     f'font-family:\'JetBrains Mono\',monospace;margin-left:4px;">'
                     f'{g["sos_count"]} SOS</span>'
                     if g["sos_count"] > 0 else "")
        status_col = "#00c853" if g["status"] == "CHECKED IN" else "#555"
        border_col = g["avatar_color"] if is_sel else "#1e2a3a"
        bg_col     = f"rgba({','.join(str(int(g['avatar_color'].lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.08)" if is_sel else "#151b28"

        st.markdown(f"""
        <div style="background:{bg_col};border:1px solid {border_col};border-radius:8px;
                    padding:10px 12px;margin-bottom:7px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;border-radius:50%;flex-shrink:0;
                        background:{g['avatar_color']}22;border:2px solid {g['avatar_color']};
                        display:flex;align-items:center;justify-content:center;
                        font-size:11px;font-weight:700;color:{g['avatar_color']};">
              {g['avatar']}
            </div>
            <div style="flex:1;min-width:0;">
              <div style="font-size:12px;font-weight:700;color:#e8edf5;white-space:nowrap;
                          overflow:hidden;text-overflow:ellipsis;">
                {g['name']}{sos_badge}
              </div>
              <div style="font-size:10px;color:#7a8ba8;margin-top:1px;
                          font-family:'JetBrains Mono',monospace;">
                Room {g['room']} · Floor {g['floor']}
              </div>
            </div>
            <span style="font-size:9px;color:{status_col};font-weight:600;
                         white-space:nowrap;">
              {"●" if g["status"]=="CHECKED IN" else "○"} {g['status'].split()[0]}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"View {g['name'].split()[0]}", key=f"sel_{g['id']}",
                     use_container_width=True):
            st.session_state.selected_guest = g["id"]
            st.rerun()

# ════════════════════════════════
#  RIGHT — Guest detail
# ════════════════════════════════
with col_detail:
    guest = next((g for g in GUESTS if g["id"] == st.session_state.selected_guest), GUESTS[0])
    status_col = "#00c853" if guest["status"] == "CHECKED IN" else "#555"
    risk_level = "HIGH" if guest["sos_count"] >= 2 else "MODERATE" if guest["sos_count"] == 1 else "NONE"
    risk_color = {"HIGH": "#ff4b4b", "MODERATE": "#ffd700", "NONE": "#00c853"}[risk_level]

    # ── Profile card ──
    profile_html = f"""
    <!DOCTYPE html><html><head>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
      *{{ box-sizing:border-box; margin:0; padding:0; }}
      body {{ background:#0d1117; padding:2px; font-family:'Inter',sans-serif; }}
    </style></head><body>

    <div style="background:linear-gradient(135deg,#111620,#151b28);border:1px solid #1e2a3a;
                border-radius:10px;padding:18px 20px;margin-bottom:10px;">
      <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
        <!-- Avatar -->
        <div style="width:56px;height:56px;border-radius:50%;flex-shrink:0;
                    background:{guest['avatar_color']}22;border:2px solid {guest['avatar_color']};
                    display:flex;align-items:center;justify-content:center;
                    font-size:18px;font-weight:800;color:{guest['avatar_color']};">
          {guest['avatar']}
        </div>
        <!-- Name & room -->
        <div style="flex:1;min-width:200px;">
          <div style="font-size:18px;font-weight:800;color:#e8edf5;">{guest['name']}</div>
          <div style="font-size:11px;color:#7a8ba8;margin-top:3px;
                      font-family:'JetBrains Mono',monospace;">
            {guest['id']} &nbsp;·&nbsp; Room {guest['room']} &nbsp;·&nbsp; Floor {guest['floor']}
          </div>
          <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;">
            <span style="font-size:10px;background:{status_col}22;border:1px solid {status_col}55;
                         color:{status_col};padding:2px 10px;border-radius:10px;
                         font-family:'JetBrains Mono',monospace;font-weight:700;">
              ● {guest['status']}
            </span>
            <span style="font-size:10px;background:{risk_color}18;border:1px solid {risk_color}35;
                         color:{risk_color};padding:2px 10px;border-radius:10px;
                         font-family:'JetBrains Mono',monospace;font-weight:700;">
              RISK: {risk_level}
            </span>
            <span style="font-size:10px;background:rgba(0,191,255,0.1);border:1px solid rgba(0,191,255,0.3);
                         color:#00bfff;padding:2px 10px;border-radius:10px;
                         font-family:'JetBrains Mono',monospace;">
              {guest['nationality']}
            </span>
          </div>
        </div>
        <!-- SOS count -->
        <div style="text-align:center;background:#0a0e14;border:1px solid #1e2a3a;
                    border-radius:8px;padding:12px 18px;">
          <div style="font-size:28px;font-weight:800;color:{'#ff4b4b' if guest['sos_count']>0 else '#00c853'};">
            {guest['sos_count']}
          </div>
          <div style="font-size:9px;color:#555;letter-spacing:1px;margin-top:2px;
                      font-family:'JetBrains Mono',monospace;">SOS TOTAL</div>
        </div>
      </div>

      <!-- Detail grid -->
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:14px;">
        <div style="background:#0a0e14;border-radius:6px;padding:10px;">
          <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:4px;">CHECK-IN</div>
          <div style="font-size:11px;color:#e8edf5;font-weight:600;">{guest['check_in']}</div>
        </div>
        <div style="background:#0a0e14;border-radius:6px;padding:10px;">
          <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:4px;">CHECK-OUT</div>
          <div style="font-size:11px;color:#e8edf5;font-weight:600;">{guest['check_out']}</div>
        </div>
        <div style="background:#0a0e14;border-radius:6px;padding:10px;">
          <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:4px;">PHONE</div>
          <div style="font-size:11px;color:#00bfff;font-weight:600;">{guest['phone']}</div>
        </div>
      </div>

      <!-- Emergency contact -->
      <div style="background:#0a0e14;border:1px solid rgba(255,75,75,0.2);border-radius:6px;
                  padding:10px 14px;margin-top:10px;">
        <div style="font-size:9px;color:#ff4b4b;font-family:'JetBrains Mono',monospace;
                    margin-bottom:4px;letter-spacing:1px;">🚨 EMERGENCY CONTACT</div>
        <div style="font-size:11px;color:#e8edf5;">{guest['emergency_contact']}</div>
      </div>
    </div>

    </body></html>
    """
    components.html(profile_html, height=310, scrolling=False)

    # ── Notes editor ──
    note_key = f"note_{guest['id']}"
    current_note = st.session_state.guest_notes.get(guest["id"], guest["notes"])

    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:8px;'
                'font-family:\'JetBrains Mono\',monospace;">📝 STAFF NOTES</div>',
                unsafe_allow_html=True)

    note_col1, note_col2 = st.columns([4, 1])
    with note_col1:
        new_note = st.text_area("Staff notes", value=current_note, height=72,
                                label_visibility="collapsed", key=note_key)
    with note_col2:
        if st.button("💾 Save", use_container_width=True):
            st.session_state.guest_notes[guest["id"]] = new_note
            st.success("Saved!")

    # ── Alert timeline ──
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin:12px 0 8px;'
                'font-family:\'JetBrains Mono\',monospace;">🚨 SOS / ALERT TIMELINE</div>',
                unsafe_allow_html=True)

    if not guest["alerts"]:
        st.markdown("""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;
                    padding:28px;text-align:center;">
          <div style="font-size:28px;margin-bottom:8px;">✅</div>
          <div style="font-size:13px;font-weight:600;color:#00c853;">No incidents recorded</div>
          <div style="font-size:11px;color:#555;margin-top:4px;">
            This guest has had a clean, incident-free stay.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        type_icons = {"FIRE": "🔥", "MEDICAL": "🏥", "SECURITY": "🛡️"}

        alert_cards = ""
        for a in guest["alerts"]:
            icon = type_icons.get(a["type"], "⚠️")
            photo_badge = ('<span style="background:rgba(0,200,83,0.12);border:1px solid rgba(0,200,83,0.35);'
                          'color:#00c853;font-size:9px;padding:1px 7px;border-radius:8px;'
                          'font-family:\'JetBrains Mono\',monospace;">📸 Photo</span>'
                          if a["photo"] else "")
            alert_cards += f"""
            <div style="background:#151b28;border:1px solid #1e2a3a;
                        border-left:3px solid {a['sev_color']};
                        border-radius:7px;padding:14px 16px;margin-bottom:10px;">

              <!-- Header -->
              <div style="display:flex;align-items:center;justify-content:space-between;
                          margin-bottom:8px;gap:10px;flex-wrap:wrap;">
                <div style="display:flex;align-items:center;gap:8px;">
                  <span style="font-size:14px;">{icon}</span>
                  <span style="font-size:13px;font-weight:700;color:#e8edf5;">{a['type']} INCIDENT</span>
                  <span style="font-size:9px;background:{a['sev_color']}18;border:1px solid {a['sev_color']}35;
                               color:{a['sev_color']};padding:1px 7px;border-radius:8px;
                               font-family:'JetBrains Mono',monospace;">{a['severity']}</span>
                  {photo_badge}
                </div>
                <div style="text-align:right;">
                  <div style="font-size:10px;color:#555;font-family:'JetBrains Mono',monospace;">{a['id']}</div>
                  <div style="font-size:10px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;">{a['ts']}</div>
                </div>
              </div>

              <!-- Description -->
              <div style="font-size:12px;color:#aab4c8;margin-bottom:10px;line-height:1.5;">{a['description']}</div>

              <!-- Detail grid -->
              <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:8px;">
                <div style="background:#0a0e14;border-radius:5px;padding:8px;">
                  <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:3px;">STATUS</div>
                  <div style="font-size:11px;font-weight:700;color:#00c853;">{a['status']}</div>
                </div>
                <div style="background:#0a0e14;border-radius:5px;padding:8px;">
                  <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:3px;">RESPONSE TIME</div>
                  <div style="font-size:11px;font-weight:700;color:#00bfff;font-family:'JetBrains Mono',monospace;">{a['response_time']}</div>
                </div>
                <div style="background:#0a0e14;border-radius:5px;padding:8px;">
                  <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:3px;">RESPONDER</div>
                  <div style="font-size:10px;font-weight:600;color:#ff8c00;">{a['responder']}</div>
                </div>
              </div>

              <!-- Outcome -->
              <div style="background:rgba(0,200,83,0.06);border:1px solid rgba(0,200,83,0.2);
                          border-radius:5px;padding:8px 12px;">
                <div style="font-size:9px;color:#00c853;font-family:'JetBrains Mono',monospace;
                            margin-bottom:3px;letter-spacing:1px;">OUTCOME</div>
                <div style="font-size:11px;color:#aab4c8;">{a['outcome']}</div>
              </div>

            </div>
            """

        timeline_html = f"""
        <!DOCTYPE html><html><head>
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
          *{{ box-sizing:border-box; margin:0; padding:0; }}
          body {{ background:#0d1117; padding:2px; overflow-y:auto; font-family:'Inter',sans-serif; }}
          ::-webkit-scrollbar {{ width:5px; }}
          ::-webkit-scrollbar-track {{ background:#0d1117; }}
          ::-webkit-scrollbar-thumb {{ background:#1e2a3a; border-radius:3px; }}
        </style></head><body>
        {alert_cards}
        </body></html>
        """
        components.html(timeline_html,
                        height=min(250 + len(guest["alerts"]) * 220, 600),
                        scrolling=True)

    # ── Add manual note/alert ──
    with st.expander("➕ Add Manual Alert Entry"):
        man_type = st.selectbox("Incident type", ["FIRE", "MEDICAL", "SECURITY"], key="man_type")
        man_desc = st.text_area("Description", placeholder="Brief description of the incident…",
                                height=60, key="man_desc")
        man_sev  = st.selectbox("Severity", ["LOW","MODERATE","HIGH","CRITICAL"], key="man_sev")
        man_resp = st.text_input("Responder assigned", placeholder="e.g. Security Alpha",
                                 key="man_resp")
        if st.button("➕ Log Alert", key="log_alert"):
            if man_desc.strip():
                sev_colors = {"LOW":"#00c853","MODERATE":"#ffd700","HIGH":"#ff8c00","CRITICAL":"#ff4b4b"}
                idx = next(i for i, g in enumerate(GUESTS) if g["id"] == guest["id"])
                GUESTS[idx]["alerts"].insert(0, {
                    "id": f"SOS-{random.randint(3900,3999)}",
                    "ts": datetime.now().strftime("%H:%M:%S"),
                    "type": man_type,
                    "description": man_desc.strip(),
                    "severity": man_sev,
                    "sev_color": sev_colors[man_sev],
                    "status": "ACTIVE",
                    "response_time": "—",
                    "responder": man_resp.strip() or "Unassigned",
                    "outcome": "Pending resolution.",
                    "photo": False,
                })
                GUESTS[idx]["sos_count"] += 1
                st.rerun()
