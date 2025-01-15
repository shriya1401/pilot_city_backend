from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, content, user_id):
        """
        Constructor for the Notification class.
        
        Args:
            content (str): The content of the notification.
            user_id (int): The ID of the user associated with the notification.
        """
        self.content = content
        self.user_id = user_id

    def create(self):
        """
        Adds the notification to the database and commits the transaction.
        
        Raises:
            Exception: If there is an error during the database transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieves the notification data as a dictionary.
        
        Returns:
            dict: A dictionary containing the notification data.
        """
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at
        }

    @staticmethod
    def init_notifications():
        """
        Initializes sample notifications for the first user in the database.
        """
        user = User.query.first()
        if user:
            sample_notification = Notification(content='Welcome to our platform!', user_id=user.id)
            try:
                sample_notification.create()
                print("Sample notification created successfully.")
            except Exception as e:
                print(f"Error creating sample notification: {e}")
        else:
            print("No user found to create sample notifications.")
