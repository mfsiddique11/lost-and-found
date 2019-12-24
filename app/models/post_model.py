from datetime import datetime
from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    pictures = db.relationship('Picture', backref='post_pic', cascade="all, delete-orphan", lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, description, title, location):
        self.description = description
        self.title = title
        self.location = location

    def to_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "title": self.title,
            "location": self.location
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), db.Enum("lost", "found"), unique=True, nullable=False)

    posts = db.relationship('Post', backref='post_category', cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, name):
        self.name = name
