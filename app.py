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
            # Headers to avoid blocking by websites
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }

            # Fetch webpage
            response = requests.get(url, headers=headers, timeout=10)

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract visible text
            text = soup.get_text(separator=' ', strip=True)

            # Detect dark patterns
            score, patterns = detect_dark_patterns(text)

            # Generate message based on score
            if score > 70:
                message = "⚠️ Highly Manipulative: Uses urgency, pressure, or misleading tactics."
            elif score > 30:
                message = "⚠️ Suspicious: Some dark patterns detected."
            else:
                message = "✅ Safe: No strong manipulation detected."

            # Prepare result
            result = {
                "score": score,
                "patterns": patterns,
                "message": message
            }

        except requests.exceptions.RequestException:
            result = {
                "error": "❌ Unable to fetch the website. It may block scraping or the URL is invalid."
            }

        except Exception as e:
            result = {
                "error": "❌ Something went wrong while analyzing the page."
            }

    return render_template('index.html', result=result)


# REQUIRED for deployment (Render / production)
if __name__ == "__main__":
    app.run()

