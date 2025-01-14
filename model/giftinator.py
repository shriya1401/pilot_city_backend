from sqlite3 import IntegrityError
from __init__ import db
from model.user import User  # Assuming User is needed for valid user references


class Giftinator(db.Model):
    __tablename__ = 'giftinator'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _yesNo = db.Column(db.String(255), nullable=False)
    _user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
   
    def __init__(self, yesNo, user_id):
        self._yesNo = yesNo
        self._user_id = user_id


    @property
    def yesNo(self):
        return self._yesNo


    @yesNo.setter
    def yesNo(self, value):
        self._yesNo = value


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
            'yesNo': self._yesNo,
            'user_id': self._user_id,
        }


def initGiftinator():
    """Initialize sample data for the Giftinator table."""
    user = User.query.first()  # Assuming at least one user exists
    if user:
        sample_gift = Giftinator(yesNo="Yes", user_id=user.id)
        try:
            sample_gift.create()
            print("Giftinator sample data initialized.")
        except Exception as e:
            print(f"Error initializing Giftinator data: {e}")
    else:
        print("No users found. Please create a user before initializing Giftinator.")



