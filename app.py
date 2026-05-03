from flask import Flask, request, render_template
from detector import detect_dark_patterns
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# 🔹 Extract text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except:
        return ""

# 🔹 Highlight detected words
def highlight_text(text, results):
    text_lower = text.lower()

    for category in results:
        for word in results[category]["matches"]:
            if word in text_lower:
                text = text.replace(
                    word,
                    f"<span style='color:red; font-weight:bold;'>{word}</span>"
                )
    return text

@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    score = 0
    risk = "Safe"
    highlighted_text = ""

    if request.method == "POST":
        text = request.form.get("text")
        url = request.form.get("url")

        # If URL provided → extract text
        if url:
            text = extract_text_from_url(url)

        if text:
            result, score = detect_dark_patterns(text)

            # Risk level
            if score < 30:
                risk = "Low"
            elif score < 60:
                risk = "Medium"
            else:
                risk = "High"

            # Highlight words
            highlighted_text = highlight_text(text, result)

    return render_template(
        "index.html",
        result=result,
        score=score,
        risk=risk,
        highlighted_text=highlighted_text
    )

# 🔥 IMPORTANT FOR RENDER DEPLOYMENT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


