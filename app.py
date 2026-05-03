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

        return text[:1000]  # limit text

    except Exception as e:
        print("Error fetching URL:", e)
        return ""

# 🔹 Highlight text safely
def highlight_text(text, results):
    try:
        for category, data in results.items():

            # handle both formats
            if isinstance(data, dict):
                words = data.get("matches", [])
            else:
                words = data

            for word in words:
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                text = pattern.sub(
                    f"<span style='color:red; font-weight:bold;'>{word}</span>",
                    text
                )

        return text

    except Exception as e:
        print("Highlight error:", e)
        return text


@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    score = 0
    risk = "Low"
    highlighted_text = ""

    try:
        if request.method == "POST":
            text = request.form.get("text", "")
            url = request.form.get("url", "")

            # If URL is provided
            if url.strip() != "":
                text = extract_text_from_url(url)

            if text.strip() != "":
                output = detect_dark_patterns(text)

                # handle return safely
                if isinstance(output, tuple):
                    result, score = output
                else:
                    result = output
                    score = sum(len(v) for v in result.values()) * 10

                # risk level
                if score < 30:
                    risk = "Low"
                elif score < 60:
                    risk = "Medium"
                else:
                    risk = "High"

                # highlight
                highlighted_text = highlight_text(text, result)

    except Exception as e:
        print("Main error:", e)

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
