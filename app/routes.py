from flask import request,jsonify
from app import app,db,bcrypt
from app.models import User,Post
from flask_login import login_user,logout_user,current_user,login_required

# Create a User
@app.route('/register', methods=['POST'])
def add_user():
        if current_user.is_authenticated:
                return 'user already logged in'
                
        if User.query.filter_by(email=request.json['email']).first()==None:
                password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
                
                new_user = User(email=request.json['email'], password=password)

                db.session.add(new_user)
                db.session.commit()
                return 'user created'
        else:
                return 'user already exists'

@app.route('/login',methods=['POST'])
def login():
        if current_user.is_authenticated:
                return 'user already logged in'
        user=User.query.filter_by(email=request.json['email']).first()
        if user and bcrypt.check_password_hash(user.password,request.json['password']):
                login_user(user)
                return 'loged in'
        else:
                return 'wrong email or pass'   

@app.route('/logout')
def logout(): 
        logout_user() 
        return 'user logged out'            


@app.route('/account')
@login_required
def account(): 
        return 'account'



@app.route('/post/create', methods=['POST'])
@login_required 
def add_post():
        description=request.json['description']
        new_post=Post(description=description,poster=current_user)
        db.session.add(new_post)
        db.session.commit()

        return 'post created'

@app.route('/post/<int:post_id>')
@login_required 
def get_post(post_id):
        post=Post.query.get_or_404(post_id)
        return post.description

@app.route('/home')
@login_required 
def get_posts():
        post=current_user.posts.all()
        print (post)
        return "success"       


@app.route('/post/<int:post_id>/update',methods=['POST'])
@login_required 
def update_post(post_id):
        post=Post.query.get_or_404(post_id)
        if post.poster==current_user:
                post.description=request.json['description']
                db.session.commit()
                return post.description
        else:
                abort(403)        
        

@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required 
def delete_post(post_id):
        post=Post.query.get_or_404(post_id)
        if post.poster==current_user:
                
                db.session.delete(post)
                db.session.commit()
                return "deleted" 
        else:
                abort(403)
             