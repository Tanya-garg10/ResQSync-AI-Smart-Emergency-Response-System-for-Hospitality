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


def process_voice_input(text: str) -> dict:
    """Full voice processing pipeline."""
    language = detect_language(text)
    detection = detect_emergency_keywords(text)
    return {
        **detection,
        "language": language,
        "language_name": "Hindi" if language == "hi" else "English",
    }
