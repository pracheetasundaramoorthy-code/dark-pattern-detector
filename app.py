from flask import Flask, request, render_template
from detector import detect_dark_patterns
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to extract text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except:
        return ""

@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    score = 0
    risk = "Safe"

    if request.method == "POST":
        text = request.form.get("text")
        url = request.form.get("url")

        # If URL is given → extract text
        if url:
            text = extract_text_from_url(url)

        # Run detection
        if text:
            result, score = detect_dark_patterns(text)

            if score < 30:
                risk = "Low"
            elif score < 60:
                risk = "Medium"
            else:
                risk = "High"

    return render_template("index.html", result=result, score=score, risk=risk)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

