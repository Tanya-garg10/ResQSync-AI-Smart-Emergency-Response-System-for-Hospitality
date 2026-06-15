"""Voice Detection & Speech-to-Text Service."""


EMERGENCY_KEYWORDS_EN = [
    "help", "fire", "emergency", "ambulance", "police", "attack",
    "bleeding", "smoke", "danger", "save", "sos", "bomb", "gun",
]

EMERGENCY_KEYWORDS_HI = [
    "bachao", "madad", "aag", "emergency", "police", "hamla",
    "khoon", "dhua", "khatra", "doctor", "bomb", "bandook",
]

ALL_KEYWORDS = set(EMERGENCY_KEYWORDS_EN + EMERGENCY_KEYWORDS_HI)


def detect_emergency_keywords(text: str) -> dict:
    """Detect emergency keywords in transcribed text."""
    text_lower = text.lower()
    found = [kw for kw in ALL_KEYWORDS if kw in text_lower]
    is_emergency = len(found) > 0
    return {
        "is_emergency": is_emergency,
        "keywords_found": found,
        "keyword_count": len(found),
        "original_text": text,
    }


def detect_language(text: str) -> str:
    """Simple language detection (Hindi vs English)."""
    hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    hindi_words = sum(1 for w in EMERGENCY_KEYWORDS_HI if w in text.lower())
    if hindi_chars > 2 or hindi_words > 0:
        return "hi"
    return "en"


def detect_emotion(text: str) -> dict:
    """Detect emotional state from text content."""
    text_lower = text.lower()

    panic_words = ["help", "bachao", "please", "!!", "!", "hurry", "fast", "jaldi", "quick", "now", "god", "oh no"]
    fear_words = ["scared", "afraid", "dangerous", "danger", "khatra", "darr", "weapon", "gun", "attack"]
    distress_words = ["hurt", "pain", "bleeding", "dard", "taklif", "unconscious", "injured"]
    calm_words = ["need", "require", "please send", "inform", "report"]

    panic_score = sum(1 for w in panic_words if w in text_lower)
    fear_score = sum(1 for w in fear_words if w in text_lower)
    distress_score = sum(1 for w in distress_words if w in text_lower)
    exclamation_count = text.count("!")

    total_panic = panic_score + (1 if exclamation_count >= 2 else 0)

    if total_panic >= 3 or exclamation_count >= 3:
        return {"emotion": "PANIC", "icon": "😱", "score": min(1.0, total_panic / 5)}
    elif fear_score >= 2:
        return {"emotion": "FEAR", "icon": "😨", "score": min(1.0, fear_score / 4)}
    elif distress_score >= 1 or panic_score >= 1:
        return {"emotion": "DISTRESS", "icon": "😰", "score": min(1.0, distress_score / 3)}
    else:
        return {"emotion": "CONCERNED", "icon": "😟", "score": 0.3}


def detect_stress_level(text: str) -> dict:
    """Detect stress level from language patterns."""
    text_lower = text.lower()

    high_stress_markers = ["!!", "!!!", "help", "bachao", "please", "hurry", "now", "fast", "jaldi", "sos"]
    medium_stress_markers = ["urgent", "need", "injured", "smoke", "fire", "danger", "emergency"]
    repetition = len(text) > 0 and any(text_lower.count(w) > 1 for w in ["help", "fire", "aag", "bachao"])

    high_score = sum(1 for w in high_stress_markers if w in text_lower) + text.count("!")
    medium_score = sum(1 for w in medium_stress_markers if w in text_lower)

    if high_score >= 3 or repetition:
        level = "HIGH"
        indicators = [w for w in high_stress_markers if w in text_lower][:4]
    elif high_score >= 1 or medium_score >= 2:
        level = "MEDIUM"
        indicators = [w for w in medium_stress_markers if w in text_lower][:3]
    else:
        level = "LOW"
        indicators = []

    return {"level": level, "indicators": indicators}


def process_voice_input(text: str) -> dict:
    """Full voice processing pipeline."""
    language = detect_language(text)
    detection = detect_emergency_keywords(text)

    # Language breakdown detail
    hindi_words_found = [w for w in EMERGENCY_KEYWORDS_HI if w in text.lower()]
    english_words_found = [w for w in EMERGENCY_KEYWORDS_EN if w in text.lower()]

    if language == "hi" and english_words_found:
        lang_name = "Hinglish"
        lang_detail = f"Hindi markers: {len(hindi_words_found)} | English markers: {len(english_words_found)} | Mixed input detected"
    elif language == "hi":
        lang_name = "Hindi"
        lang_detail = f"Hindi markers: {len(hindi_words_found)} | Devanagari script or Hindi keywords detected"
    else:
        lang_name = "English"
        lang_detail = f"English markers: {len(english_words_found)} | Standard English input"

    return {
        **detection,
        "language": language,
        "language_name": lang_name,
        "language_detail": lang_detail,
    }
