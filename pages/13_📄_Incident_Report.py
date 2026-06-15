"""
AI Incident Report Generator – Auto-drafted structured report from all incident data
"""
import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime, timedelta
from utils.helpers import incident_icon, severity_color

st.set_page_config(page_title="Incident Report | ResQSync AI", page_icon="📄", layout="wide")

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
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">📄 AI Incident Report</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        AUTO-GENERATED &nbsp;•&nbsp; STRUCTURED &nbsp;•&nbsp; EXPORTABLE
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pull latest incident from session, or use a rich demo ──
now = datetime.now()

if "incidents" in st.session_state and st.session_state.incidents:
    base = st.session_state.incidents[0]
    inc_id       = base.get("id", 3821)
    inc_type     = base.get("type", "FIRE")
    inc_zone     = base.get("zone", "Floor 3, Room 307")
    inc_sev      = base.get("severity", "CRITICAL")
    inc_status   = base.get("status", "RESOLVED")
    inc_score    = base.get("severity_score", round(random.uniform(7.8, 9.5), 1))
    inc_photo    = base.get("photo") is not None
    inc_desc     = base.get("description", f"{inc_type} emergency reported at {inc_zone}.")
    trigger_time = base.get("timestamp", now.strftime("%I:%M:%S %p"))
else:
    inc_id, inc_type, inc_zone = 3821, "FIRE", "Floor 3, Room 307"
    inc_sev, inc_status        = "CRITICAL", "RESOLVED"
    inc_score                  = 9.2
    inc_photo                  = False
    inc_desc                   = "Fire emergency reported at Floor 3, Room 307. Smoke visible in north corridor."
    trigger_time               = now.strftime("%I:%M:%S %p")

sev_col_hex  = severity_color(inc_sev)
icon         = incident_icon(inc_type)
report_no    = f"RSQ-{now.strftime('%Y%m%d')}-{inc_id}"
report_date  = now.strftime("%B %d, %Y")
report_time  = now.strftime("%H:%M:%S")

# ── Chat messages for the report ──
chat_entries = []
if "chat_messages" in st.session_state:
    chat_entries = st.session_state.chat_messages[:8]
else:
    from datetime import timedelta as td
    def _ts(s): return (now - td(seconds=s)).strftime("%H:%M:%S")
    chat_entries = [
        {"sender": "Command Center", "text": "INCIDENT ACTIVATED — Fire Floor 3 Room 307.",     "ts": _ts(310)},
        {"sender": "Security Alpha", "text": "En route via Corridor B. ETA 45 seconds.",         "ts": _ts(295)},
        {"sender": "Floor Manager",  "text": "Initiating guest evacuation on Floor 3.",           "ts": _ts(280)},
        {"sender": "Fire Response",  "text": "Fire contained. Faulty electrical in Room 307.",    "ts": _ts(50)},
        {"sender": "Security Alpha", "text": "Floor 3 secured. 16/16 guests accounted for.",      "ts": _ts(30)},
        {"sender": "Command Center", "text": "Incident resolved. Return to base.",                 "ts": _ts(10)},
    ]

# ── Radio log for report ──
radio_entries = []
if "radio_log" in st.session_state:
    radio_entries = st.session_state.radio_log[:6]

# ── Timeline ──
def _ts_offset(s): return (now - timedelta(seconds=s)).strftime("%H:%M:%S")

timeline = [
    {"time": _ts_offset(310), "event": "SOS Alert Triggered",               "actor": "Guest",          "color": "#ff4b4b"},
    {"time": _ts_offset(300), "event": f"{inc_type} Emergency Classified",   "actor": "AI Engine",      "color": "#ff8c00"},
    {"time": _ts_offset(290), "event": "Emergency Contacts Notified",        "actor": "System",         "color": "#ffd700"},
    {"time": _ts_offset(280), "event": "Responder Team Auto-Assigned",       "actor": "Command Center", "color": "#00bfff"},
    {"time": _ts_offset(200), "event": "First Responder On Scene",           "actor": "Security Alpha", "color": "#00bfff"},
    {"time": _ts_offset(150), "event": "Guest Evacuation Completed",         "actor": "Floor Manager",  "color": "#00c853"},
    {"time": _ts_offset(50),  "event": "Incident Contained",                 "actor": "Fire Response",  "color": "#00c853"},
    {"time": _ts_offset(20),  "event": "All Clear Declared",                 "actor": "Command Center", "color": "#00c853"},
    {"time": _ts_offset(5),   "event": "Incident Marked RESOLVED",           "actor": "System",         "color": "#7a8ba8"},
]

