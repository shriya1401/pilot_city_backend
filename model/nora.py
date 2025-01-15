from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class Nora(db.Model):
    __tablename__ = 'Nora'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _message = db.Column(db.String(255), nullable=False)
    _user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    _name = db.Column(db.String(100), nullable=False)
    _age = db.Column(db.Integer, nullable=False)
    _birthday = db.Column(db.Date, nullable=False)

    def __init__(self, message, user_id, name, age, birthday):
        self._message = message
        self._user_id = user_id
        self._name = name
        self._age = age
        self._birthday = birthday

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
            'name': self._name,
            'age': self._age,
            'birthday': str(self._birthday),
        }

    @staticmethod
    def initNoras():
        """
        Initialize the Nora table with sample data.
        """
        sample_messages = [
            {"message": "Welcome, Jane Doe!", "user_id": 1, "name": "Jane Doe", "age": 28, "birthday": "1995-03-14"},
            {"message": "Hello, John Doe!", "user_id": 2, "name": "John Doe", "age": 32, "birthday": "1991-07-21"},
            {"message": "Greetings, Alice Smith!", "user_id": 3, "name": "Alice Smith", "age": 25, "birthday": "1998-09-10"},
            {"message": "Hi, Bob Johnson!", "user_id": 4, "name": "Bob Johnson", "age": 35, "birthday": "1988-12-05"}
        ]

        for sample in sample_messages:
            try:
                nora = Nora(
                    message=sample["message"],
                    user_id=sample["user_id"],
                    name=sample["name"],
                    age=sample["age"],
                    birthday=sample["birthday"]
                )
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
                nora = Nora(
                    message=entry['message'],
                    user_id=entry['user_id'],
                    name=entry['name'],
                    age=entry['age'],
                    birthday=entry['birthday']
                )
                db.session.add(nora)
            except IntegrityError:
                db.session.rollback()
        db.session.commit()
