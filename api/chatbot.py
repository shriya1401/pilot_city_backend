from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.chatbot import Chatbot  # Import the Chatbot model

# Create a Blueprint for the chatbot API
chatbot_api = Blueprint('chatbot_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(chatbot_api)

class ChatbotAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new chatbot entry."""
            data = request.get_json()
            if not data or 'yesNo' not in data or 'user_id' not in data:
                return {"message": "Missing required fields"}, 400

            try:
                # Create a Chatbot instance with yesNo and user_id
                chatbot = Chatbot(
                    yesNo=data['yesNo'],
                    user_id=data['user_id']
                )
                chatbot.create()
                return jsonify(chatbot.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def get(self):
            """Retrieve a specific chatbot entry by ID."""
            data = request.get_json()
            if not data or 'chatbot_id' not in data:
                return {"message": "Chatbot ID required"}, 400

            chatbot = Chatbot.query.get(data['chatbot_id'])
            if not chatbot:
                return {"message": "Chatbot not found"}, 404

            return jsonify(chatbot.read())

        @token_required()
        def put(self):
            """Update an existing chatbot entry."""
            data = request.get_json()
            if not data or 'chatbot_id' not in data:
                return {"message": "Chatbot ID required"}, 400

            chatbot = Chatbot.query.get(data['chatbot_id'])
            if not chatbot:
                return {"message": "Chatbot not found"}, 404

            try:
                if 'yesNo' in data:
                    chatbot.yesNo = data['yesNo']
                if 'user_id' in data:
                    chatbot._user_id = data['user_id']
                chatbot.create()  # Call create() to save the changes
                return jsonify(chatbot.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def delete(self):
            """Delete a chatbot entry."""
            data = request.get_json()
            if not data or 'chatbot_id' not in data:
                return {"message": "Chatbot ID required"}, 400

            chatbot = Chatbot.query.get(data['chatbot_id'])
            if not chatbot:
                return {"message": "Chatbot not found"}, 404

            try:
                chatbot.delete()
                return {"message": "Chatbot deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all chatbots."""
            chatbots = Chatbot.query.all()
            return jsonify([chatbot.read() for chatbot in chatbots])

# Map API endpoints
api.add_resource(ChatbotAPI._CRUD, '/chatbot')
api.add_resource(ChatbotAPI._ALL, '/chatbots')
