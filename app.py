from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Simple dark pattern keywords (you can expand later)
DARK_PATTERNS = {
    "scarcity": ["only", "left in stock", "selling fast", "limited time"],
    "urgency": ["hurry", "deal ends", "last chance", "today only"],
    "hidden_costs": ["extra charges", "fees apply", "shipping not included"],
    "forced_action": ["subscribe", "sign up required", "must create account"],
    "misleading_discount": ["50% off*", "up to", "starting at"]
}

def analyze_text(text):
    text_lower = text.lower()

    detected = []
    score = 0
    highlighted = []

    for pattern, keywords in DARK_PATTERNS.items():
        for kw in keywords:
            if kw in text_lower:
                detected.append(pattern)
                score += 20
                highlighted.append(kw)

    score = min(score, 100)

    return {
        "score": score,
        "detected_patterns": list(set(detected)),
        "highlighted_keywords": highlighted
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    url = data.get("url")

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        # extract visible text
        text = soup.get_text(separator=" ")

        result = analyze_text(text)

        return jsonify({
            "status": "success",
            "url": url,
            "manipulation_score": result["score"],
            "detected_patterns": result["detected_patterns"],
            "highlighted_text": result["highlighted_keywords"]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)

