def detect_dark_patterns(text):
    patterns = {
        "Urgency": {
            "keywords": ["hurry", "limited time", "act now", "buy now", "offer ends soon"],
            "weight": 15,
            "explanation": "Creates pressure to act quickly without thinking."
        },
        "Scarcity": {
            "keywords": ["only few left", "only 1 left", "last chance", "selling fast"],
            "weight": 20,
            "explanation": "Makes the product seem rare to push quick decisions."
        },
        "Pressure": {
            "keywords": ["don't miss", "exclusive deal", "grab now", "best deal"],
            "weight": 10,
            "explanation": "Encourages emotional buying instead of logical thinking."
        }
    }

    text = text.lower()
    results = {}
    total_score = 0

    for category, data in patterns.items():
        matches = [word for word in data["keywords"] if word in text]
        if matches:
            results[category] = {
                "matches": matches,
                "explanation": data["explanation"]
            }
            total_score += len(matches) * data["weight"]

    return results, total_score


# TEST
sample = "Hurry! Only 1 left. Limited time offer! Don't miss this deal!"
result, score = detect_dark_patterns(sample)

print("Results:", result)
print("Score:", score)
