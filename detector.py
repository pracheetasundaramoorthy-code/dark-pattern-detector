DARK_PATTERNS = {
    "scarcity": ["only", "left in stock", "selling fast", "limited time"],
    "urgency": ["hurry", "deal ends", "last chance", "today only"],
    "hidden_costs": ["extra charges", "fees apply", "shipping not included"],
    "forced_action": ["subscribe", "sign up required", "must create account"],
    "misleading_discount": ["50% off", "up to", "starting at"]
}

def analyze_text(text):
    text = text.lower()

    detected = []
    highlighted = []
    score = 0

    for pattern, keywords in DARK_PATTERNS.items():
        for kw in keywords:
            if kw in text:
                detected.append(pattern)
                highlighted.append(kw)
                score += 20

    score = min(score, 100)

    return {
        "score": score,
        "detected_patterns": list(set(detected)),
        "highlighted": highlighted
    }
