import re

def detect_dark_patterns(text):
    score = 0
    patterns = []
    highlights = []

    text = text.lower()

    urgency_patterns = ["only \\d+ left", "hurry", "limited time", "last chance"]
    confirm_patterns = ["no thanks", "i don't want", "skip and lose"]

    # Urgency detection
    for pattern in urgency_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            score += 10
            patterns.append("Fake urgency detected")
            highlights.append(m)

    # Confirm shaming
    for phrase in confirm_patterns:
        if phrase in text:
            score += 15
            patterns.append("Confirm shaming detected")
            highlights.append(phrase)

    return score, patterns, highlights
