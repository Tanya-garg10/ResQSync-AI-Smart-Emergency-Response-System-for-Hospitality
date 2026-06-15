"""
Live Notifications – Real-time alert popups, SMS/push delivery receipts, notification history
"""
import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Notifications | ResQSync AI", page_icon="🔔", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
</style>
""", unsafe_allow_html=True)

# ── Data helpers ──
def _ts(s=0):
    return (datetime.now() - timedelta(seconds=s)).strftime("%H:%M:%S")

def _ago(s=0):
    if s < 60:   return f"{s}s ago"
    if s < 3600: return f"{s//60}m {s%60}s ago"
    return f"{s//3600}h ago"

CHANNELS = {
    "SMS":   {"icon": "💬", "color": "#00c853"},
    "Push":  {"icon": "📲", "color": "#00bfff"},
    "Email": {"icon": "📧", "color": "#ffd700"},
    "Call":  {"icon": "📞", "color": "#ff8c00"},
    "Radio": {"icon": "📻", "color": "#a78bfa"},
}

RECIPIENTS = [
    {"name": "Rohan Sharma (Guest 307)",    "role": "Guest",       "icon": "👤", "color": "#e8edf5"},
    {"name": "Priya Singh (Floor Manager)", "role": "Staff",       "icon": "🏨", "color": "#ffd700"},
    {"name": "Security Alpha",              "role": "Responder",   "icon": "🛡️", "color": "#00bfff"},
    {"name": "Medical Unit 1",              "role": "Responder",   "icon": "🏥", "color": "#00c853"},
    {"name": "Fire Response Team",          "role": "Responder",   "icon": "🔥", "color": "#ff4b4b"},
    {"name": "Hotel Manager (Anil Mehta)",  "role": "Management",  "icon": "👔", "color": "#ff8c00"},
    {"name": "Emergency Services (112)",    "role": "Authority",   "icon": "🚑", "color": "#ff4b4b"},
    {"name": "Command Center",              "role": "Command",     "icon": "📡", "color": "#ff8c00"},
]

STATUS_OPTIONS = ["DELIVERED", "DELIVERED", "DELIVERED", "READ", "READ", "PENDING", "FAILED"]

DEMO_NOTIFICATIONS = [
    {
        "id": 1, "ts": _ts(310), "ago": _ago(310),
        "type": "CRITICAL_ALERT",
        "title": "🚨 CRITICAL — Fire Emergency",
        "body": "Fire detected at Floor 3, Room 307. Immediate evacuation required.",
        "recipient": RECIPIENTS[0], "channel": "SMS",   "status": "READ",
        "severity": "CRITICAL", "sev_color": "#ff4b4b",
    },
    {
        "id": 2, "ts": _ts(308), "ago": _ago(308),
        "type": "RESPONDER_DISPATCH",
        "title": "📡 Responder Dispatched",
        "body": "Security Alpha dispatched to Floor 3. ETA 45 seconds.",
        "recipient": RECIPIENTS[2], "channel": "Push",  "status": "DELIVERED",
        "severity": "HIGH", "sev_color": "#ff8c00",
    },
    {
        "id": 3, "ts": _ts(305), "ago": _ago(305),
        "type": "CRITICAL_ALERT",
        "title": "🔥 Fire Alert — Management",
        "body": "Fire emergency on Floor 3. Response teams mobilized. Guests being evacuated.",
        "recipient": RECIPIENTS[5], "channel": "Call",  "status": "READ",
        "severity": "CRITICAL", "sev_color": "#ff4b4b",
    },
    {
        "id": 4, "ts": _ts(300), "ago": _ago(300),
        "type": "EVACUATION",
        "title": "🚶 Evacuation Order — Floor 3",
        "body": "Please evacuate Floor 3 immediately. Use staircases. Do not use elevators.",
        "recipient": RECIPIENTS[1], "channel": "Push",  "status": "READ",
        "severity": "CRITICAL", "sev_color": "#ff4b4b",
    },
    {
        "id": 5, "ts": _ts(295), "ago": _ago(295),
        "type": "AUTHORITY_CONTACT",
        "title": "🚑 Emergency Services Alerted",
        "body": "Automated call placed to 112. Fire brigade and ambulance dispatched.",
        "recipient": RECIPIENTS[6], "channel": "Call",  "status": "DELIVERED",
        "severity": "CRITICAL", "sev_color": "#ff4b4b",
    },
    {
        "id": 6, "ts": _ts(280), "ago": _ago(280),
        "type": "STATUS_UPDATE",
        "title": "📊 Status Update — Responders On Scene",
        "body": "Security Alpha and Fire Response team on scene. Containment in progress.",
        "recipient": RECIPIENTS[5], "channel": "SMS",   "status": "READ",
        "severity": "HIGH", "sev_color": "#ff8c00",
    },
    {
        "id": 7, "ts": _ts(200), "ago": _ago(200),
        "type": "STATUS_UPDATE",
        "title": "✅ Evacuation Complete",
        "body": "All 16 guests safely evacuated from Floor 3. No casualties reported.",
        "recipient": RECIPIENTS[5], "channel": "Push",  "status": "READ",
        "severity": "MODERATE", "sev_color": "#ffd700",
    },
    {
        "id": 8, "ts": _ts(100), "ago": _ago(100),
        "type": "STATUS_UPDATE",
        "title": "🔒 Fire Contained",
        "body": "Fire extinguished. Cause: electrical fault Room 307. Structural check underway.",
        "recipient": RECIPIENTS[5], "channel": "Email", "status": "DELIVERED",
        "severity": "MODERATE", "sev_color": "#ffd700",
    },
    {
        "id": 9, "ts": _ts(30), "ago": _ago(30),
        "type": "RESOLVED",
        "title": "🟢 Incident Resolved — All Clear",
        "body": "Incident #3821 marked RESOLVED. All responders returning to base.",
        "recipient": RECIPIENTS[7], "channel": "Push",  "status": "READ",
        "severity": "LOW", "sev_color": "#00c853",
    },
]

# ── Session init ──
if "notif_log"     not in st.session_state: st.session_state.notif_log     = list(DEMO_NOTIFICATIONS)
if "notif_counter" not in st.session_state: st.session_state.notif_counter = len(DEMO_NOTIFICATIONS) + 1
if "notif_unread"  not in st.session_state: st.session_state.notif_unread  = 3

# ── Header ──
unread = sum(1 for n in st.session_state.notif_log if n["status"] in ("PENDING", "DELIVERED"))
st.markdown(f"""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;
            display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
  <div>
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">🔔 Live Notifications</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
      SMS &nbsp;•&nbsp; PUSH &nbsp;•&nbsp; EMAIL &nbsp;•&nbsp; CALL &nbsp;•&nbsp; RADIO &nbsp;•&nbsp; DELIVERY RECEIPTS
    </div>
  </div>
  <div style="background:rgba(255,75,75,0.12);border:1px solid rgba(255,75,75,0.35);
              border-radius:20px;padding:6px 16px;font-size:12px;font-weight:700;color:#ff4b4b;">
    {unread} unread
  </div>
