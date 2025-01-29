from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.survey import survey
from model.user import User  # Assuming User model is used for validation

# Blueprint and API setup
survey_api = Blueprint('survey_api', __name__, url_prefix='/api/survey')
api = Api(survey_api)

# Survey Resource: CRUD operations
class SurveyResource(Resource):
    def post(self):
        """Create a new survey message."""
        data = request.get_json()
        
        message = data.get('message')
        user_id = data.get('user_id')
        
        if not message or not user_id:
            return {"error": "Message and user_id are required"}, 400
        
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        # Create and save the survey message
        new_survey = survey(message=message, user_id=user_id)
        try:
            new_survey.create()
            return {"message": "Survey saved successfully", "data": new_survey.read()}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def get(self):
        """Fetch all survey messages."""
        surveys = survey.query.all()
        if surveys:
            return jsonify([s.read() for s in surveys])
        return {"message": "No surveys found"}, 404


class SurveyDetailResource(Resource):
    def get(self, survey_id):
        """Fetch a specific survey by ID."""
        survey_entry = survey.query.get(survey_id)
        if survey_entry:
            return jsonify(survey_entry.read())
        return {"error": "Survey not found"}, 404

    def delete(self, survey_id):
        """Delete a specific survey by ID."""
        survey_entry = survey.query.get(survey_id)
        if survey_entry:
            try:
                db.session.delete(survey_entry)
                db.session.commit()
                return {"message": "Survey deleted successfully"}, 200
            except Exception as e:
                db.session.rollback()
                return {"error": str(e)}, 500
        return {"error": "Survey not found"}, 404

# Add Resources to API
api.add_resource(SurveyResource, '/')
api.add_resource(SurveyDetailResource, '/survey')

