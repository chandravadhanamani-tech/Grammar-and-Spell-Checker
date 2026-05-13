from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api.languagetool.org/v2/check"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_text():
    text = request.form['text']

    # API Request Payload
    data = {
        "text": text,
        "language": "en-US"
    }

    # Send request to LanguageTool API
    response = requests.post(API_URL, data=data)

    if response.status_code == 200:
        result = response.json()
        matches = result.get("matches", [])

        if not matches:
            return jsonify({"corrected_text": text})  # No errors, return original text

        # Apply corrections
        corrected_text = text
        for match in reversed(matches):  # Process in reverse to avoid shifting issues
            start, end = match["offset"], match["offset"] + match["length"]
            
            if match["replacements"]:  # Ensure there is a suggestion
                replacement = match["replacements"][0]["value"]
                corrected_text = corrected_text[:start] + replacement + corrected_text[end:]

        return jsonify({"corrected_text": corrected_text})

    else:
        return jsonify({"error": "Failed to connect to API"})

if __name__ == '__main__':
    app.run(debug=True)
