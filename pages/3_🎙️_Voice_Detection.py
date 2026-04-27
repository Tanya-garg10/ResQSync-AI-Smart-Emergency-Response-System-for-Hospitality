"""
AI Voice Detection – Speech-to-text emergency keyword detection
"""
import streamlit as st
from services.voice_service import process_voice_input
from services.ai_classifier import full_analysis
from utils.helpers import incident_icon, severity_color

st.set_page_config(page_title="Voice Detection | ResQSync AI", page_icon="🎙️", layout="wide")

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
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">AI Voice Detection</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        SPEECH-TO-TEXT • KEYWORD DETECTION • MULTI-LANGUAGE
    </div>
</div>
""", unsafe_allow_html=True)

col_input, col_result = st.columns([1, 1])

with col_input:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">VOICE INPUT SIMULATION</div>', unsafe_allow_html=True)

    # Language selector
    lang = st.radio("Language", ["🇬🇧 English", "🇮🇳 Hindi"], horizontal=True, label_visibility="collapsed")

    # Text input (simulating voice)
    if "🇮🇳" in lang:
        placeholder = "e.g., Bachao! Aag lag gayi hai, madad chahiye..."
    else:
        placeholder = "e.g., Help! There's a fire in the kitchen, someone is hurt..."

    voice_text = st.text_area("Speak or type your emergency...", height=120,
                               placeholder=placeholder, label_visibility="collapsed")

    # Demo phrases
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:16px 0 8px 0;font-family:\'JetBrains Mono\',monospace;">QUICK TEST PHRASES</div>', unsafe_allow_html=True)

    demo_col1, demo_col2 = st.columns(2)
    with demo_col1:
        if st.button("🔥 Fire in lobby", use_container_width=True):
            voice_text = "Help! There is a fire in the hotel lobby, smoke everywhere!"
            st.session_state["voice_input"] = voice_text
        if st.button("🏥 Medical emergency", use_container_width=True):
            voice_text = "Someone is unconscious and bleeding in room 201, need ambulance!"
            st.session_state["voice_input"] = voice_text
    with demo_col2:
        if st.button("🚨 Security threat", use_container_width=True):
            voice_text = "There's an intruder with a weapon near the parking area!"
            st.session_state["voice_input"] = voice_text
        if st.button("🇮🇳 Hindi: Aag!", use_container_width=True):
            voice_text = "Bachao! Aag lag gayi hai, bahut dhua aa raha hai, madad chahiye!"
            st.session_state["voice_input"] = voice_text

    # Use session state if button was clicked
    if "voice_input" in st.session_state and not voice_text:
        voice_text = st.session_state["voice_input"]

    process_btn = st.button("🔍 Process Voice Input", use_container_width=True, type="primary")

with col_result:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">ANALYSIS OUTPUT</div>', unsafe_allow_html=True)

    if process_btn and voice_text:
        # Voice processing
        voice_result = process_voice_input(voice_text)
        ai_result = full_analysis(voice_text)
        sev_col = severity_color(ai_result["severity"])

        # Voice detection card
        emergency_bg = "rgba(255,75,75,0.1)" if voice_result["is_emergency"] else "rgba(0,200,83,0.1)"
        emergency_border = "rgba(255,75,75,0.3)" if voice_result["is_emergency"] else "rgba(0,200,83,0.3)"
        emergency_text = "🚨 EMERGENCY DETECTED" if voice_result["is_emergency"] else "✅ NO EMERGENCY DETECTED"
        emergency_color = "#ff4b4b" if voice_result["is_emergency"] else "#00c853"

        st.markdown(f"""
        <div style="background:{emergency_bg};border:1px solid {emergency_border};border-radius:8px;padding:16px;margin-bottom:12px;text-align:center;">
            <div style="font-size:16px;font-weight:700;color:{emergency_color};">{emergency_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # Details
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:16px;margin-bottom:12px;">
            <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">VOICE ANALYSIS</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div>
                    <div style="font-size:10px;color:#7a8ba8;">LANGUAGE</div>
                    <div style="font-size:14px;font-weight:600;color:#00bfff;">{voice_result['language_name']}</div>
                </div>
                <div>
                    <div style="font-size:10px;color:#7a8ba8;">KEYWORDS FOUND</div>
                    <div style="font-size:14px;font-weight:600;color:#ff8c00;">{voice_result['keyword_count']}</div>
                </div>
            </div>
            <div style="margin-top:10px;">
                <div style="font-size:10px;color:#7a8ba8;">DETECTED KEYWORDS</div>
                <div style="font-size:12px;color:#e8edf5;margin-top:4px;">
                    {' '.join([f'<span style="background:rgba(255,75,75,0.2);padding:2px 8px;border-radius:4px;margin:2px;display:inline-block;font-size:11px;">{kw}</span>' for kw in voice_result['keywords_found']]) or '<span style="color:#555;">None</span>'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # AI Classification
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-left:3px solid {sev_col};border-radius:8px;padding:16px;">
            <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">AI CLASSIFICATION</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;">
                <div>
                    <div style="font-size:10px;color:#7a8ba8;">TYPE</div>
                    <div style="font-size:18px;font-weight:700;color:#e8edf5;">{incident_icon(ai_result['type'])} {ai_result['type']}</div>
                </div>
                <div>
                    <div style="font-size:10px;color:#7a8ba8;">SEVERITY</div>
                    <div style="font-size:18px;font-weight:700;color:{sev_col};">{ai_result['severity']}</div>
                </div>
                <div>
                    <div style="font-size:10px;color:#7a8ba8;">CONFIDENCE</div>
                    <div style="font-size:18px;font-weight:700;color:#00bfff;">{int(ai_result['confidence']*100)}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:40px;text-align:center;">
            <div style="font-size:40px;margin-bottom:12px;">🎙️</div>
            <div style="font-size:14px;color:#7a8ba8;">Enter text or click a demo phrase, then process</div>
            <div style="font-size:11px;color:#555;margin-top:8px;">Supports English & Hindi keywords</div>
        </div>
        """, unsafe_allow_html=True)
