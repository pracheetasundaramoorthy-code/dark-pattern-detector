from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from detector import detect_dark_patterns

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        url = request.form.get('url')

        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract visible text
            text = soup.get_text(separator=' ')

            # Detect dark patterns
            score, patterns = detect_dark_patterns(text)

            # Message based on score
            if score > 70:
                message = "⚠️ Highly Manipulative Website"
            elif score > 30:
                message = "⚠️ Suspicious Website"
            else:
                message = "✅ Seems Safe"

            result = {
                "score": score,
                "patterns": patterns,
                "message": message
            }

        except Exception as e:
            result = {
                "error": "Unable to fetch or analyze the URL"
            }

    return render_template('index.html', result=result)


# IMPORTANT: Required for deployment
if __name__ == "__main__":
    app.run()

