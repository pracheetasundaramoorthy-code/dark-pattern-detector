from flask import Flask, request, render_template
from detector import detect_dark_patterns
import requests
from bs4 import BeautifulSoup
import os
import re

app = Flask(__name__)

# 🔹 Extract text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except:
        return ""

# 🔹 Highlight detected words (SAFE VERSION)
def highlight_text(text, results):
    try:
        for category in results:
            words = results[category]["matches"] if isinstance(results[category], dict) else results[category]
            
            for word in words:
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                text = pattern.sub(
                    f"<span style='color:red; font-weight:bold;'>{word}</span>",
                    text
                )
        return text
    except:
        return text  # return original text if error

@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    score = 0
    risk = "Safe"
    highlighted_text = ""

    if request.method == "POST":
        text = request.form.get("text")
        url = request.form.get("url")

        # 🔹 If URL is given → extract text
        if url:
            text = extract_text_from_url(url)

        if text:
            output = detect_dark_patterns(text)

            # 🔹 Handle both return types safely
            if isinstance(output, tuple):
                result, score = output
            else:
                result = output
                score = sum(len(v) for v in result.values()) * 10

            # 🔹 Risk level
            if score < 30:
                risk = "Low"
            elif score < 60:
                risk = "Medium"
            else:
                risk = "High"

            # 🔹 Highlight text
            highlighted_text = highlight_text(text, result)

    return render_template(
        "index.html",
        result=result,
        score=score,
        risk=risk,
        highlighted_text=highlighted_text
    )

# 🔥 REQUIRED FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

