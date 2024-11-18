import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Securely retrieve API key
API_KEY = os.getenv("GHOST_AI_API_KEY")
API_ENDPOINT = "https://the-ghost-ai-backend-005c5dcbf4a6.herokuapp.com/transformations/humanize/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/humanize', methods=['POST'])
def humanize_text():
    # Validate API key
    if not API_KEY:
        return jsonify({"error": "API key is missing"}), 500
    
    # Validate input
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    input_text = data.get("text")
    intensity = data.get("humanizerIntensity", "HIGH")
    purpose = data.get("purpose", "GENERAL")
    literacy_level = data.get("literacyLevel", "COLLEGE")

    # Prepare payload for Ghost AI
    payload = {
        "text": input_text,
        "humanizerIntensity": intensity,
        "purpose": purpose,
        "literacyLevel": literacy_level
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Make API request
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        return jsonify({
            "humanized_text": result.get("output"),
            "input_text": input_text
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", True))