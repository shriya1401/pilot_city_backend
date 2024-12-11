import os
from flask import Flask, request, jsonify
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

# Chat history
chat_history = []

# Define the chat endpoint
def chat_endpoint(app):
    @app.route('/chat', methods=['POST'])
    def chat():
        user_input = request.json.get('user_input', '')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        try:
            # Start chat session
            chat_session = model.start_chat(history=chat_history)
            response = chat_session.send_message(user_input)

            # Update chat history
            assistant_response = response.text
            chat_history.append({"role": "user", "parts": [user_input]})
            chat_history.append({"role": "assistant", "parts": [assistant_response]})

            return jsonify({"response": assistant_response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
