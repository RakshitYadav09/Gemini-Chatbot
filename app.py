from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

from flask_cors import CORS  # Allows frontend access

app = Flask(__name__)
CORS(app)  # Enables CORS for frontend interaction
from dotenv import load_dotenv
load_dotenv()


# Get API Key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY environment variable not set!")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

@app.route('/')
def home():
    return render_template('index.html')  # Make sure index.html exists in a 'templates' folder

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()  # Read JSON request
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400

    user_message = data['message']
    try:
        response = model.generate_content(user_message)

        # Ensure response contains text
        if response and hasattr(response, "candidates") and response.candidates:
            response_text = response.candidates[0].content.parts[0].text
        else:
            response_text = "Sorry, I couldn't generate a response."

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
