from datetime import datetime
from app import db,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    confirmed_on = db.Column(db.DateTime, index=True)
    confirm_id=db.Column(db.Boolean,unique=False,default=False)
    posts = db.relationship('Post', backref='poster', lazy='dynamic')        
   
    def __repr__(self):
        return '<User {}>'.format(self.email,self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    itemName = db.Column(db.String(100),nullable=False)
    location = db.Column(db.String(100),nullable=False)
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    pic=db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.itemName,self.description)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    posts = db.relationship('Post', backref='postcategory', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.name)        