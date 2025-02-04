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

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:4887"}}, supports_credentials=True)



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
@app.route('/chat', methods=['OPTIONS'])
def chat_preflight():
    response = jsonify({'message': 'CORS preflight request success'})
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:4887")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200



# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8206)