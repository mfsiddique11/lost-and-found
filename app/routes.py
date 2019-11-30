import os
import secrets
from flask import request,jsonify,session
from app import app,db,bcrypt, mail
from app.models import User,Post,Category
from flask_login import login_user,logout_user,current_user,login_required
from flask_mail import Message
import json


@app.route("/emailverification/<code>")
@login_required
def emailVerification(code):
        if session['key'+str(current_user.id)]==code:
                session.pop['key'+str(current_user.id)]
                return 'email verified'
                
        else:
                return 'token expired'

@app.route('/register', methods=['POST'])
def add_user():
        if current_user.is_authenticated:
                 session['key'+str(current_user.id)] = secrets.token_hex(8)
                 msg=Message('Email verification request',sender='donotreplytesting121@gmail.com',recipients=['mfsiddique11@gmail.com'])
                 msg.body=session['key'+str(current_user.id)]
                 print(session['key'+str(current_user.id)])
                 mail.send(msg)
                
                 return 'user already logged in'
                
        if User.query.filter_by(email=request.json['email']).first()==None:
                if request.json['password']==request.json['confirmpassword']:
                        session['key'+str(current_user.id)] = secrets.token_hex(8)
                        msg=Message('Email verification request',sender='donotreplytesting121@gmail.com',recipients=['mfsiddique11@gmail.com'])
                        msg.body=session['key'+str(current_user.id)]
                        mail.send(msg)

                        hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
                        
                        new_user = User(email=request.json['email'], password=hashed_password)

                        db.session.add(new_user)
                        db.session.commit()
                        login_user(new_user)
                        return 'user created'
                else:
                        return 'password donot match'        
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
        if current_user.is_authenticated:
                logout_user() 
                return 'user logged out'  
        else:
                return 'please login'                  


@app.route('/change_password', methods=['POST'])
@login_required
def change_password(): 
        if current_user.is_authenticated:
                user=User.query.get(current_user.id)
                if user and bcrypt.check_password_hash(user.password,request.json['oldpassword']):
                        if request.json['newpassword']==request.json['confirmpassword']:
                                hashed_password = bcrypt.generate_password_hash(request.json['newpassword']).decode('utf-8')
                                user.password=hashed_password
                                db.session.commit()
                                return 'password changed successfully'
                        else:
                                return 'passwords do not match'
        else:
                return 'please login first'


@app.route('/category/add',methods=['POST'])
def add_category():
        name=request.json['name']
        category=Category.query.filter_by(name=name).first()
        if category:
                return 'category already exists'
        else:
                new_category=Category(name=name)
                db.session.add(new_category)
                db.session.commit()
                return 'added category successfully'

@app.route('/category/show',methods=['POST'])
def show_category():
        print(Category.query.all())
        return 'success'

@app.route('/category/<int:category_id>',methods=['POST'])
def get_category(category_id):
        category=Category.query.get_or_404(category_id)
        return category.name

@app.route('/category/<int:category_id>/update',methods=['POST'])
def update_category(category_id):
        category=Category.query.get_or_404(category_id)
        category.name=request.json['name']
        db.session.commit()
        return 'updated succesfuly'

@app.route('/category/<int:category_id>/delete',methods=['POST'])
def delete_category(category_id):
        category=Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return "deleted" 


                   
# def save_picture(pic):
#         random_hex=secrets.token_hex(8)
#         _,f_ext=os.path.splitext(pic.filename)
#         picture_fn=random_hex+f_ext
#         picture_path=os.path.join(app.root_path,'pictures',picture_fn)
#         pic.save(picture_path)
#         return picture_fn


@app.route('/post/create', methods=['POST'])
@login_required 
def add_post():
        # description=request.form['value'].description
        # print (description)
        # picture_file=save_picture(request.files['image'])
        if Category.query.all() == []:
                return 'please add categories first'
        else:
                description=request.json['description']
                pic=request.json['pic']
                itemName=request.json['itemName']
                location=request.json['location']
                category=Category.query.get(int(request.json['category']))

                new_post=Post(itemName=itemName,location=location,description=description,pic=pic,poster=current_user,postcategory=category)

                db.session.add(new_post)
                db.session.commit()

                return 'post created'

@app.route('/post/<int:post_id>')
@login_required 
def get_post(post_id):
        post=Post.query.get_or_404(post_id)
        print(post.postcategory.name)
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
             
@app.route('/post/search',methods=['GET'])
@login_required 
def search_post():
        if 'itemname' in request.args and 'location' in request.args:
                posts=Post.query.filter_by(itemName=request.args.get('itemname'),location=request.args.get('location')).all()
                print(posts)
                return 'success'
        elif 'itemname' in request.args: 
                posts=Post.query.filter_by(itemName=request.args.get('itemname')).all()
                print(posts)
                return 'success' 
        elif 'location' in request.args:
                posts=Post.query.filter_by(location=request.args.get('location')).all()
                print(posts)
                return 'success'      
        else:
                return 'add query to the search'
                