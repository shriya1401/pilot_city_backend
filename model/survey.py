from sqlite3 import IntegrityError
from __init__ import db
from model.user import User  # Assuming User is needed for valid user references


class survey(db.Model):
    __tablename__ = 'survey'  # Changed to reflect the new file name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _message = db.Column(db.String(255), nullable=False)
    _user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
   
    def __init__(self, message, user_id):
        self._message = message
        self._user_id = user_id


    @property
    def message(self):
        return self._message


    @message.setter
    def message(self, value):
        self._message = value


    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    def read(self):
        return {
            'id': self.id,
            'message': self._message,
            'user_id': self._user_id,
        }


def initsurvey():
    """Initialize sample data for the survey table."""
    user = User.query.first()  # Assuming at least one user exists
    if user:
        sample_chat = survey(message="good", user_id=user.id)
        try:
            sample_chat.create()
            print("survey sample data initialized.")
        except Exception as e:
            print(f"Error initializing survey data: {e}")
    else:
        print("No users found. Please create a user before initializing survey.")