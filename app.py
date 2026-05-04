from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from detector import detect_dark_patterns

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None

    if request.method == 'POST':
        url = request.form['url']

        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract visible text properly
            texts = soup.stripped_strings
            page_text = " ".join(texts)

            score, patterns, highlights = detect_dark_patterns(page_text)

            result = {
                "score": score,
                "patterns": patterns,
                "highlights": highlights
            }

        except Exception as e:
            result = {"error": "Invalid or blocked URL"}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)


