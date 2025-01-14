from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class Nora(db.Model):
    __tablename__ = 'Nora'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _message = db.Column(db.String(255), nullable=False)
    _user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, message, user_id):
        self._message = message
        self._user_id = user_id 

    @property
    def message(self):
        return self._message

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

    @staticmethod
    def initNoras():
        """
        Initialize the Nora table with sample data.
        """
        sample_messages = [
            {"message": "Welcome to the system!", "user_id": 1},
            {"message": "Here is another test message.", "user_id": 2},
        ]

        for sample in sample_messages:
            try:
                nora = Nora(message=sample["message"], user_id=sample["user_id"])
                db.session.add(nora)
            except IntegrityError:
                db.session.rollback()
        db.session.commit()

    @staticmethod
    def restore(data):
        """
        Restore Nora entries from JSON data.
        """
        for entry in data:
            try:
                nora = Nora(message=entry['message'], user_id=entry['user_id'])
                db.session.add(nora)
            except IntegrityError:
                db.session.rollback()
        db.session.commit()
