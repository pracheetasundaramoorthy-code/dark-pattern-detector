from flask import Flask, request, render_template
from detector import detect_dark_patterns
import requests
from bs4 import BeautifulSoup
import os
import re

app = Flask(__name__)

# 🔹 Extract text from URL (with headers to avoid blocking)
def extract_text_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return "Unable to fetch content."

        soup = BeautifulSoup(response.text, "html.parser")

        # remove scripts/styles
        for tag in soup(["script", "style"]):
            tag.extract()

        text = ' '.join(soup.stripped_strings)

        return text[:2000]  # limit size

    except Exception as e:
        print("URL Error:", e)
        return "Unable to fetch content."


# 🔹 Extract relevant sentences + highlight
def get_relevant_sentences(text, results):
    sentences = re.split(r'(?<=[.!?]) +', text)
    output = []

    for sentence in sentences:
        for category, data in results.items():
            words = data.get("matches", [])

            for word in words:
                if word.lower() in sentence.lower():

                    pattern = re.compile(re.escape(word), re.IGNORECASE)
                    highlighted = pattern.sub(
                        f"<span style='color:red; font-weight:bold;'>{word}</span>",
                        sentence
                    )

                    output.append(highlighted)
                    break

    return output


@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    score = 0
    risk = "Low"
    highlighted_text = []

    if request.method == "POST":
        text = request.form.get("text", "")
        url = request.form.get("url", "")

        # 🔹 URL input
        if url.strip():
            text = extract_text_from_url(url)

        # 🔹 ALWAYS run detection (even if text small)
        if text:
            result, score = detect_dark_patterns(text)

            # 🔹 risk level
            if score < 30:
                risk = "Low"
            elif score < 60:
                risk = "Medium"
            else:
                risk = "High"

            # 🔹 relevant sentences
            highlighted_text = get_relevant_sentences(text, result)

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
