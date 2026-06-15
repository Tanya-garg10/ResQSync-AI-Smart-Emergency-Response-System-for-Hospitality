"""
AI Voice Analysis – Emotion detection, stress level, confidence score, Hinglish support
"""
import streamlit as st
from services.voice_service import process_voice_input, detect_emotion, detect_stress_level
from services.ai_classifier import full_analysis
from utils.helpers import incident_icon, severity_color

st.set_page_config(page_title="AI Voice Analysis | ResQSync AI", page_icon="🎙️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains Mono:wght@400;500&display=swap');
.stApp { background-color: #0a0e14 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #111620 !important; border-right: 1px solid #1e2a3a !important; }
@keyframes wave-pulse {
    0%,100% { transform: scaleY(0.6); opacity: 0.4; }
    50% { transform: scaleY(1.0); opacity: 1.0; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:8px 0 16px 0;border-bottom:1px solid #1e2a3a;margin-bottom:20px;">
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">🎙️ AI Voice Analysis</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        EMOTION DETECTION • STRESS ANALYSIS • HINGLISH • CONFIDENCE SCORING
    </div>
</div>
""", unsafe_allow_html=True)

col_input, col_result = st.columns([1, 1])

with col_input:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">VOICE INPUT SIMULATION</div>', unsafe_allow_html=True)

    lang = st.radio("Language", ["🇬🇧 English", "🇮🇳 Hindi", "🔀 Hinglish"], horizontal=True, label_visibility="collapsed")

    if "🇮🇳" in lang:
        placeholder = "e.g., Bachao! Aag lag gayi hai, madad chahiye..."
    elif "🔀" in lang:
        placeholder = "e.g., Help karo! Fire ho gayi hai floor 3 mein, please come fast..."
    else:
        placeholder = "e.g., Help! There's a fire in the kitchen, someone is hurt..."

    voice_text = st.text_area("Speak or type your emergency...", height=110,
                               placeholder=placeholder, label_visibility="collapsed",
                               key="voice_ta")

    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:16px 0 8px;font-family:\'JetBrains Mono\',monospace;">QUICK TEST PHRASES</div>', unsafe_allow_html=True)

    demo_col1, demo_col2 = st.columns(2)
    with demo_col1:
        if st.button("🔥 Fire in lobby", use_container_width=True):
            st.session_state["voice_input"] = "Help! There is a fire in the hotel lobby, smoke everywhere!"
        if st.button("🏥 Medical emergency", use_container_width=True):
            st.session_state["voice_input"] = "Someone is unconscious and bleeding in room 201, need ambulance now!"
    with demo_col2:
        if st.button("🚨 Security threat", use_container_width=True):
            st.session_state["voice_input"] = "There's an intruder with a weapon near the parking area, danger!"
        if st.button("🔀 Hinglish: Fire!", use_container_width=True):
            st.session_state["voice_input"] = "Help karo yaar! Aag lag gayi hai kitchen mein, bahut dhua aa raha hai, please jaldi aao!"

    if "voice_input" in st.session_state and not voice_text:
        voice_text = st.session_state["voice_input"]
        st.markdown(f'<div style="background:#151b28;border:1px solid #1e2a3a;border-radius:6px;padding:10px;font-size:12px;color:#7a8ba8;margin-top:4px;">📝 <em>{voice_text[:80]}...</em></div>', unsafe_allow_html=True)

    process_btn = st.button("🔍 Analyze Voice Input", use_container_width=True, type="primary")

    # Waveform visualization
    st.markdown("""
    <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;margin-top:14px;text-align:center;">
        <div style="font-size:10px;color:#7a8ba8;letter-spacing:1px;margin-bottom:10px;">AUDIO WAVEFORM</div>
        <div style="display:flex;align-items:center;justify-content:center;gap:3px;height:40px;">
            """ + "".join([
                f'<div style="width:3px;background:#00bfff;border-radius:2px;opacity:0.7;animation:wave-pulse {0.3 + (i%5)*0.1:.1f}s ease-in-out infinite;height:{10+abs(20-i)*1.5:.0f}px;"></div>'
                for i in range(40)
            ]) + """
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_result:
    st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;font-family:\'JetBrains Mono\',monospace;">AI ANALYSIS OUTPUT</div>', unsafe_allow_html=True)

    active_text = voice_text or st.session_state.get("voice_input", "")

    if process_btn and active_text:
        voice_result = process_voice_input(active_text)
        ai_result = full_analysis(active_text)
        emotion = detect_emotion(active_text)
        stress = detect_stress_level(active_text)
        sev_col = severity_color(ai_result["severity"])

        # Emergency status banner
        emergency_bg = "rgba(255,75,75,0.1)" if voice_result["is_emergency"] else "rgba(0,200,83,0.08)"
        emergency_border = "rgba(255,75,75,0.4)" if voice_result["is_emergency"] else "rgba(0,200,83,0.3)"
        emergency_text = "🚨 EMERGENCY DETECTED" if voice_result["is_emergency"] else "✅ NO EMERGENCY DETECTED"
        emergency_color = "#ff4b4b" if voice_result["is_emergency"] else "#00c853"

        st.markdown(f"""
        <div style="background:{emergency_bg};border:1px solid {emergency_border};border-radius:8px;padding:14px;margin-bottom:12px;text-align:center;">
            <div style="font-size:16px;font-weight:700;color:{emergency_color};">{emergency_text}</div>
        </div>
        """, unsafe_allow_html=True)

        # AI Classification card
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-left:3px solid {sev_col};border-radius:8px;padding:14px;margin-bottom:10px;">
            <div style="font-size:10px;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">DETECTED EMERGENCY</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                <div style="background:#0a0e14;border-radius:6px;padding:10px;">
                    <div style="font-size:10px;color:#7a8ba8;">TYPE</div>
                    <div style="font-size:18px;font-weight:700;color:#e8edf5;">{incident_icon(ai_result['type'])} {ai_result['type']}</div>
                </div>
                <div style="background:#0a0e14;border-radius:6px;padding:10px;">
                    <div style="font-size:10px;color:#7a8ba8;">CONFIDENCE</div>
                    <div style="font-size:18px;font-weight:700;color:#00bfff;">{int(ai_result['confidence']*100)}%</div>
                </div>
                <div style="background:#0a0e14;border-radius:6px;padding:10px;">
                    <div style="font-size:10px;color:#7a8ba8;">LANGUAGE</div>
                    <div style="font-size:14px;font-weight:600;color:#ffd700;">{voice_result['language_name']}</div>
                </div>
                <div style="background:#0a0e14;border-radius:6px;padding:10px;">
                    <div style="font-size:10px;color:#7a8ba8;">SEVERITY</div>
                    <div style="font-size:14px;font-weight:600;color:{sev_col};">{ai_result['severity']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Emotion + Stress card
        stress_color = "#ff4b4b" if stress["level"] == "HIGH" else "#ff8c00" if stress["level"] == "MEDIUM" else "#00c853"
        emotion_color = "#ff4b4b" if emotion["emotion"] in ["PANIC", "FEAR"] else "#ff8c00" if emotion["emotion"] == "DISTRESS" else "#00bfff"

        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;margin-bottom:10px;">
            <div style="font-size:10px;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">🧠 EMOTION & STRESS ANALYSIS</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;">
                <div style="background:#0a0e14;border-radius:6px;padding:12px;text-align:center;">
                    <div style="font-size:10px;color:#7a8ba8;margin-bottom:6px;">EMOTION</div>
                    <div style="font-size:22px;margin-bottom:4px;">{emotion['icon']}</div>
                    <div style="font-size:14px;font-weight:700;color:{emotion_color};">{emotion['emotion']}</div>
                </div>
                <div style="background:#0a0e14;border-radius:6px;padding:12px;text-align:center;">
                    <div style="font-size:10px;color:#7a8ba8;margin-bottom:6px;">STRESS LEVEL</div>
                    <div style="font-size:22px;margin-bottom:4px;">{'🔴' if stress['level']=='HIGH' else '🟠' if stress['level']=='MEDIUM' else '🟢'}</div>
                    <div style="font-size:14px;font-weight:700;color:{stress_color};">{stress['level']}</div>
                </div>
            </div>
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:6px;">STRESS INDICATORS</div>
            <div style="font-size:11px;color:#e8edf5;">{' '.join([f'<span style="background:rgba(255,75,75,0.15);padding:2px 8px;border-radius:4px;margin:2px;display:inline-block;">{ind}</span>' for ind in stress['indicators']]) or '<span style="color:#555;">None detected</span>'}</div>
        </div>
        """, unsafe_allow_html=True)

        # Keywords & Language
        st.markdown(f"""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:14px;">
            <div style="font-size:10px;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">KEYWORDS DETECTED ({voice_result['keyword_count']})</div>
            <div style="font-size:12px;color:#e8edf5;margin-bottom:10px;">
                {' '.join([f'<span style="background:rgba(255,75,75,0.2);padding:2px 8px;border-radius:4px;margin:2px;display:inline-block;font-size:11px;">{kw}</span>' for kw in voice_result['keywords_found']]) or '<span style="color:#555;">None detected</span>'}
            </div>
            <div style="font-size:10px;color:#7a8ba8;margin-bottom:4px;">INPUT LANGUAGE BREAKDOWN</div>
            <div style="background:#0a0e14;border-radius:6px;padding:8px;font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;">
                {voice_result['language_detail']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:10px;padding:50px 30px;text-align:center;">
            <div style="font-size:48px;margin-bottom:12px;">🎙️</div>
            <div style="font-size:14px;font-weight:600;color:#e8edf5;">AI Voice Analysis Ready</div>
            <div style="font-size:12px;color:#7a8ba8;margin-top:8px;line-height:1.8;">
                Type or click a demo phrase,<br>then hit <strong>Analyze Voice Input</strong>
            </div>
        </div>
        <div style="background:#151b28;border:1px solid #1e2a3a;border-radius:8px;padding:16px;margin-top:12px;">
            <div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">ANALYSIS CAPABILITIES</div>
            <div style="font-size:12px;color:#e8edf5;line-height:2.2;">
                🧠 Emotion detection (Panic / Fear / Distress)<br>
                📊 Stress level scoring (High / Medium / Low)<br>
                🔀 Hinglish mixed language support<br>
                🎯 Confidence scoring per analysis<br>
                🔑 Emergency keyword extraction
            </div>
        </div>
        """, unsafe_allow_html=True)
