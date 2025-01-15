# userPreferences.py in the API
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.userPreferences import UserPreference  # Import the UserPreference model

# Create a Blueprint for the user preferences API
user_preference_api = Blueprint('user_preference_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(user_preference_api)

class UserPreferenceAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new user preference."""
            data = request.get_json()
            if not data or 'user_id' not in data:
                return {"message": "User ID is required"}, 400

            try:
                # Create a UserPreference instance
                preference = UserPreference(
                    user_id=data['user_id'],
                    theme=data.get('theme', 'light'),
                    language=data.get('language', 'English')
                )
                preference.create()
                return jsonify(preference.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def get(self):
            """Retrieve a specific user preference by user ID."""
            data = request.get_json()
            if not data or 'user_id' not in data:
                return {"message": "User ID required"}, 400

            preference = UserPreference.query.filter_by(user_id=data['user_id']).first()
            if not preference:
                return {"message": "User preference not found"}, 404

            return jsonify(preference.read())

        @token_required()
        def put(self):
            """Update an existing user preference."""
            data = request.get_json()
            if not data or 'user_id' not in data:
                return {"message": "User ID required"}, 400

            preference = UserPreference.query.filter_by(user_id=data['user_id']).first()
            if not preference:
                return {"message": "User preference not found"}, 404

            try:
                preference.update(data)
                return jsonify(preference.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def delete(self):
            """Delete a user preference."""
            data = request.get_json()
            if not data or 'user_id' not in data:
                return {"message": "User ID required"}, 400

            preference = UserPreference.query.filter_by(user_id=data['user_id']).first()
            if not preference:
                return {"message": "User preference not found"}, 404

            try:
                preference.delete()
                return {"message": "User preference deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all user preferences."""
            preferences = UserPreference.query.all()
            return jsonify([preference.read() for preference in preferences])

# Map API endpoints
api.add_resource(UserPreferenceAPI._CRUD, '/user_preference')
api.add_resource(UserPreferenceAPI._ALL, '/user_preferences')
