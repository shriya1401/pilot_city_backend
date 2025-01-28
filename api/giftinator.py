import os
import requests
from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
import google.generativeai as genai

# Configure the Google Generative AI model using an API key
genai.configure(api_key=os.environ.get('GOOGLE_GENERATIVEAI_API_KEY'))

# Model generation configuration
generation_config = {
    "temperature": 1.15,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative AI model
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
    ),
)

# Flask app initialization
app = Flask(__name__)

# Blueprint for Post API
gift_api = Blueprint('gift_api', __name__, url_prefix='/api/gift')
api = Api(gift_api)

# Backend URL placeholder
BACKEND_URL = "http://localhost:5000"  # Replace with actual backend URL


# Fetches chat history from the backend
def fetch_chat_history():
    try:
        response = requests.get(f"{BACKEND_URL}/get_chat")
        response.raise_for_status()
        return response.json().get("history", [])
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []


# Saves a chat entry to the backend
def save_chat_history(history_entry):
    try:
        response = requests.post(f"{BACKEND_URL}/save_chat", json=history_entry)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error saving chat history: {e}")
        return False


# Define the Chat Resource
class ChatResource(Resource):
    def post(self):
        user_input = request.json.get('user_input', '')
        if not user_input:
            return {"error": "No input provided"}, 400

        try:
            chat_history = fetch_chat_history()
            chat_session = model.start_chat(history=chat_history)
            response = chat_session.send_message(user_input)
            assistant_response = response.text

            user_entry = {"role": "user", "parts": [user_input]}
            assistant_entry = {"role": "assistant", "parts": [assistant_response]}

            save_chat_history(user_entry)
            save_chat_history(assistant_entry)

            return {"response": assistant_response}, 200
        except Exception as e:
            return {"error": str(e)}, 500


# Add ChatResource to the Blueprint's API
api.add_resource(ChatResource, '/chat')

# Register the Blueprint with the Flask app
app.register_blueprint(gift_api)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)