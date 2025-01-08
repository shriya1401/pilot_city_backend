from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from model.post import Post
from __init__ import db

class ranking(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    post = relationship("Post", back_populates="ratings")

    def __init__(self, stars, user_id, post_id):
        self.stars = stars
        self.user_id = user_id
        self.post_id = post_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        
    def read(self):
        return {
            "id": self.id,
            "stars": self.stars,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "timestamp": self.timestamp.isoformat()
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()