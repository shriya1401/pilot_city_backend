import os
import requests
from flask import request, jsonify
import google.generativeai as genai

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
    system_instruction="You are an assistant capable of answering questions and having conversations."
)

# Backend endpoints
BACKEND_URL = "http://localhost:5000"  # Replace with actual backend URL

def fetch_chat_history():
    """Fetch chat history from the user's backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/get_chat")
        response.raise_for_status()
        return response.json().get("history", [])
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []

def save_chat_history(history_entry):
    """Save a single chat entry to the user's backend."""
    try:
        response = requests.post(f"{BACKEND_URL}/save_chat", json=history_entry)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error saving chat history: {e}")
        return False

# Define the chat endpoint
def chat_endpoint(app):
    @app.route('/chat', methods=['POST'])
    def chat():
        user_input = request.json.get('user_input', '')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        try:
            # Fetch existing chat history from backend
            chat_history = fetch_chat_history()

            # Start chat session
            chat_session = model.start_chat(history=chat_history)
            response = chat_session.send_message(user_input)

            # Update chat history
            assistant_response = response.text
            user_entry = {"role": "user", "parts": [user_input]}
            assistant_entry = {"role": "assistant", "parts": [assistant_response]}

            # Save to backend
            save_chat_history(user_entry)
            save_chat_history(assistant_entry)

            return jsonify({"response": assistant_response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
