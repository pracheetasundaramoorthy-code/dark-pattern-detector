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
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts/styles
        for tag in soup(["script", "style"]):
            tag.extract()

        text = ' '.join(soup.stripped_strings)

        return text[:1500]  # limit size

    except:
        return ""

# 🔹 Get only relevant sentences + highlight
def get_relevant_sentences(text, results):
    try:
        sentences = re.split(r'(?<=[.!?]) +', text)
        relevant = []

        for sentence in sentences:
            for category, data in results.items():

                words = data["matches"] if isinstance(data, dict) else data

                for word in words:
                    if word.lower() in sentence.lower():

                        pattern = re.compile(re.escape(word), re.IGNORECASE)
                        highlighted = pattern.sub(
                            f"<span style='color:red; font-weight:bold;'>{word}</span>",
                            sentence
                        )

                        relevant.append(highlighted)
                        break

        return relevant

    except:
        return []


@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    score = 0
    risk = "Low"
    highlighted_text = []

    if request.method == "POST":
        text = request.form.get("text", "")
        url = request.form.get("url", "")

        # URL input
        if url.strip():
            text = extract_text_from_url(url)

        if text.strip():
            output = detect_dark_patterns(text)

            # Handle return
            if isinstance(output, tuple):
                result, score = output
            else:
                result = output
                score = sum(len(v) for v in result.values()) * 10

            # Risk level
            if score < 30:
                risk = "Low"
            elif score < 60:
                risk = "Medium"
            else:
                risk = "High"

            # Get relevant sentences
            highlighted_text = get_relevant_sentences(text, result)

    return render_template(
        "index.html",
        result=result,
        score=score,
        risk=risk,
        highlighted_text=highlighted_text
    )


# 🔥 Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
