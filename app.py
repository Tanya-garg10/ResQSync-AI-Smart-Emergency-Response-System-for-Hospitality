"""
ResQSync AI – Smart Emergency Response System
Main Entry Point
"""
import streamlit as st
from utils.auth import login, logout, require_auth

st.set_page_config(
    page_title="ResQSync AI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global Dark Theme CSS (Command Center Style) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root variables */
:root {
    --bg-primary: #0a0e14;
    --bg-secondary: #111620;
    --bg-card: #151b28;
    --bg-card-hover: #1a2233;
    --border-color: #1e2a3a;
    --text-primary: #e8edf5;
    --text-secondary: #7a8ba8;
    --accent-red: #ff4b4b;
    --accent-green: #00c853;
    --accent-orange: #ff8c00;
    --accent-blue: #00bfff;
    --accent-yellow: #ffd700;
}

/* Global overrides */
.stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-color) !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: var(--text-secondary) !important;
}

/* Card containers */
.command-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

/* Header bar */
.header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 20px;
}
.header-title {
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.5px;
}
.header-meta {
    font-size: 12px;
    color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
}

/* System status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.5px;
}
.status-nominal {
    background: rgba(0, 200, 83, 0.15);
    color: #00c853;
    border: 1px solid rgba(0, 200, 83, 0.3);
}
.status-alert {
    background: rgba(255, 75, 75, 0.15);
    color: #ff4b4b;
    border: 1px solid rgba(255, 75, 75, 0.3);
}

/* Health bars */
.health-bar-container {
    margin: 8px 0;
}
.health-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-secondary);
    margin-bottom: 4px;
    letter-spacing: 0.5px;
}
.health-bar-track {
    background: #1a2233;
    border-radius: 3px;
    height: 6px;
    overflow: hidden;
}
.health-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.5s ease;
}

/* Intel cards */
.intel-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-left: 3px solid var(--accent-orange);
    border-radius: 6px;
    padding: 12px 14px;
    margin-bottom: 8px;
}
.intel-card.critical {
    border-left-color: var(--accent-red);
}
.intel-card.priority {
    border-left-color: var(--accent-orange);
}
.intel-card.moderate {
    border-left-color: var(--accent-yellow);
}
.intel-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.intel-id {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
}
.intel-time {
    font-size: 10px;
    color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
}
.intel-meta {
    font-size: 11px;
    color: var(--text-secondary);
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Event log table */
.event-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}
.event-table th {
    text-align: left;
    padding: 10px 12px;
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border-color);
}
.event-table td {
    padding: 10px 12px;
    color: var(--text-primary);
    border-bottom: 1px solid rgba(30, 42, 58, 0.5);
}
.event-table tr:hover td {
    background: rgba(26, 34, 51, 0.5);
}
.active-status {
    color: var(--accent-green);
    font-weight: 600;
}
.responding-status {
    color: var(--accent-orange);
    font-weight: 600;
}

/* SOS Button */
.sos-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px 0;
}
.sos-btn {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, #ff4b4b 0%, #cc0000 70%, #990000 100%);
    border: 4px solid rgba(255, 75, 75, 0.4);
    color: white;
    font-size: 36px;
    font-weight: 800;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 40px rgba(255, 75, 75, 0.3), 0 0 80px rgba(255, 75, 75, 0.1);
    animation: sos-pulse 2s infinite;
    letter-spacing: 3px;
}
@keyframes sos-pulse {
    0%, 100% { box-shadow: 0 0 40px rgba(255, 75, 75, 0.3); transform: scale(1); }
    50% { box-shadow: 0 0 60px rgba(255, 75, 75, 0.5); transform: scale(1.03); }
}

/* Section titles */
.section-title {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-family: 'JetBrains Mono', monospace;
}

/* Sidebar nav items */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 6px;
    color: var(--text-secondary);
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 2px;
}
.nav-item:hover, .nav-item.active {
    background: rgba(0, 191, 255, 0.1);
    color: var(--text-primary);
}
.nav-item.active {
    background: rgba(0, 191, 255, 0.15);
    color: #00bfff;
}

