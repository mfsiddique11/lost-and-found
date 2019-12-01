# from datetime import datetime
# from app import db,app
# from app.users.models import User
# from app.categories.models import Category

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(140))
#     itemName = db.Column(db.String(100),nullable=False)
#     location = db.Column(db.String(100),nullable=False)
#     created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     pic=db.Column(db.String(100),nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.itemName,self.description)

