"""
Predictive Risk Alert – AI-powered risk prediction with demo sensor data
"""
import streamlit as st
import random
import time
from datetime import datetime, timedelta
from utils.helpers import severity_color

st.set_page_config(page_title="Predictive Risk | ResQSync AI", page_icon="⚠️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
@keyframes alert-pulse {
    0%,100% { box-shadow: 0 0 10px rgba(255,215,0,0.2); }
    50% { box-shadow: 0 0 25px rgba(255,215,0,0.5); }
}
@keyframes risk-glow {
    0%,100% { opacity: 0.7; }
    50% { opacity: 1.0; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">⚠️ Predictive Risk Alert</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        AI RISK DETECTION • SENSOR ANALYTICS • PREVENTIVE ALERTS
    </div>
</div>
""", unsafe_allow_html=True)

# ── Live Risk Score ──
if "risk_seed" not in st.session_state:
    st.session_state.risk_seed = random.randint(0, 1000)

r = random.Random(st.session_state.risk_seed)

overall_risk = r.uniform(62, 78)
risk_color = "#ff4b4b" if overall_risk > 75 else "#ff8c00" if overall_risk > 60 else "#ffd700"
risk_label = "HIGH" if overall_risk > 75 else "ELEVATED" if overall_risk > 60 else "MODERATE"

st.markdown(f"""
<div style="background:rgba(255,140,0,0.06);border:1px solid rgba(255,140,0,0.3);border-radius:12px;padding:20px;margin-bottom:20px;animation:alert-pulse 3s infinite;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
        <div>
            <div style="font-size:13px;font-weight:600;color:#ff8c00;letter-spacing:1.5px;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">⚠️ OVERALL RISK LEVEL</div>
            <div style="font-size:48px;font-weight:800;color:{risk_color};line-height:1.1;">{overall_risk:.1f}<span style="font-size:24px;">/100</span></div>
            <div style="font-size:16px;font-weight:700;color:{risk_color};margin-top:4px;">{risk_label} RISK</div>
        </div>
        <div style="flex:1;min-width:200px;">
            <div style="background:#111620;border-radius:8px;padding:14px;">
                <div style="font-size:10px;color:#7a8ba8;margin-bottom:8px;letter-spacing:1px;">AI RECOMMENDATION</div>
                <div style="font-size:13px;color:#e8edf5;line-height:1.6;">
                    {'⚡ <strong>Immediate Inspection Required</strong><br>Elevated fire risk detected in Zone A.<br>Dispatch safety team immediately.' if overall_risk > 75 else '🔍 <strong>Preventive Action Advised</strong><br>Elevated crowd density in common areas.<br>Recommend increased patrol rounds.'}
                </div>
            </div>
        </div>
        <div>
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:4px;">LAST SCAN</div>
            <div style="font-size:13px;color:#00bfff;font-family:'JetBrains Mono',monospace;">{datetime.now().strftime('%H:%M:%S')}</div>
            <div style="font-size:10px;color:#555;margin-top:4px;">Auto-refresh: 30s</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Active Risk Alerts ──
risk_alerts = [
    {
        "zone": "Zone A — Kitchen / Floor 2",
        "type": "🔥 Fire Hazard",
        "detail": "High crowd density detected near kitchen vents. Potential smoke buildup.",
        "risk": r.uniform(70, 85),
        "action": "Inspect Zone A immediately",
        "color": "#ff4b4b",
        "sensor": "Smoke Density: 68 ppm (Threshold: 50)",
    },
    {
        "zone": "Lobby — Ground Floor",
        "type": "👥 Crowd Density",
        "detail": "Above-normal crowd concentration near main entrance. Stampede risk elevated.",
        "risk": r.uniform(60, 72),
        "action": "Deploy crowd management staff",
        "color": "#ff8c00",
        "sensor": "Crowd Density: 87 persons/100m² (Max: 70)",
    },
    {
        "zone": "Parking Level B2",
        "type": "🚗 Carbon Monoxide",
        "detail": "CO levels slightly elevated. Ventilation system may be underperforming.",
        "risk": r.uniform(45, 58),
        "action": "Check ventilation system",
        "color": "#ffd700",
        "sensor": "CO Level: 42 ppm (Threshold: 35)",
    },
    {
        "zone": "Floor 3 — Corridor",
        "type": "🌡️ Temperature Anomaly",
        "detail": "Room temperature sensors show 4°C above average in north corridor.",
        "risk": r.uniform(35, 48),
        "action": "HVAC inspection advised",
        "color": "#ffd700",
        "sensor": "Temp: 29°C (Normal: 23-25°C)",
    },
]

st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:14px;font-family:\'JetBrains Mono\',monospace;">🎯 ACTIVE RISK PREDICTIONS</div>', unsafe_allow_html=True)

alert_cols = st.columns(2)
for i, alert in enumerate(risk_alerts):
    with alert_cols[i % 2]:
        risk_pct = int(alert["risk"])
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid {alert['color']}44;border-left:3px solid {alert['color']};border-radius:8px;padding:14px;margin-bottom:12px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                <div>
                    <div style="font-size:13px;font-weight:700;color:{alert['color']};">{alert['type']}</div>
                    <div style="font-size:11px;color:#7a8ba8;margin-top:2px;">{alert['zone']}</div>
                </div>
                <div style="background:{alert['color']}22;border:1px solid {alert['color']}55;border-radius:20px;padding:4px 12px;">
                    <span style="font-size:14px;font-weight:700;color:{alert['color']};">{risk_pct}%</span>
                </div>
            </div>
            <div style="font-size:12px;color:#aab4c8;margin-bottom:10px;line-height:1.5;">{alert['detail']}</div>
            <div style="background:#0a0e14;border-radius:6px;padding:8px;margin-bottom:10px;">
                <div style="font-size:9px;color:#555;font-family:'JetBrains Mono',monospace;margin-bottom:2px;">SENSOR READING</div>
                <div style="font-size:11px;color:#ffd700;font-family:'JetBrains Mono',monospace;">{alert['sensor']}</div>
            </div>
            <div style="font-size:11px;color:{alert['color']};font-weight:600;">→ {alert['action']}</div>
            <div style="margin-top:8px;background:#111620;border-radius:4px;height:4px;">
                <div style="width:{risk_pct}%;height:100%;background:{alert['color']};border-radius:4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Sensor Dashboard ──
st.markdown("---")
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:14px;font-family:\'JetBrains Mono\',monospace;">📡 LIVE SENSOR READINGS</div>', unsafe_allow_html=True)

sensors = [
    {"name": "Smoke Detectors", "value": f"{r.randint(45, 70)} ppm", "status": "ELEVATED", "color": "#ff8c00", "icon": "💨"},
    {"name": "Temperature Sensors", "value": f"{r.randint(24, 30)}°C avg", "status": "NORMAL", "color": "#00c853", "icon": "🌡️"},
    {"name": "CO Sensors", "value": f"{r.randint(35, 50)} ppm", "status": "WARNING", "color": "#ffd700", "icon": "🏭"},
    {"name": "Motion Sensors", "value": f"{r.randint(120, 200)} events/hr", "status": "HIGH", "color": "#ff8c00", "icon": "🚶"},
    {"name": "Crowd Density", "value": f"{r.randint(75, 95)}%", "status": "ELEVATED", "color": "#ff8c00", "icon": "👥"},
    {"name": "Door Sensors", "value": f"{r.randint(2, 5)} open", "status": "NORMAL", "color": "#00c853", "icon": "🚪"},
]

sensor_cols = st.columns(3)
for i, sensor in enumerate(sensors):
    with sensor_cols[i % 3]:
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;margin-bottom:10px;text-align:center;">
            <div style="font-size:24px;margin-bottom:6px;">{sensor['icon']}</div>
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:4px;">{sensor['name']}</div>
            <div style="font-size:18px;font-weight:700;color:#e8edf5;">{sensor['value']}</div>
            <div style="font-size:10px;font-weight:600;color:{sensor['color']};margin-top:4px;">{sensor['status']}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Risk History Chart ──
st.markdown("---")
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">📊 RISK TREND (LAST 24 HOURS)</div>', unsafe_allow_html=True)

try:
    import plotly.graph_objects as go
    import pandas as pd

    hours = [(datetime.now() - timedelta(hours=i)).strftime("%H:%M") for i in range(24, 0, -1)]
    risk_values = [r.uniform(30, 80) for _ in range(24)]
    risk_values[-3] = 71.0
    risk_values[-2] = 74.5
    risk_values[-1] = overall_risk

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours, y=risk_values,
        mode="lines+markers",
        line=dict(color="#ff8c00", width=2),
        marker=dict(size=4, color="#ffd700"),
        fill="tozeroy",
        fillcolor="rgba(255,140,0,0.08)",
        name="Risk Score",
    ))
    fig.add_hline(y=75, line_dash="dash", line_color="#ff4b4b", annotation_text="HIGH RISK THRESHOLD", annotation_font_color="#ff4b4b")
    fig.update_layout(
        paper_bgcolor="#151b28", plot_bgcolor="#151b28",
        font=dict(color="#e8edf5", size=10),
        margin=dict(t=10, b=30, l=40, r=10),
        height=200,
        yaxis=dict(range=[0, 100], gridcolor="#1e2a3a", title="Risk Score"),
        xaxis=dict(gridcolor="#1e2a3a"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
except ImportError:
    st.markdown('<div style="color:#7a8ba8;font-size:12px;">Install plotly for risk trend chart</div>', unsafe_allow_html=True)

# Refresh button
if st.button("🔄 Refresh Risk Analysis", use_container_width=False):
    st.session_state.risk_seed = random.randint(0, 9999)
    st.rerun()
