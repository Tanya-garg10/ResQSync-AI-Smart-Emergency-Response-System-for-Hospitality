"""AI Emergency Classification & Severity Scoring."""
import random


# Keyword-based classification (works offline, no API needed)
KEYWORDS = {
    "FIRE": ["fire", "smoke", "burning", "flames", "aag", "jalana", "dhua"],
    "MEDICAL": ["medical", "heart", "bleeding", "unconscious", "pain", "doctor",
                 "ambulance", "dard", "doctor", "tabiyat", "bimaari"],
    "SECURITY": ["security", "theft", "attack", "intruder", "weapon", "gun",
                  "threat", "chor", "hamla", "khatra"],
}

SEVERITY_WEIGHTS = {
    "fire": 0.9, "smoke": 0.7, "burning": 0.95, "flames": 0.95,
    "heart": 0.9, "bleeding": 0.85, "unconscious": 0.95, "pain": 0.5,
    "attack": 0.9, "weapon": 0.95, "gun": 0.95, "intruder": 0.8,
    "theft": 0.6, "help": 0.5, "emergency": 0.7,
}


def classify_emergency(text: str) -> dict:
    """Classify emergency type from text input."""
    text_lower = text.lower()
    scores = {}
    for etype, keywords in KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[etype] = score

    if not scores:
        # Default to security if "help" or "emergency" detected
        if any(w in text_lower for w in ["help", "emergency", "bachao", "madad"]):
            return {"type": "SECURITY", "confidence": 0.6}
        return {"type": "UNKNOWN", "confidence": 0.0}

    best_type = max(scores, key=scores.get)
    confidence = min(scores[best_type] / 3.0, 1.0)
    return {"type": best_type, "confidence": round(confidence, 2)}


def calculate_severity(text: str) -> dict:
    """Calculate severity score from text."""
    text_lower = text.lower()
    max_weight = 0.0
    matched_words = []

    for word, weight in SEVERITY_WEIGHTS.items():
        if word in text_lower:
            matched_words.append(word)
            max_weight = max(max_weight, weight)

    if max_weight >= 0.85:
        level = "CRITICAL"
    elif max_weight >= 0.65:
        level = "PRIORITY"
    elif max_weight >= 0.4:
        level = "MODERATE"
    elif max_weight > 0:
        level = "LOW"
    else:
        level = "LOW"
        max_weight = 0.2

    return {
        "level": level,
        "score": round(max_weight, 2),
        "matched_keywords": matched_words,
    }


def full_analysis(text: str) -> dict:
    """Run full classification + severity analysis."""
    classification = classify_emergency(text)
    severity = calculate_severity(text)
    return {
        "input_text": text,
        "type": classification["type"],
        "confidence": classification["confidence"],
        "severity": severity["level"],
        "severity_score": severity["score"],
        "keywords_detected": severity["matched_keywords"],
    }
