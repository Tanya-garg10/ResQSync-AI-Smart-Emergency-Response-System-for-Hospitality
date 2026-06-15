"""
Admin Dashboard – Active emergencies, coordination, response management
"""
import streamlit as st
import streamlit.components.v1 as components
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
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">📊 Admin Dashboard</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        INCIDENT MANAGEMENT • RESPONSE COORDINATION • SYSTEM CONTROL
    </div>
</div>
""", unsafe_allow_html=True)

if "incidents" not in st.session_state:
    st.session_state.incidents = get_incidents(50)

incidents = st.session_state.incidents

# ── Metric Cards ──
active     = len([i for i in incidents if i["status"] == "ACTIVE"])
responding = len([i for i in incidents if i["status"] == "RESPONDING"])
resolved   = len([i for i in incidents if i["status"] == "RESOLVED"])
critical   = len([i for i in incidents if i["severity"] == "CRITICAL"])

m1, m2, m3, m4 = st.columns(4)
for col, label, value, color in zip(
    [m1, m2, m3, m4],
    ["ACTIVE", "RESPONDING", "RESOLVED", "CRITICAL"],
    [active, responding, resolved, critical],
    ["#ff4b4b", "#ff8c00", "#00c853", "#ff4b4b"],
):
    with col:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-top:3px solid {color};
                    border-radius:8px;padding:20px;text-align:center;">
            <div style="font-size:32px;font-weight:700;color:{color};
                        font-family:'JetBrains Mono',monospace;">{value}</div>
            <div style="font-size:10px;color:#7a8ba8;text-transform:uppercase;
                        letter-spacing:1.5px;margin-top:4px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Filters ──
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
            'text-transform:uppercase;margin-bottom:10px;'
            'font-family:\'JetBrains Mono\',monospace;">INCIDENT MANAGEMENT</div>',
            unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    filter_type     = st.selectbox("Filter Type",     ["ALL", "FIRE", "MEDICAL", "SECURITY"])
with f2:
    filter_status   = st.selectbox("Filter Status",   ["ALL", "ACTIVE", "RESPONDING", "RESOLVED"])
with f3:
    filter_severity = st.selectbox("Filter Severity", ["ALL", "CRITICAL", "PRIORITY", "MODERATE", "LOW"])

filtered = incidents
if filter_type     != "ALL": filtered = [i for i in filtered if i["type"]     == filter_type]
if filter_status   != "ALL": filtered = [i for i in filtered if i["status"]   == filter_status]
if filter_severity != "ALL": filtered = [i for i in filtered if i["severity"] == filter_severity]

# ── Build table as self-contained HTML (avoids Streamlit markdown escaping) ──
rows_html = ""
for inc in filtered:
    sev_col  = severity_color(inc["severity"])
    stat_col = status_color(inc["status"])
    icon     = incident_icon(inc["type"])
    status_dot = "🔴" if inc["status"] == "ACTIVE" else "🟠" if inc["status"] == "RESPONDING" else "⚫"

    rows_html += f"""
    <tr class="row">
      <td style="padding:11px 14px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;
                 font-size:11px;font-weight:600;border-bottom:1px solid #1e2a3a;">{inc['id']}</td>
      <td style="padding:11px 14px;color:#e8edf5;font-size:12px;
                 border-bottom:1px solid #1e2a3a;">{icon} {inc['type']}</td>
      <td style="padding:11px 14px;color:#aab4c8;font-size:12px;
                 border-bottom:1px solid #1e2a3a;">{inc['zone']}</td>
      <td style="padding:11px 14px;border-bottom:1px solid #1e2a3a;">
        <span style="color:{sev_col};font-weight:700;font-size:11px;
                     font-family:'JetBrains Mono',monospace;">{inc['severity']}</span>
      </td>
      <td style="padding:11px 14px;border-bottom:1px solid #1e2a3a;">
        <span style="color:{stat_col};font-weight:700;font-size:11px;
                     font-family:'JetBrains Mono',monospace;">{status_dot} {inc['status']}</span>
      </td>
      <td style="padding:11px 14px;color:#555;font-size:11px;
                 border-bottom:1px solid #1e2a3a;
                 font-family:'JetBrains Mono',monospace;">{inc['timestamp']}</td>
    </tr>
    """

table_html = f"""
<!DOCTYPE html><html><head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#0d1117; overflow-y:auto; font-family:'Inter',sans-serif; }}
  ::-webkit-scrollbar {{ width:5px; height:5px; }}
  ::-webkit-scrollbar-track {{ background:#0d1117; }}
  ::-webkit-scrollbar-thumb {{ background:#1e2a3a; border-radius:3px; }}
  table {{ width:100%; border-collapse:collapse; font-size:12px; }}
  thead th {{
    text-align:left; padding:10px 14px;
    color:#7a8ba8; font-weight:500; font-size:10px;
    letter-spacing:1.5px; text-transform:uppercase;
    background:#111620; border-bottom:2px solid #1e2a3a;
    font-family:'JetBrains Mono',monospace;
  }}
  .row:hover td {{ background:rgba(0,191,255,0.04); }}
  {"" if filtered else ""}
</style>
</head><body>
<div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;overflow:hidden;">
  <table>
    <thead>
      <tr>
        <th>ID</th><th>TYPE</th><th>ZONE</th>
        <th>SEVERITY</th><th>STATUS</th><th>TIME</th>
      </tr>
    </thead>
    <tbody>
      {rows_html if rows_html else
       '<tr><td colspan="6" style="padding:30px;text-align:center;color:#555;">No incidents match the selected filters</td></tr>'}
    </tbody>
  </table>
</div>
</body></html>
"""

row_count = len(filtered)
table_height = max(120, min(60 + row_count * 44, 500))
components.html(table_html, height=table_height, scrolling=True)

# ── Charts row ──
st.markdown("<br>", unsafe_allow_html=True)
chart_c1, chart_c2 = st.columns(2)

with chart_c1:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:10px;'
                'font-family:\'JetBrains Mono\',monospace;">INCIDENTS BY TYPE</div>',
                unsafe_allow_html=True)
    try:
        import plotly.graph_objects as go
        fire_n     = sum(1 for i in incidents if i["type"] == "FIRE")
        medical_n  = sum(1 for i in incidents if i["type"] == "MEDICAL")
        security_n = sum(1 for i in incidents if i["type"] == "SECURITY")
        fig = go.Figure(go.Pie(
            labels=["🔥 Fire", "🏥 Medical", "🚨 Security"],
            values=[fire_n, medical_n, security_n],
            hole=0.55,
            marker=dict(colors=["#ff4b4b", "#00bfff", "#ff8c00"]),
        ))
        fig.update_layout(
            paper_bgcolor="#151b28", plot_bgcolor="#151b28",
            font=dict(color="#e8edf5", size=11),
            margin=dict(t=10, b=10, l=10, r=10), height=220,
            legend=dict(font=dict(color="#e8edf5")),
            showlegend=True,
        )
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        st.info("Install plotly for charts")

with chart_c2:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:10px;'
                'font-family:\'JetBrains Mono\',monospace;">INCIDENTS BY SEVERITY</div>',
                unsafe_allow_html=True)
    try:
        import plotly.graph_objects as go
        sev_counts = {s: sum(1 for i in incidents if i["severity"] == s)
                      for s in ["CRITICAL", "PRIORITY", "MODERATE", "LOW"]}
        fig2 = go.Figure(go.Bar(
            x=list(sev_counts.keys()),
            y=list(sev_counts.values()),
            marker_color=["#ff4b4b", "#ff8c00", "#ffd700", "#00c853"],
            text=list(sev_counts.values()),
            textposition="outside",
            textfont=dict(color="#e8edf5"),
        ))
        fig2.update_layout(
            paper_bgcolor="#151b28", plot_bgcolor="#151b28",
            font=dict(color="#e8edf5", size=11),
            margin=dict(t=20, b=10, l=10, r=10), height=220,
            xaxis=dict(gridcolor="#1e2a3a"),
            yaxis=dict(gridcolor="#1e2a3a"),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)
    except ImportError:
        pass

# ── Quick Actions ──
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;'
            'text-transform:uppercase;margin-bottom:10px;'
            'font-family:\'JetBrains Mono\',monospace;">QUICK ACTIONS</div>',
            unsafe_allow_html=True)

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
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.incidents = generate_demo_incidents(8)
        st.rerun()
with a4:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.incidents = []
        st.rerun()
