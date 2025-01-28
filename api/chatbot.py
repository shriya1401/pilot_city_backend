import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app
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
            current_user = g.current_user  # Current user from token
            data = request.get_json()

            if not data or 'message' not in data:
                return {'message': 'Message is required'}, 400

            chatbot = Chatbot(
                message=data['message'],
                user_id=current_user.id
            )
            chatbot.create()
            return chatbot.read(), 201  # Directly return JSON-serializable dict with status code

        @token_required()
        def get(self):
            """Retrieve a specific chatbot entry by ID."""
            data = request.get_json()
            if not data or 'chatbot_id' not in data:
                return {"message": "Chatbot ID is required"}, 400

            chatbot = Chatbot.query.get(data['chatbot_id'])
            if not chatbot:
                return {"message": "Chatbot not found"}, 404

            return chatbot.read(), 200

        @token_required()
        def put(self):
            """Update an existing chatbot entry."""
            data = request.get_json()
            if not data or 'chatbot_id' not in data:
                return {"message": "Chatbot ID is required"}, 400

            chatbot = Chatbot.query.get(data['chatbot_id'])
            if not chatbot:
                return {"message": "Chatbot not found"}, 404

            if 'message' in data:
                chatbot.message = data['message']
            
            chatbot.update()
            return chatbot.read(), 200

        @token_required()
        def delete(self):
            """Delete a chatbot entry."""
            data = request.get_json()
            if not data or 'chatbot_id' not in data:
                return {"message": "Chatbot ID is required"}, 400

            chatbot = Chatbot.query.get(data['chatbot_id'])
            if not chatbot:
                return {"message": "Chatbot not found"}, 404

            chatbot.delete()
            return {"message": "Chatbot deleted successfully"}, 200

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all chatbot entries."""
            chatbots = Chatbot.query.all()
            return [chatbot.read() for chatbot in chatbots], 200

    class _BY_USER(Resource):
        @token_required()
        def get(self, user_id):
            """Retrieve chatbot entries by user ID."""
            chatbots = Chatbot.query.filter_by(user_id=user_id).all()
            if not chatbots:
                return {"message": "No chatbot entries found for this user"}, 404
            return [chatbot.read() for chatbot in chatbots], 200

# Map API endpoints
api.add_resource(ChatbotAPI._CRUD, '/chatbot')
api.add_resource(ChatbotAPI._ALL, '/chatbots')
api.add_resource(ChatbotAPI._BY_USER, '/chatbots/user/<int:user_id>')
