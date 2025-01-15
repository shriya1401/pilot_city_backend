# userPreferences.py

# imports from flask
import logging
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from __init__ import app, db  # Assuming __init__.py initializes app and db
from datetime import datetime
from flask import request
from model.user import User  # Assuming User model is in the `user.py` file

# UserPreference Model
class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    preference_id = db.Column(db.Integer, primary_key=True)  # Primary key for the preference
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    theme = db.Column(db.String(255), default='light')  # Theme preference
    language = db.Column(db.String(255), default='English')  # Language preference

    def __init__(self, user_id, theme='light', language='English'):
        self.user_id = user_id
        self.theme = theme
        self.language = language

    def __repr__(self):
        return f"UserPreference(id={self.preference_id}, user_id={self.user_id}, theme={self.theme}, language={self.language})"

    def create(self):
        """Creates a new user preference in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error creating preference for user '{self.user_id}': {str(e)}")
            return None
        return self

    def read(self):
        """Returns a dictionary representation of the user preference."""
        return {
            "preference_id": self.preference_id,
            "user_id": self.user_id,
            "theme": self.theme,
            "language": self.language
        }

    def update(self, data):
        """Updates the user preference with new data."""
        self.theme = data.get('theme', self.theme)
        self.language = data.get('language', self.language)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error updating preference for user '{self.user_id}': {str(e)}")
            return None
        return self

    def delete(self):
        """Deletes the user preference from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error deleting preference for user '{self.user_id}': {str(e)}")
            return None
        return self

# Initialize sample user preferences
def initUserPreferences():
    """Initialize some sample user preferences in the database."""
    users = User.query.all()  # Fetch all users to assign preferences
    sample_preferences = [
        UserPreference(user_id=users[0].id, theme='dark', language='French'),
        UserPreference(user_id=users[1].id, theme='light', language='Spanish'),
        UserPreference(user_id=users[2].id, theme='dark', language='English'),
        # Add more sample data as needed
    ]
    for preference in sample_preferences:
        try:
            db.session.add(preference)
            db.session.commit()
            print(f"Preference created for user {preference.user_id}")
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Failed to create preference for user {preference.user_id}. Error: {str(e)}")

# API routes to interact with user preferences

@app.route('/user/preferences', methods=['GET'])
def get_user_preferences():
    """Returns a list of all user preferences."""
    preferences = UserPreference.query.all()
    return jsonify([preference.read() for preference in preferences])

@app.route('/user/<int:user_id>/preference', methods=['GET'])
def get_user_preference(user_id):
    """Returns the preferences of a specific user by their ID."""
    preference = UserPreference.query.filter_by(user_id=user_id).first()
    if preference:
        return jsonify(preference.read())
    return jsonify({'error': 'User preference not found'}), 404

@app.route('/user/<int:user_id>/preference', methods=['POST'])
def create_user_preference(user_id):
    """Creates a new preference for a user."""
    data = request.get_json()
    preference = UserPreference(
        user_id=user_id,
        theme=data.get('theme', 'light'),
        language=data.get('language', 'English')
    )
    preference.create()
    return jsonify(preference.read()), 201

@app.route('/user/<int:user_id>/preference', methods=['PUT'])
def update_user_preference(user_id):
    """Updates an existing preference for a user."""
    preference = UserPreference.query.filter_by(user_id=user_id).first()
    if preference:
        data = request.get_json()
        preference.update(data)
        return jsonify(preference.read())
    return jsonify({'error': 'User preference not found'}), 404

@app.route('/user/<int:user_id>/preference', methods=['DELETE'])
def delete_user_preference(user_id):
    """Deletes a user's preference."""
    preference = UserPreference.query.filter_by(user_id=user_id).first()
    if preference:
        preference.delete()
        return jsonify({'message': 'User preference deleted successfully'}), 200
    return jsonify({'error': 'User preference not found'}), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
