"""
Incident Analytics – Response time trends, incident history, charts
"""
import streamlit as st
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Analytics | ResQSync AI", page_icon="📈", layout="wide")

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
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">Incident Analytics</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        RESPONSE METRICS • TREND ANALYSIS • INCIDENT HISTORY
    </div>
</div>
""", unsafe_allow_html=True)

# ── Generate analytics data ──
if "analytics_data" not in st.session_state:
    days = 30
    data = {
        "dates": [(datetime.now() - timedelta(days=i)).strftime("%b %d") for i in range(days-1, -1, -1)],
        "fire_count": [random.randint(0, 3) for _ in range(days)],
        "medical_count": [random.randint(0, 5) for _ in range(days)],
        "security_count": [random.randint(0, 2) for _ in range(days)],
        "response_times": [random.uniform(30, 180) for _ in range(days)],
    }
    st.session_state.analytics_data = data

data = st.session_state.analytics_data

# ── Summary Metrics ──
total_incidents = sum(data["fire_count"]) + sum(data["medical_count"]) + sum(data["security_count"])
avg_response = sum(data["response_times"]) / len(data["response_times"])
fastest = min(data["response_times"])
resolution_rate = random.uniform(92, 99)

m1, m2, m3, m4 = st.columns(4)
summary = [
    ("TOTAL INCIDENTS", str(total_incidents), "#00bfff"),
    ("AVG RESPONSE", f"{avg_response:.0f}s", "#ff8c00"),
    ("FASTEST", f"{fastest:.0f}s", "#00c853"),
    ("RESOLUTION RATE", f"{resolution_rate:.1f}%", "#00c853"),
]

for col, (label, value, color) in zip([m1, m2, m3, m4], summary):
    with col:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-top:3px solid {color};border-radius:8px;padding:20px;text-align:center;">
            <div style="font-size:28px;font-weight:700;color:{color};font-family:'JetBrains Mono',monospace;">{value}</div>
            <div style="font-size:10px;color:#7a8ba8;text-transform:uppercase;letter-spacing:1.5px;margin-top:4px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ──
try:
    import plotly.graph_objects as go
    import pandas as pd

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">INCIDENTS BY TYPE (30 DAYS)</div>', unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Fire", x=data["dates"], y=data["fire_count"], marker_color="#ff4b4b"))
        fig.add_trace(go.Bar(name="Medical", x=data["dates"], y=data["medical_count"], marker_color="#00bfff"))
        fig.add_trace(go.Bar(name="Security", x=data["dates"], y=data["security_count"], marker_color="#ff8c00"))
        fig.update_layout(
            barmode="stack",
            plot_bgcolor="#0a0e14", paper_bgcolor="#151b28",
            font=dict(color="#7a8ba8", size=10),
            margin=dict(l=40, r=20, t=20, b=40),
            height=300,
            legend=dict(orientation="h", y=1.1),
            xaxis=dict(gridcolor="#1e2a3a", showgrid=False),
            yaxis=dict(gridcolor="#1e2a3a"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">RESPONSE TIME TREND</div>', unsafe_allow_html=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=data["dates"], y=data["response_times"],
            mode="lines+markers",
            line=dict(color="#00bfff", width=2),
            marker=dict(size=4, color="#00bfff"),
            fill="tozeroy",
            fillcolor="rgba(0,191,255,0.1)",
        ))
        fig2.update_layout(
            plot_bgcolor="#0a0e14", paper_bgcolor="#151b28",
            font=dict(color="#7a8ba8", size=10),
            margin=dict(l=40, r=20, t=20, b=40),
            height=300,
            xaxis=dict(gridcolor="#1e2a3a", showgrid=False),
            yaxis=dict(gridcolor="#1e2a3a", title="Seconds"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Pie chart + severity breakdown
    pie_col, sev_col = st.columns(2)

    with pie_col:
        st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">INCIDENT DISTRIBUTION</div>', unsafe_allow_html=True)

        fig3 = go.Figure(data=[go.Pie(
            labels=["Fire", "Medical", "Security"],
            values=[sum(data["fire_count"]), sum(data["medical_count"]), sum(data["security_count"])],
            marker=dict(colors=["#ff4b4b", "#00bfff", "#ff8c00"]),
            hole=0.5,
            textfont=dict(color="#e8edf5"),
        )])
        fig3.update_layout(
            plot_bgcolor="#0a0e14", paper_bgcolor="#151b28",
            font=dict(color="#7a8ba8", size=10),
            margin=dict(l=20, r=20, t=20, b=20),
            height=280,
            legend=dict(font=dict(color="#7a8ba8")),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with sev_col:
        st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;font-family:\'JetBrains Mono\',monospace;">SEVERITY BREAKDOWN</div>', unsafe_allow_html=True)

        sev_data = {"CRITICAL": random.randint(5, 15), "PRIORITY": random.randint(10, 25),
                     "MODERATE": random.randint(15, 30), "LOW": random.randint(8, 20)}
        sev_colors = {"CRITICAL": "#ff4b4b", "PRIORITY": "#ff8c00", "MODERATE": "#ffd700", "LOW": "#00c853"}

        for sev, count in sev_data.items():
            pct = int(count / sum(sev_data.values()) * 100)
            color = sev_colors[sev]
            st.markdown(f"""
            <div style="margin:12px 0;">
                <div style="display:flex;justify-content:space-between;font-size:11px;font-family:'JetBrains Mono',monospace;color:#7a8ba8;margin-bottom:4px;">
                    <span>{sev}</span>
                    <span style="color:{color};">{count} ({pct}%)</span>
                </div>
                <div style="background:#1a2233;border-radius:3px;height:8px;overflow:hidden;">
                    <div style="height:100%;width:{pct}%;background:{color};border-radius:3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

except ImportError:
    st.warning("Install plotly for charts: `pip install plotly`")
    st.markdown("""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:40px;text-align:center;">
        <div style="font-size:40px;margin-bottom:12px;">📊</div>
        <div style="color:#7a8ba8;">Charts require plotly. Run: pip install plotly</div>
    </div>
    """, unsafe_allow_html=True)