/* Generate alert button */
.generate-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: rgba(0, 200, 83, 0.15);
    border: 1px solid rgba(0, 200, 83, 0.3);
    border-radius: 6px;
    color: #00c853;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    justify-content: center;
    margin-top: 16px;
}

/* Metric boxes */
.metric-box {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.metric-label {
    font-size: 11px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* Streamlit button overrides */
.stButton > button {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: var(--bg-card-hover) !important;
    border-color: var(--accent-blue) !important;
}

/* Streamlit input overrides */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; padding:10px 0 20px 0;">
        <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#ff4b4b,#cc0000);display:flex;align-items:center;justify-content:center;font-size:18px;">🚨</div>
        <div>
            <div style="font-size:16px;font-weight:700;color:#e8edf5;letter-spacing:1px;">ResQSync<span style="color:#00bfff;">AI</span></div>
            <div style="font-size:9px;color:#7a8ba8;letter-spacing:2px;font-family:'JetBrains Mono',monospace;">V5 GLOBAL MESH</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Auth section
    if not st.session_state.get("authenticated"):
        st.markdown("---")
        st.markdown('<p style="font-size:11px;color:#7a8ba8;letter-spacing:1px;">LOGIN</p>', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="admin / staff / guest", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
        if st.button("🔐 Authenticate", use_container_width=True):
            if login(username, password):
                st.rerun()
            else:
                st.error("Access Denied")
        st.markdown('<p style="font-size:10px;color:#555;">Demo: admin/admin123, staff/staff123, guest/guest123</p>', unsafe_allow_html=True)
    else:
        role = st.session_state.get("role", "guest")
        name = st.session_state.get("display_name", "User")
        st.markdown(f"""
        <div style="padding:8px 12px;background:rgba(0,191,255,0.1);border-radius:6px;border:1px solid rgba(0,191,255,0.2);margin-bottom:16px;">
            <div style="font-size:12px;color:#00bfff;font-weight:600;">{name}</div>
            <div style="font-size:10px;color:#7a8ba8;text-transform:uppercase;letter-spacing:1px;">{role}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size:10px;color:#555;padding:8px 0;">
        <div>📡 Uplink: <span style="color:#00c853;">ESTABLISHED</span></div>
        <div>🛡️ Encryption: <span style="color:#00c853;">AES-256</span></div>
        <div>🌐 Nodes: <span style="color:#00bfff;">47 Active</span></div>
    </div>
    """, unsafe_allow_html=True)


# ── Main Content (Landing / Login Prompt) ──
if not st.session_state.get("authenticated"):
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
        <div style="font-size:48px;margin-bottom:16px;">🚨</div>
        <div style="font-size:28px;font-weight:700;color:#e8edf5;letter-spacing:1px;">
            ResQSync<span style="color:#00bfff;">AI</span>
        </div>
        <div style="font-size:13px;color:#7a8ba8;margin-top:8px;letter-spacing:2px;font-family:'JetBrains Mono',monospace;">
            SMART EMERGENCY RESPONSE SYSTEM
        </div>
        <div style="margin-top:30px;font-size:14px;color:#7a8ba8;">
            Login from the sidebar to access the Command Center
        </div>
        <div style="margin-top:40px;display:flex;justify-content:center;gap:30px;">
            <div style="text-align:center;">
                <div style="font-size:24px;">🔥</div>
                <div style="font-size:10px;color:#7a8ba8;margin-top:4px;">FIRE</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;">🏥</div>
                <div style="font-size:10px;color:#7a8ba8;margin-top:4px;">MEDICAL</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;">🚨</div>
                <div style="font-size:10px;color:#7a8ba8;margin-top:4px;">SECURITY</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;padding:40px 20px;">
        <div style="font-size:18px;color:#e8edf5;font-weight:600;">Welcome to Command Center</div>
        <div style="font-size:13px;color:#7a8ba8;margin-top:8px;">
            Use the sidebar navigation pages to access system modules
        </div>
        <div style="margin-top:20px;font-size:12px;color:#555;">
            ← Select a page from the sidebar
        </div>
    </div>
    """, unsafe_allow_html=True)
