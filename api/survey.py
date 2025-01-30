from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError
from __init__ import db
from model.survey import Survey
from api.jwt_authorize import token_required

survey_api = Blueprint('survey_api', __name__, url_prefix='/api')
api = Api(survey_api)

class SurveyAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new survey response."""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'message' not in data:
                return {'message': 'Survey message is required'}, 400

            survey_response = Survey(
                message=data['message'],
                user_id=current_user.id
            )

            try:
                survey_response.create()
                # Directly return the dictionary from `read()`
                return survey_response.read(), 201
            except IntegrityError:
                return {'message': 'Survey creation failed due to database error'}, 500

        @token_required()
        def get(self):
            """Retrieve a survey response by ID."""
            survey_id = request.args.get('id')  # Get 'id' from query parameter
            if not survey_id:
                return {'message': 'Survey ID required'}, 400

            survey_response = Survey.query.get(survey_id)
            if not survey_response:
                return {'message': 'Survey response not found'}, 404

            # Directly return the dictionary from `read()`
            return survey_response.read()

        @token_required()
        def delete(self):
            """Delete a survey response by ID."""
            survey_id = request.args.get('id')  # Get 'id' from query parameter
            if not survey_id:
                return {'message': 'Survey ID required'}, 400

            survey_response = Survey.query.get(survey_id)
            if not survey_response:
                return {'message': 'Survey response not found'}, 404

            try:
                survey_response.delete()
                return {'message': 'Survey response deleted successfully'}, 200
            except IntegrityError:
                return {'message': 'Survey deletion failed due to database error'}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all survey responses."""
            surveys = Survey.query.all()
            # Directly return a list of dictionaries from `read()`
            return [survey.read() for survey in surveys]

    class _BY_USER(Resource):
        @token_required()
        def get(self, user_id):
            """Retrieve all survey responses by a specific user."""
            surveys = Survey.query.filter_by(user_id=user_id).all()
            if not surveys:
                return {'message': 'No survey responses found for this user'}, 404
            # Directly return a list of dictionaries from `read()`
            return [survey.read() for survey in surveys]

# Map API endpoints
api.add_resource(SurveyAPI._CRUD, '/survey')
api.add_resource(SurveyAPI._ALL, '/surveys')
api.add_resource(SurveyAPI._BY_USER, '/surveys/user/<int:user_id>')