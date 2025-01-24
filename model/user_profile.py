# userprofile.py

# imports from flask
import logging
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from __init__ import app, db  # Assuming __init__.py initializes app and db
from datetime import datetime
from flask import request
from model.user import User  # Assuming User model is in the `user.py` file

# Userprofile Model
class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    profile_id = db.Column(db.Integer, primary_key=True)  # Primary key for the profile
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    name = db.Column(db.String(255), default='toby')  # name profile
    password = db.Column(db.String(255), default='123Qwerty!')  # password profile

    def __init__(self, user_id, name='toby', password='123Qwerty!'):
        self.user_id = user_id
        self.name = name
        self.password = password

    def __repr__(self):
        return f"Userprofile(id={self.profile_id}, user_id={self.user_id}, name={self.name}, password={self.password})"

    def create(self):
        """Creates a new user profile in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error creating profile for user '{self.user_id}': {str(e)}")
            return None
        return self

    def read(self):
        """Returns a dictionary representation of the user profile."""
        return {
            "profile_id": self.profile_id,
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password
        }

    def update(self, data):
        """Updates the user profile with new data."""
        self.name = data.get('name', self.name)
        self.password = data.get('password', self.password)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error updating profile for user '{self.user_id}': {str(e)}")
            return None
        return self

    def delete(self):
        """Deletes the user profile from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error deleting profile for user '{self.user_id}': {str(e)}")
            return None
        return self

# Initialize sample user profile
def initUserProfile():
    """Initialize some sample user profile in the database."""
    users = User.query.all()  # Fetch all users to assign profile
    sample_profile = [
        UserProfile(user_id=users[0].id, name='mort', password='csp123'),
        UserProfile(user_id=users[1].id, name='toby', password='123Qwerty!'),
        UserProfile(user_id=users[2].id, name='rando', password='password'),
        # Add more sample data as needed
    ]
    for profile in sample_profile:
        try:
            db.session.add(profile)
            db.session.commit()
            print(f"profile created for user {profile.user_id}")
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Failed to create profile for user {profile.user_id}. Error: {str(e)}")

# API routes to interact with user profile

@app.route('/user/profiles', methods=['GET'])
def get_user_profiles():
    """Returns a list of all user profile."""
    profiles = UserProfile.query.all()
    return jsonify([profile.read() for profile in profiles])

@app.route('/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    """Returns the profile of a specific user by their ID."""
    profiles = UserProfile.query.filter_by(user_id=user_id).first()
    if profiles:
        return jsonify(profiles.read())
    return jsonify({'error': 'User profile not found'}), 404

@app.route('/user/<int:user_id>/profile', methods=['POST'])
def create_user_profile(user_id):
    """Creates a new profile for a user."""
    data = request.get_json()
    profile = UserProfile(
        user_id=user_id,
        name=data.get('name', 'toby'),
        password=data.get('password', 'password')
    )
    profile.create()
    return jsonify(profile.read()), 201

@app.route('/user/<int:user_id>/profile', methods=['PUT'])
def update_user_profile(user_id):
    """Updates an existing profile for a user."""
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if profile:
        data = request.get_json()
        profile.update(data)
        return jsonify(profile.read())
    return jsonify({'error': 'User profile not found'}), 404

@app.route('/user/<int:user_id>/profile', methods=['DELETE'])
def delete_user_profile(user_id):
    """Deletes a user's profile."""
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if profile:
        profile.delete()
        return jsonify({'message': 'User profile deleted successfully'}), 200
    return jsonify({'error': 'User profile not found'}), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
