"""
AI Help Assistant – Emergency guidance chatbot
"""
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Assistant | ResQSync AI", page_icon="🤖", layout="wide")

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
    <span style="font-size:22px;font-weight:700;color:#e8edf5;">AI Help Assistant</span>
    <div style="font-size:11px;color:#7a8ba8;font-family:'JetBrains Mono',monospace;margin-top:4px;">
        EMERGENCY GUIDANCE • FIRST AID • SAFETY PROTOCOLS
    </div>
</div>
""", unsafe_allow_html=True)

# ── Knowledge Base (offline, no API needed) ──
KNOWLEDGE = {
    "fire": """🔥 **FIRE EMERGENCY GUIDANCE**

1. **Alert** – Pull the nearest fire alarm and call emergency services
2. **Evacuate** – Leave immediately using stairs, NOT elevators
3. **Stay Low** – Crawl below smoke level
4. **Close Doors** – Shut doors behind you to slow fire spread
5. **Stop, Drop, Roll** – If clothes catch fire
6. **Assembly Point** – Go to designated meeting area
7. **Do NOT re-enter** – Wait for fire department clearance

🧯 **Fire Extinguisher (PASS Method):**
- **P**ull the pin
- **A**im at base of fire
- **S**queeze the handle
- **S**weep side to side""",

    "medical": """🏥 **MEDICAL EMERGENCY GUIDANCE**

1. **Check Scene Safety** – Ensure area is safe for you
2. **Call for Help** – Alert medical team / call ambulance
3. **Check Responsiveness** – Tap shoulder, ask "Are you okay?"
4. **Airway** – Tilt head back, lift chin
5. **Breathing** – Look, listen, feel for 10 seconds
6. **CPR** – If not breathing: 30 chest compressions, 2 breaths
7. **AED** – Use if available, follow voice prompts
8. **Bleeding** – Apply direct pressure with clean cloth
9. **Shock** – Lay person flat, elevate legs, keep warm
10. **Do NOT move** – Unless in immediate danger""",

    "security": """🚨 **SECURITY THREAT GUIDANCE**

**RUN – HIDE – FIGHT Protocol:**

🏃 **RUN (First Choice)**
- Have an escape route in mind
- Leave belongings behind
- Help others if possible
- Call security/police when safe

🔒 **HIDE (If Can't Run)**
- Find a room with a lockable door
- Barricade the door
- Silence your phone
- Stay away from windows
- Turn off lights

⚔️ **FIGHT (Last Resort)**
- Act with aggression
- Use improvised weapons
- Commit to your actions

📞 When safe, call: Security Desk → Local Police → Emergency Services""",

    "earthquake": """🌍 **EARTHQUAKE GUIDANCE**

1. **DROP** – Get down on hands and knees
2. **COVER** – Get under sturdy furniture
3. **HOLD ON** – Stay until shaking stops
4. **After Shaking** – Check for injuries
5. **Evacuate** – If building is damaged
6. **Avoid** – Elevators, damaged areas, fallen power lines
7. **Aftershocks** – Be prepared for additional shaking""",

    "default": """⚠️ **GENERAL EMERGENCY GUIDANCE**

1. Stay calm and assess the situation
2. Call for help – alert staff or dial emergency number
3. Follow evacuation signs if needed
4. Help others if safe to do so
5. Go to the nearest assembly point
6. Wait for official all-clear

📞 **Emergency Contacts:**
- Hotel Security: Ext. 100
- Front Desk: Ext. 0
- Local Emergency: 112 / 911"""
}


def get_response(query: str) -> str:
    """Get AI response based on query keywords."""
    q = query.lower()
    if any(w in q for w in ["fire", "smoke", "burning", "aag"]):
        return KNOWLEDGE["fire"]
    elif any(w in q for w in ["medical", "hurt", "bleeding", "unconscious", "heart", "cpr", "first aid"]):
        return KNOWLEDGE["medical"]
    elif any(w in q for w in ["security", "threat", "intruder", "weapon", "attack", "theft"]):
        return KNOWLEDGE["security"]
    elif any(w in q for w in ["earthquake", "quake", "shaking"]):
        return KNOWLEDGE["earthquake"]
    else:
        return KNOWLEDGE["default"]


# ── Chat Interface ──
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "🤖 I'm your emergency guidance assistant. Ask me about fire safety, medical emergencies, security threats, or any emergency protocol.", "time": datetime.now().strftime("%I:%M %p")}
    ]

# Display chat
for msg in st.session_state.chat_history:
    is_user = msg["role"] == "user"
    align = "flex-end" if is_user else "flex-start"
    bg = "rgba(0,191,255,0.1)" if is_user else "#151b28"
    border = "rgba(0,191,255,0.3)" if is_user else "#1e2a3a"

    st.markdown(f"""
    <div style="display:flex;justify-content:{align};margin-bottom:10px;">
        <div style="background:{bg};border:1px solid {border};border-radius:8px;padding:12px 16px;max-width:70%;">
            <div style="font-size:13px;color:#e8edf5;line-height:1.6;">{msg['content']}</div>
            <div style="font-size:9px;color:#555;margin-top:6px;text-align:right;">{msg['time']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Quick question buttons
st.markdown('<div style="font-size:11px;font-weight:600;color:#7a8ba8;letter-spacing:1.5px;text-transform:uppercase;margin:16px 0 8px 0;font-family:\'JetBrains Mono\',monospace;">QUICK QUESTIONS</div>', unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)
quick_q = None
with q1:
    if st.button("🔥 Fire safety", use_container_width=True):
        quick_q = "What should I do in case of fire?"
with q2:
    if st.button("🏥 First aid", use_container_width=True):
        quick_q = "How to handle a medical emergency?"
with q3:
    if st.button("🚨 Security threat", use_container_width=True):
        quick_q = "What to do during a security threat?"
with q4:
    if st.button("🌍 Earthquake", use_container_width=True):
        quick_q = "What to do during an earthquake?"

# Input
user_input = st.chat_input("Ask about any emergency procedure...")

query = quick_q or user_input
if query:
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.chat_history.append({"role": "user", "content": query, "time": now})
    response = get_response(query)
    st.session_state.chat_history.append({"role": "assistant", "content": response, "time": now})
    st.rerun()
