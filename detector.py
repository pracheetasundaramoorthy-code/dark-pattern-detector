import re

def detect_dark_patterns(text):
    score = 0
    patterns = []

    keywords = {
        "False Urgency": ["only", "hurry", "limited", "last chance"],
        "Scarcity": ["only 1 left", "few left", "selling fast"],
        "Pressure": ["buy now", "act now", "don't miss"],
        "Misleading Discount": ["% off", "deal", "offer ends"]
    }

    text_lower = text.lower()

    for category, words in keywords.items():
        for word in words:
            if word in text_lower:
                score += 10
                patterns.append((word, category))

    score = min(score, 100)

    return score, patterns