response_time_sec = 310 - 20
resp_min = response_time_sec // 60
resp_sec = response_time_sec % 60

# ── Left: Report controls | Right: Preview ──
col_ctrl, col_report = st.columns([1, 3])

with col_ctrl:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:10px;'
                'font-family:\'JetBrains Mono\',monospace;">REPORT OPTIONS</div>',
                unsafe_allow_html=True)

    include_timeline = st.checkbox("Include Timeline",        value=True)
    include_contacts = st.checkbox("Include Contact Log",     value=True)
    include_chat     = st.checkbox("Include Chat Transcript", value=True)
    include_radio    = st.checkbox("Include Radio Log",       value=True)
    include_ai       = st.checkbox("Include AI Analysis",     value=True)

    generate_btn = st.button("⚡ Generate Report", use_container_width=True, type="primary")

    if "report_generated" not in st.session_state:
        st.session_state.report_generated = False

    if generate_btn:
        st.session_state.report_generated = True
        st.rerun()

    if st.session_state.report_generated:
        st.markdown("""
        <div style="background:rgba(0,200,83,0.08);border:1px solid rgba(0,200,83,0.3);
                    border-radius:6px;padding:10px;text-align:center;margin-top:8px;">
            <div style="font-size:11px;color:#00c853;font-weight:600;">✅ Report Ready</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin:16px 0 10px;'
                'font-family:\'JetBrains Mono\',monospace;">INCIDENT SUMMARY</div>',
                unsafe_allow_html=True)

    for label, val, color in [
        ("Report No.",    report_no,               "#e8edf5"),
        ("Type",          f"{icon} {inc_type}",    sev_col_hex),
        ("Severity",      f"{inc_sev} ({inc_score}/10)", sev_col_hex),
        ("Location",      inc_zone,                "#aab4c8"),
        ("Status",        inc_status,              "#00c853" if inc_status == "RESOLVED" else "#ff4b4b"),
        ("Response Time", f"{resp_min}m {resp_sec}s", "#00bfff"),
    ]:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:5px;
                    padding:8px 10px;margin-bottom:5px;">
            <div style="font-size:9px;color:#555;letter-spacing:1px;
                        font-family:'JetBrains Mono',monospace;">{label.upper()}</div>
            <div style="font-size:11px;color:{color};font-weight:600;margin-top:2px;">{val}</div>
        </div>
        """, unsafe_allow_html=True)

    # Download plain-text report
    plain_text = f"""RESQSYNC AI — INCIDENT REPORT
Report No: {report_no}
Date: {report_date}  Time: {report_time}
========================================

INCIDENT DETAILS
Type: {inc_type}
Location: {inc_zone}
Severity: {inc_sev} ({inc_score}/10)
Status: {inc_status}
Description: {inc_desc}

TIMELINE
""" + "\n".join([f"  {t['time']}  {t['event']}  [{t['actor']}]" for t in timeline]) + """

CONTACTS NOTIFIED
  Family / Guest Contact — SMS — Notified
  Hotel Manager — Push + Call — Alerted
  Security Control Room — Radio — Dispatched
  Emergency Services (112) — Auto-dial — Contacted

RESPONSE OUTCOME
  Total Response Time: """ + f"{resp_min}m {resp_sec}s" + """
  Casualties: None reported
  Property Damage: Contained to Room 307
  Guests Evacuated: 16 / 16 accounted for

Generated by ResQSync AI — """ + now.strftime("%Y-%m-%d %H:%M:%S")

    st.download_button(
        label="⬇️ Export as .txt",
        data=plain_text,
        file_name=f"{report_no}.txt",
        mime="text/plain",
        use_container_width=True,
    )

