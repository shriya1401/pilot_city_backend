from sqlalchemy.exc import IntegrityError
from __init__ import db
from model.user import User  # Import User model for foreign key reference

# Survey Model
class Survey(db.Model):
    __tablename__ = 'surveys'  # Plural table name for consistency

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, message, user_id):
        self.message = message
        self.user_id = user_id

    def __repr__(self):
        return f"Survey(id={self.id}, message={self.message}, user_id={self.user_id})"

    def create(self):
        """Adds a new survey response to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise IntegrityError("Survey response creation failed due to a database error.")

    def read(self):
        """Returns a dictionary representation of the survey response."""
        return {
            'id': self.id,
            'message': self.message,
            'user_id': self.user_id
        }

    def delete(self):
        """Deletes the survey response from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise IntegrityError("Survey response deletion failed due to a database error.")

# Initialize sample survey responses
def init_surveys():
    """Initialize some sample survey responses in the database."""
    user = User.query.first()  # Ensure a user exists before creating sample data
    if user:
        sample_survey = Survey(message="Great experience!", user_id=user.id)
        try:
            sample_survey.create()
            print("Survey sample data initialized.")
        except IntegrityError as e:
            print(f"Error initializing survey data: {e}")
    else:
        print("No users found. Please create a user before initializing surveys.")