</div>
""", unsafe_allow_html=True)

# ── Stat cards ──
total_n   = len(st.session_state.notif_log)
delivered = sum(1 for n in st.session_state.notif_log if n["status"] in ("DELIVERED","READ"))
read_n    = sum(1 for n in st.session_state.notif_log if n["status"] == "READ")
failed_n  = sum(1 for n in st.session_state.notif_log if n["status"] == "FAILED")
rate      = round(delivered / total_n * 100) if total_n else 0

mc = st.columns(5)
for col, lbl, val, color in zip(mc,
    ["TOTAL SENT", "DELIVERED", "READ", "FAILED", "DELIVERY RATE"],
    [total_n, delivered, read_n, failed_n, f"{rate}%"],
    ["#e8edf5", "#00bfff", "#00c853", "#ff4b4b", "#ffd700"]):
    with col:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;
                    padding:14px;text-align:center;">
          <div style="font-size:22px;font-weight:800;color:{color};
                      font-family:'JetBrains Mono',monospace;">{val}</div>
          <div style="font-size:9px;color:#555;letter-spacing:1.5px;margin-top:4px;">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# ── Main layout ──
col_send, col_feed = st.columns([1, 2])

# ════════════════════════════════
#  LEFT — Compose & send
# ════════════════════════════════
with col_send:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:10px;'
                'font-family:\'JetBrains Mono\',monospace;">SEND NOTIFICATION</div>',
                unsafe_allow_html=True)

    notif_title = st.text_input("Title", placeholder="Alert title…", label_visibility="collapsed",
                                key="notif_title_inp")
    notif_body  = st.text_area("Message", placeholder="Notification message…",
                               height=80, label_visibility="collapsed", key="notif_body_inp")

    sel_rec = st.selectbox("Recipient", [r["name"] for r in RECIPIENTS],
                           label_visibility="collapsed")
    sel_ch  = st.selectbox("Channel",   list(CHANNELS.keys()),
                           label_visibility="collapsed")
    sel_sev = st.selectbox("Severity",  ["LOW", "MODERATE", "HIGH", "CRITICAL"],
                           label_visibility="collapsed")

    sev_colors = {"LOW": "#00c853", "MODERATE": "#ffd700", "HIGH": "#ff8c00", "CRITICAL": "#ff4b4b"}

    if st.button("📤 Send Notification", use_container_width=True, type="primary"):
        if notif_title.strip() and notif_body.strip():
            rec_obj = next((r for r in RECIPIENTS if r["name"] == sel_rec), RECIPIENTS[0])
            st.session_state.notif_log.insert(0, {
                "id":        st.session_state.notif_counter,
                "ts":        datetime.now().strftime("%H:%M:%S"),
                "ago":       "just now",
                "type":      "MANUAL",
                "title":     notif_title.strip(),
                "body":      notif_body.strip(),
                "recipient": rec_obj,
                "channel":   sel_ch,
                "status":    "PENDING",
                "severity":  sel_sev,
                "sev_color": sev_colors[sel_sev],
            })
            st.session_state.notif_counter += 1
            st.rerun()

    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin:14px 0 8px;'
                'font-family:\'JetBrains Mono\',monospace;">QUICK ALERTS</div>',
                unsafe_allow_html=True)

    quick_alerts = [
        ("🚨 Fire Alert",       "🚨 FIRE ALERT",     "Fire emergency detected. Evacuate immediately!",           "CRITICAL"),
        ("🏥 Medical Emergency","🏥 MEDICAL",         "Medical emergency reported. Medical team dispatched.",      "HIGH"),
        ("🔒 All Clear",        "✅ ALL CLEAR",       "Incident resolved. All clear. Return to normal operations.","LOW"),
        ("⚠️ Suspicious Activity","⚠️ SECURITY ALERT","Suspicious activity reported. Security team responding.",  "HIGH"),
        ("🌊 Flood Warning",    "🌊 FLOOD WARNING",  "Flooding detected in basement. Avoid lower floors.",        "CRITICAL"),
        ("💨 Evacuation Order", "🚶 EVACUATE NOW",   "Evacuation order issued. Use nearest staircase. Stay calm.","CRITICAL"),
    ]
    qc1, qc2 = st.columns(2)
    for i, (btn_label, title, body, sev) in enumerate(quick_alerts):
        with (qc1 if i % 2 == 0 else qc2):
            if st.button(btn_label, use_container_width=True, key=f"qa_{i}"):
                rec_obj = random.choice(RECIPIENTS)
                ch      = random.choice(list(CHANNELS.keys()))
                st.session_state.notif_log.insert(0, {
                    "id":        st.session_state.notif_counter,
                    "ts":        datetime.now().strftime("%H:%M:%S"),
                    "ago":       "just now",
                    "type":      "QUICK",
                    "title":     title,
                    "body":      body,
                    "recipient": rec_obj,
                    "channel":   ch,
                    "status":    "PENDING",
                    "severity":  sev,
                    "sev_color": sev_colors[sev],
                })
                st.session_state.notif_counter += 1
                st.rerun()

    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin:14px 0 8px;'
                'font-family:\'JetBrains Mono\',monospace;">CHANNEL STATUS</div>',
                unsafe_allow_html=True)

    for ch_name, ch_info in CHANNELS.items():
        sent_ch = sum(1 for n in st.session_state.notif_log if n["channel"] == ch_name)
        ok_ch   = sum(1 for n in st.session_state.notif_log
                      if n["channel"] == ch_name and n["status"] in ("DELIVERED","READ"))
        rate_ch = round(ok_ch / sent_ch * 100) if sent_ch else 100
        bar_w   = rate_ch
        bar_col = "#00c853" if rate_ch >= 90 else "#ffd700" if rate_ch >= 70 else "#ff4b4b"
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:6px;
                    padding:9px 12px;margin-bottom:5px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;">
            <span style="font-size:12px;color:{ch_info['color']};font-weight:600;">
              {ch_info['icon']} {ch_name}
            </span>
            <span style="font-size:10px;color:{bar_col};font-family:'JetBrains Mono',monospace;">
              {rate_ch}% delivery  ·  {sent_ch} sent
            </span>
          </div>
          <div style="background:#1e2a3a;border-radius:3px;height:4px;overflow:hidden;">
            <div style="background:{bar_col};height:4px;width:{bar_w}%;border-radius:3px;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🗑️ Clear All Notifications", use_container_width=True):
        st.session_state.notif_log     = []
        st.session_state.notif_counter = 1
        st.rerun()

# ════════════════════════════════
#  RIGHT — Live feed
# ════════════════════════════════
with col_feed:
    hdr1, hdr2 = st.columns([2, 1])
    with hdr1:
        filter_ch  = st.selectbox("Filter by channel",
                                  ["All Channels"] + list(CHANNELS.keys()),
                                  label_visibility="collapsed")
    with hdr2:
        filter_st  = st.selectbox("Filter by status",
                                  ["All Statuses", "PENDING", "DELIVERED", "READ", "FAILED"],
                                  label_visibility="collapsed")

    # Simulate delivery — mark first PENDING as DELIVERED
    if st.button("⚡ Simulate Delivery Update", use_container_width=True):
        for n in st.session_state.notif_log:
            if n["status"] == "PENDING":
                n["status"] = "DELIVERED"
                break
        for n in st.session_state.notif_log:
            if n["status"] == "DELIVERED":
                n["status"] = "READ"
                break
        st.rerun()

    log = st.session_state.notif_log
    if filter_ch != "All Channels":
        log = [n for n in log if n["channel"] == filter_ch]
    if filter_st != "All Statuses":
        log = [n for n in log if n["status"] == filter_st]

    if not log:
        st.markdown("""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;
                    padding:40px;text-align:center;color:#7a8ba8;">
          <div style="font-size:36px;margin-bottom:10px;">🔔</div>
          <div>No notifications match the selected filters</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        status_meta = {
            "PENDING":   {"icon": "⏳", "color": "#ffd700", "bg": "rgba(255,215,0,0.06)"},
            "DELIVERED": {"icon": "✓",  "color": "#00bfff", "bg": "rgba(0,191,255,0.06)"},
            "READ":      {"icon": "✓✓", "color": "#00c853", "bg": "rgba(0,200,83,0.06)"},
            "FAILED":    {"icon": "✗",  "color": "#ff4b4b", "bg": "rgba(255,75,75,0.06)"},
        }

        cards_html = ""
        for n in log:
            sm   = status_meta.get(n["status"], status_meta["DELIVERED"])
            ch   = CHANNELS.get(n["channel"], {"icon": "📨", "color": "#7a8ba8"})
            rec  = n["recipient"]

            cards_html += f"""
            <div style="background:#151b28;border:1px solid #1e2a3a;
                        border-left:3px solid {n['sev_color']};
                        border-radius:7px;padding:13px 15px;margin-bottom:9px;
                        background:{sm['bg']};position:relative;">

              <!-- Top row -->
              <div style="display:flex;align-items:flex-start;justify-content:space-between;
                          gap:10px;margin-bottom:6px;">
                <div style="flex:1;min-width:0;">
                  <div style="font-size:13px;font-weight:700;color:#e8edf5;
                              margin-bottom:2px;line-height:1.3;">{n['title']}</div>
                  <div style="font-size:11px;color:#aab4c8;line-height:1.5;">{n['body']}</div>
                </div>
                <div style="text-align:right;flex-shrink:0;">
                  <div style="font-size:16px;font-weight:800;color:{sm['color']};
                              font-family:'JetBrains Mono',monospace;">{sm['icon']}</div>
                  <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;
                              margin-top:2px;white-space:nowrap;">{n['status']}</div>
                </div>
              </div>

              <!-- Bottom row -->
              <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:8px;">
                <!-- Recipient -->
                <span style="font-size:11px;color:{rec['color']};font-weight:600;">
                  {rec['icon']} {rec['name'].split('(')[0].strip()}
                </span>
                <!-- Channel badge -->
                <span style="font-size:10px;background:{ch['color']}22;border:1px solid {ch['color']}44;
                             color:{ch['color']};padding:1px 8px;border-radius:10px;
                             font-family:'JetBrains Mono',monospace;">
                  {ch['icon']} {n['channel']}
                </span>
                <!-- Severity badge -->
                <span style="font-size:9px;background:{n['sev_color']}18;border:1px solid {n['sev_color']}35;
                             color:{n['sev_color']};padding:1px 7px;border-radius:10px;
                             font-family:'JetBrains Mono',monospace;">{n['severity']}</span>
                <!-- Timestamp -->
                <span style="margin-left:auto;font-size:9px;color:#555;
                             font-family:'JetBrains Mono',monospace;">
                  {n['ts']} · {n['ago']}
                </span>
              </div>

            </div>
            """

        feed_html = f"""
        <!DOCTYPE html><html><head>
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
          *{{ box-sizing:border-box; margin:0; padding:0; }}
          body {{ background:#0d1117; padding:4px; overflow-y:auto; font-family:'Inter',sans-serif; }}
          ::-webkit-scrollbar {{ width:5px; }}
          ::-webkit-scrollbar-track {{ background:#0d1117; }}
          ::-webkit-scrollbar-thumb {{ background:#1e2a3a; border-radius:3px; }}
        </style></head><body>
        {cards_html}
        </body></html>
        """
        feed_height = min(len(log) * 115, 600)
        components.html(feed_html, height=max(feed_height, 200), scrolling=True)