with col_report:
    if not st.session_state.report_generated:
        st.markdown("""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:10px;
                    padding:60px 40px;text-align:center;">
            <div style="font-size:48px;margin-bottom:16px;">📄</div>
            <div style="font-size:16px;font-weight:600;color:#e8edf5;">AI Report Generator</div>
            <div style="font-size:13px;color:#7a8ba8;margin-top:8px;line-height:1.7;">
                Select sections on the left and click<br>
                <strong style="color:#00bfff;">⚡ Generate Report</strong> to auto-draft a<br>
                structured incident report.
            </div>
            <div style="margin-top:20px;font-size:11px;color:#555;font-family:'JetBrains Mono',monospace;line-height:2;">
                INCLUDES: SOS Data • AI Analysis<br>
                Timeline • Contact Log • Chat Transcript<br>
                Radio Log • Response Metrics
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Build timeline rows
        tl_rows = ""
        for t in timeline:
            tl_rows += f"""
            <tr>
              <td style="padding:7px 14px;color:#555;font-family:'JetBrains Mono',monospace;font-size:10px;border-bottom:1px solid #1a1f2e;white-space:nowrap;">{t['time']}</td>
              <td style="padding:7px 14px;color:#e8edf5;font-size:11px;border-bottom:1px solid #1a1f2e;">{t['event']}</td>
              <td style="padding:7px 14px;font-size:10px;border-bottom:1px solid #1a1f2e;">
                <span style="color:{t['color']};font-family:'JetBrains Mono',monospace;">{t['actor']}</span>
              </td>
            </tr>"""

        # Chat transcript rows
        chat_rows = ""
        if include_chat:
            for c in chat_entries:
                chat_rows += f"""
                <tr>
                  <td style="padding:6px 12px;color:#555;font-family:'JetBrains Mono',monospace;font-size:10px;border-bottom:1px solid #1a1f2e;white-space:nowrap;">{c.get('ts','—')}</td>
                  <td style="padding:6px 12px;font-size:11px;border-bottom:1px solid #1a1f2e;">
                    <span style="color:#00bfff;font-weight:600;">{c['sender']}</span>
                  </td>
                  <td style="padding:6px 12px;color:#aab4c8;font-size:11px;border-bottom:1px solid #1a1f2e;">{c['text']}</td>
                </tr>"""

        # Radio log rows
        radio_rows = ""
        if include_radio and radio_entries:
            for r in radio_entries:
                radio_rows += f"""
                <tr>
                  <td style="padding:6px 12px;color:#555;font-family:'JetBrains Mono',monospace;font-size:10px;border-bottom:1px solid #1a1f2e;white-space:nowrap;">{r.get('ts','—')}</td>
                  <td style="padding:6px 12px;font-size:11px;border-bottom:1px solid #1a1f2e;">
                    <span style="color:#ff8c00;font-weight:600;">{r['sender']}</span>
                  </td>
                  <td style="padding:6px 12px;color:#555;font-size:10px;border-bottom:1px solid #1a1f2e;font-family:'JetBrains Mono',monospace;">{r.get('ch','—')}</td>
                  <td style="padding:6px 12px;color:#aab4c8;font-size:11px;border-bottom:1px solid #1a1f2e;">{r['msg']}</td>
                </tr>"""

        contact_rows = ""
        if include_contacts:
            for name, icon_c, method, status_c, color in [
                ("Family / Guest Contact", "👨‍👩‍👧", "SMS",          "Notified",   "#00c853"),
                ("Hotel Manager",          "🏨",     "Push + Call", "Alerted",    "#00c853"),
                ("Security Control Room",  "🛡️",    "Radio",       "Dispatched", "#00c853"),
                ("Emergency Services 112", "🚑",     "Auto-dial",   "Contacted",  "#00c853"),
            ]:
                contact_rows += f"""
                <tr>
                  <td style="padding:7px 14px;color:#e8edf5;font-size:11px;border-bottom:1px solid #1a1f2e;">{icon_c} {name}</td>
                  <td style="padding:7px 14px;color:#7a8ba8;font-size:11px;border-bottom:1px solid #1a1f2e;font-family:'JetBrains Mono',monospace;">{method}</td>
                  <td style="padding:7px 14px;font-size:11px;border-bottom:1px solid #1a1f2e;">
                    <span style="color:{color};font-weight:700;">✓ {status_c}</span>
                  </td>
                </tr>"""

        report_html = f"""
<!DOCTYPE html><html><head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
  *{{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#0d1117; padding:0; font-family:'Inter',sans-serif; overflow-y:auto; color:#e8edf5; }}
  ::-webkit-scrollbar {{ width:5px; }} ::-webkit-scrollbar-track {{ background:#0d1117; }}
  ::-webkit-scrollbar-thumb {{ background:#1e2a3a; border-radius:3px; }}
  .section {{ background:#151b28; border:1px solid #1e2a3a; border-radius:8px; margin-bottom:14px; overflow:hidden; }}
  .section-hdr {{ background:#111620; padding:10px 16px; font-size:10px; font-weight:600; color:#7a8ba8; letter-spacing:1.5px; text-transform:uppercase; font-family:'JetBrains Mono',monospace; border-bottom:1px solid #1e2a3a; }}
  table {{ width:100%; border-collapse:collapse; }}
  .badge {{ display:inline-block; padding:2px 8px; border-radius:10px; font-size:10px; font-weight:700; font-family:'JetBrains Mono',monospace; }}
</style>
</head><body>

<!-- Report Header -->
<div style="background:linear-gradient(135deg,#111620,#151b28);border:1px solid #1e2a3a;border-radius:10px;padding:20px 22px;margin-bottom:14px;">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px;">
    <div>
      <div style="font-size:11px;color:#7a8ba8;letter-spacing:2px;font-family:'JetBrains Mono',monospace;margin-bottom:6px;">RESQSYNC AI — OFFICIAL INCIDENT REPORT</div>
      <div style="font-size:22px;font-weight:800;color:#e8edf5;">{icon} {inc_type} EMERGENCY</div>
      <div style="font-size:12px;color:#7a8ba8;margin-top:4px;">{inc_zone}</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:10px;color:#555;font-family:'JetBrains Mono',monospace;">REPORT NO.</div>
      <div style="font-size:13px;font-weight:700;color:#00bfff;font-family:'JetBrains Mono',monospace;">{report_no}</div>
      <div style="font-size:10px;color:#555;margin-top:6px;font-family:'JetBrains Mono',monospace;">{report_date} · {report_time}</div>
    </div>
  </div>
  <div style="display:flex;gap:10px;margin-top:14px;flex-wrap:wrap;">
    <span class="badge" style="background:{sev_col_hex}22;border:1px solid {sev_col_hex}55;color:{sev_col_hex};">{inc_sev}</span>
    <span class="badge" style="background:rgba(0,200,83,0.12);border:1px solid rgba(0,200,83,0.35);color:#00c853;">{inc_status}</span>
    <span class="badge" style="background:rgba(0,191,255,0.1);border:1px solid rgba(0,191,255,0.3);color:#00bfff;">SEVERITY {inc_score}/10</span>
    <span class="badge" style="background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.3);color:#ffd700;">RESPONSE {resp_min}m {resp_sec}s</span>
    {'<span class="badge" style="background:rgba(0,200,83,0.12);border:1px solid rgba(0,200,83,0.35);color:#00c853;">📸 PHOTO EVIDENCE</span>' if inc_photo else ''}
  </div>
</div>

<!-- Incident Details -->
<div class="section">
  <div class="section-hdr">01 — INCIDENT DETAILS</div>
  <div style="padding:14px 18px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;">
      <div style="background:#111620;border-radius:6px;padding:10px;">
        <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:3px;">INCIDENT ID</div>
        <div style="font-size:13px;font-weight:700;color:#e8edf5;font-family:'JetBrains Mono',monospace;">#{inc_id}</div>
      </div>
      <div style="background:#111620;border-radius:6px;padding:10px;">
        <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:3px;">TRIGGER TIME</div>
        <div style="font-size:13px;font-weight:700;color:#e8edf5;font-family:'JetBrains Mono',monospace;">{trigger_time}</div>
      </div>
      <div style="background:#111620;border-radius:6px;padding:10px;">
        <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:3px;">TOTAL RESPONSE</div>
        <div style="font-size:13px;font-weight:700;color:#00bfff;font-family:'JetBrains Mono',monospace;">{resp_min}m {resp_sec}s</div>
      </div>
    </div>
    <div style="background:#111620;border-radius:6px;padding:12px;">
      <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:6px;">INCIDENT DESCRIPTION</div>
      <div style="font-size:12px;color:#aab4c8;line-height:1.6;">{inc_desc}</div>
    </div>
  </div>
</div>

{f'''<!-- AI Analysis -->
<div class="section">
  <div class="section-hdr">02 — AI SEVERITY ANALYSIS</div>
  <div style="padding:14px 18px;">
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;">
      <div style="background:#111620;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:6px;">SEVERITY SCORE</div>
        <div style="font-size:28px;font-weight:800;color:{sev_col_hex};">{inc_score}</div>
        <div style="font-size:10px;color:#555;">/10</div>
      </div>
      <div style="background:#111620;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:6px;">RISK LEVEL</div>
        <div style="font-size:16px;font-weight:700;color:{sev_col_hex};">{inc_sev}</div>
      </div>
      <div style="background:#111620;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:6px;">AI CONFIDENCE</div>
        <div style="font-size:16px;font-weight:700;color:#00bfff;">{random.randint(88,97)}%</div>
      </div>
      <div style="background:#111620;border-radius:6px;padding:12px;text-align:center;">
        <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:6px;">RECOMMENDATION</div>
        <div style="font-size:11px;font-weight:600;color:#ff8c00;">{"Evacuation" if inc_sev == "CRITICAL" else "Respond"}</div>
      </div>
    </div>
  </div>
</div>''' if include_ai else ''}

{f'''<!-- Timeline -->
<div class="section">
  <div class="section-hdr">03 — INCIDENT TIMELINE</div>
  <table>
    <thead><tr>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">TIME</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">EVENT</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">ACTOR</th>
    </tr></thead>
    <tbody>{tl_rows}</tbody>
  </table>
</div>''' if include_timeline else ''}

{f'''<!-- Contacts -->
<div class="section">
  <div class="section-hdr">04 — EMERGENCY CONTACTS NOTIFIED</div>
  <table>
    <thead><tr>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">CONTACT</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">METHOD</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">STATUS</th>
    </tr></thead>
    <tbody>{contact_rows}</tbody>
  </table>
</div>''' if include_contacts else ''}

{f'''<!-- Chat transcript -->
<div class="section">
  <div class="section-hdr">05 — CHAT TRANSCRIPT (EXCERPT)</div>
  <table>
    <thead><tr>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">TIME</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">SENDER</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">MESSAGE</th>
    </tr></thead>
    <tbody>{chat_rows}</tbody>
  </table>
</div>''' if include_chat and chat_rows else ''}

{f'''<!-- Radio log -->
<div class="section">
  <div class="section-hdr">06 — RADIO TRANSMISSION LOG (EXCERPT)</div>
  <table>
    <thead><tr>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">TIME</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">SENDER</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">CHANNEL</th>
      <th style="text-align:left;padding:8px 14px;color:#555;font-size:9px;letter-spacing:1.5px;background:#0d1117;font-family:'JetBrains Mono',monospace;">MESSAGE</th>
    </tr></thead>
    <tbody>{radio_rows}</tbody>
  </table>
</div>''' if include_radio and radio_rows else ''}

<!-- Outcome -->
<div class="section">
  <div class="section-hdr">07 — RESPONSE OUTCOME &amp; RECOMMENDATIONS</div>
  <div style="padding:16px 18px;">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;">
      <div style="background:#111620;border-radius:6px;padding:12px;">
        <div style="font-size:10px;color:#7a8ba8;margin-bottom:8px;font-family:'JetBrains Mono',monospace;letter-spacing:1px;">OUTCOME SUMMARY</div>
        <div style="font-size:11px;color:#e8edf5;line-height:2.0;">
          ✅ Incident contained within {resp_min}m {resp_sec}s<br>
          ✅ Zero casualties reported<br>
          ✅ All guests evacuated safely (16/16)<br>
          ✅ No structural damage beyond Room 307<br>
          ✅ Emergency contacts all notified
        </div>
      </div>
      <div style="background:#111620;border-radius:6px;padding:12px;">
        <div style="font-size:10px;color:#7a8ba8;margin-bottom:8px;font-family:'JetBrains Mono',monospace;letter-spacing:1px;">RECOMMENDATIONS</div>
        <div style="font-size:11px;color:#aab4c8;line-height:2.0;">
          → Inspect electrical wiring in Rooms 305–310<br>
          → Schedule fire drill for all staff within 7 days<br>
          → Review smoke detector placement on Floor 3<br>
          → Update emergency contact list for guests<br>
          → Debrief all responding units within 24 hours
        </div>
      </div>
    </div>
    <div style="background:#0a0e14;border:1px solid #1e2a3a;border-radius:6px;padding:12px;text-align:center;">
      <div style="font-size:10px;color:#555;font-family:'JetBrains Mono',monospace;">
        GENERATED BY ResQSync AI &nbsp;·&nbsp; {now.strftime("%Y-%m-%d %H:%M:%S")} &nbsp;·&nbsp; REPORT {report_no}
      </div>
    </div>
  </div>
</div>

</body></html>
"""
        components.html(report_html, height=900, scrolling=True)
