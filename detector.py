def detect_dark_patterns(text):
    patterns = {
        "Urgency": ["hurry", "limited time", "ending soon"],
        "Scarcity": ["only few left", "only 1 left", "limited stock"],
        "Pressure": ["buy now", "order now", "add to cart"],
        "Social Proof": ["bought", "ratings", "reviews"],
        "Discount": ["% off", "discount", "deal", "offer"]
    }

    text_lower = text.lower()
    results = {}
    score = 0

    for category, keywords in patterns.items():
        matches = [k for k in keywords if k in text_lower]

        if matches:
            results[category] = {
                "matches": matches,
                "explanation": f"{category} pattern detected"
            }
            score += len(matches) * 10

    return results, score

           
