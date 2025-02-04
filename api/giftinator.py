import os
import requests
from flask import request, jsonify, Flask
import google.generativeai as genai
from flask_cors import CORS

# Configure AI model
genai.configure(api_key=os.environ.get('GOOGLE_GENERATIVEAI_API_KEY'))

generation_config = {
    "temperature": 1.15,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are an expert in suggesting gifts for people. Your task is to engage "
        "in conversations about gift-giving and provide thoughtful suggestions. "
        "Understand the user’s preferences, occasion, and budget to offer personalized "
        "gift ideas. Use relatable examples, humor, and creativity to make the interaction "
        "enjoyable. Ask clarifying questions to better understand the recipient’s personality "
        "and interests. Offer practical tips for wrapping, presenting, or adding a personal touch "
        "to the gift. Tailor suggestions to fit a range of scenarios, from simple and inexpensive "
        "to elaborate and luxurious."
        "Also when giving suggestions, provide some trending product descriptions, prices, "
        "customer ratings, and where to find the item."
    ),
)

# Initialize Flask app
app = Flask(__name__)

# Apply CORS settings to the app
CORS(app, supports_credentials=True, resources={
    "/chat": {
        "origins": "http://127.0.0.1:4887",  # Exact origin of frontend
        "methods": ["POST"],  # Allowed HTTP methods
        "allow_headers": ["Content-Type", "Authorization"],  # Allowed headers
    }
})

# Define the chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Generate chatbot response
        chat_session = model.start_chat()
        response = chat_session.send_message(user_input)

        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ensure CORS headers are added to all responses
@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:4887"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST"
    return response

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8887)