# models/user_preferences.py

from flask import jsonify
from sqlalchemy.exc import IntegrityError
from __init__ import db
from model.user import User  # Ensure the User model is imported


class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    preference_id = db.Column(db.Integer, primary_key=True)  # Primary key for the preference
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)  # Foreign key to users table (updated to 'uid')
    categories = db.Column(db.JSON, nullable=False)  # List of preferred categories
    budget_min = db.Column(db.Numeric(10, 2), nullable=True)  # Minimum budget for the gift
    budget_max = db.Column(db.Numeric(10, 2), nullable=True)  # Maximum budget for the gift

    def __init__(self, uid, categories, budget_min=None, budget_max=None):
        self.uid = uid
        self.categories = categories
        self.budget_min = budget_min
        self.budget_max = budget_max

    def __repr__(self):
        return f"UserPreference(id={self.preference_id}, uid={self.uid}, categories={self.categories}, budget_min={self.budget_min}, budget_max={self.budget_max})"

    def create(self):
        """Creates a new user preference in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {"error": str(e)}
        return self

    def read(self):
        """Returns a dictionary representation of the user preference."""
        return {
            "preference_id": self.preference_id,
            "uid": self.uid,  # updated to 'uid'
            "categories": self.categories,
            "budget_min": float(self.budget_min) if self.budget_min is not None else None,
            "budget_max": float(self.budget_max) if self.budget_max is not None else None
        }

    def update(self, data):
        """Updates the user preference with new data."""
        self.categories = data.get('categories', self.categories)
        self.budget_min = data.get('budget_min', self.budget_min)
        self.budget_max = data.get('budget_max', self.budget_max)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {"error": str(e)}
        return self

    def delete(self):
        """Deletes the user preference from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {"error": str(e)}
        return self
