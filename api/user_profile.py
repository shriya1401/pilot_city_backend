# userprofiles.py in the API
from flask import Blueprint, request, jsonify, Flask
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.user_profile import UserProfile  # Import the Userprofile model
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={
    "/api/*": {
        "origins": "http://127.0.0.1:4887",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
    }
})

# Create a Blueprint for the user profiles API
user_profile_api = Blueprint('user_profile_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(user_profile_api)

class UserProfileAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new user profile."""
            data = request.get_json()
            if not data or 'user_id' not in data:
                return {"message": "User ID is required"}, 400

            try:
                # Create a Userprofile instance
                profile = UserProfile(
                    user_id=data['user_id'],
                    name=data.get('name', 'toby'),
                    password=data.get('password', '123Qwerty!')
                )
                profile.create()
                return jsonify(profile.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def get(self):
            """Retrieve a specific user profile by user ID."""
            data = request.get_json()
            if not data or 'user_id' not in data:
                return {"message": "User ID required"}, 400

            profile = UserProfile.query.filter_by(user_id=data['user_id']).first()
            if not profile:
                return {"message": "User profile not found"}, 404

            return jsonify(profile.read())

        @token_required()
        def put(self):
            """Update an existing user profile."""
            data = request.get_json()
            if not data or 'user_id' not in data:
                return {"message": "User ID required"}, 400

            profile = UserProfile.query.filter_by(user_id=data['user_id']).first()
            if not profile:
                return {"message": "User profile not found"}, 404

            try:
                profile.update(data)
                return jsonify(profile.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def delete(self):
            """Delete a user profile."""
            data = request.get_json()
            if not data or 'user_id' not in data:
                return {"message": "User ID required"}, 400

            profile = UserProfile.query.filter_by(user_id=data['user_id']).first()
            if not profile:
                return {"message": "User profile not found"}, 404

            try:
                profile.delete()
                return {"message": "User profile deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all user profiles."""
            profiles = UserProfile.query.all()
            return jsonify([profile.read() for profile in profiles])

# Map API endpoints
api.add_resource(UserProfileAPI._CRUD, '/user_profile')
api.add_resource(UserProfileAPI._ALL, '/user_profiles')
