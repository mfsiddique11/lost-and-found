# from datetime import datetime


# #User model
# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   email = db.Column(db.String(120), unique=True, nullable=False)
#   password = db.Column(db.String(60),nullable=False)
#   posts=db.relationship('Post',backref='poster',lazy=True)
#   def __init__(self, email, password):
#     self.email = email
#     self.password=password

# #Post model

# class Post(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   category = db.Column(db.String(100),nullable=False)
#   itemName = db.Column(db.String(100),nullable=False)
#   location = db.Column(db.String(100),nullable=False)
#   description = db.Column(db.Text,nullable=False)
#   date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
#   pic=db.Column(db.String(100),nullable=False)
#   user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

#   def __init__(self, category, itemName,location,description,date,pic):
#     self.category = category
#     self.itemName=itemName
#     self.location=location
#     self.description=description
#     self.date=date
#     self.pic=pic







from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='poster', lazy='dynamic')
  
    def get_reset_token(self,expires_sec=1800):
            s=Serializer(app.config['SECRET_KEY'],expires_sec)
            return s.dump({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
            s=Serializer(app.config['SECRET_KEY'])
            try:
                    user_id=s.loads(token)['user_id']
            except:
                    return None
            return User.query.get(user_id)        
   
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    itemName = db.Column(db.String(100),nullable=False)
    location = db.Column(db.String(100),nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    pic=db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.description)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    posts = db.relationship('Post', backref='postcategory', lazy='dynamic')


    def __repr__(self):
        return '<Post {}>'.format(self.name)        