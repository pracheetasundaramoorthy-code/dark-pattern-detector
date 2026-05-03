from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from detector import analyze_text

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json["url"]

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        result = analyze_text(text)

        return jsonify({
            "status": "success",
            "score": result["score"],
            "patterns": result["detected_patterns"],
            "highlighted": result["highlighted"]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)
