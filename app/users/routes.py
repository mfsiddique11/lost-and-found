from flask import request,jsonify,session,Blueprint
from app import app,db,bcrypt, mail
from app.models import User
from flask_login import login_user,logout_user,current_user,login_required
from flask_mail import Message
from datetime import datetime
import os
import secrets

users=Blueprint('users','__name__')

@users.route('/loginnotify')
def login_notify():
        return 'please login first'

@users.route('/register', methods=['POST'])
def add_user():
        if current_user.is_authenticated:
                 return 'user is already logged in'
                
        if User.query.filter_by(email=request.json['email']).first()==None:
                if User.query.filter_by(username=request.json['username']).first()==None:    
                        if request.json['password']==request.json['confirmpassword']:
                                hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
                                new_user = User(username=request.json['username'],
                                           email=request.json['email'], password=hashed_password)

                                db.session.add(new_user)
                                db.session.commit()
                                login_user(new_user)
                                session['key'+str(current_user.id)] = secrets.token_hex(8)
                                msg=Message('Email verification request',sender='donotreplytesting121@gmail.com',recipients=['mfsiddique11@gmail.com'])
                                msg.body=session['key'+str(current_user.id)]
                                mail.send(msg)
                                return 'user created and logedIn, verification email has been sent'
                        else:
                                return 'password donot match' 
                else:
                        return 'username already exists'                       
        else:

                return 'email already exists'



@users.route("/emailverification/<code>")
@login_required
def emailVerification(code):
        user=User.query.get(current_user.id)
        if user.confirm_id==False:
                if session['key'+str(current_user.id)]==code:
                        user=User.query.get(current_user.id)
                        user.confirm_id=True
                        user.confirmed_on=datetime.now()
                        session.pop('key'+str(current_user.id))
                        db.session.commit()
                        return 'email verified'
                        
                else:
                        return 'wrong code'
        else:
                return 'email already verified'


@users.route('/login',methods=['POST'])
def login():
        if current_user.is_authenticated:
                return 'user already logged in'
        user=User.query.filter_by(email=request.json['email']).first()
        
        if user and bcrypt.check_password_hash(user.password,request.json['password']):
                if user.confirm_id==False:
                        session['key'+str(current_user.id)] = secrets.token_hex(8)
                        msg=Message('Email verification request',sender='donotreplytesting121@gmail.com',recipients=['mfsiddique11@gmail.com'])
                        msg.body=session['key'+str(current_user.id)]
                        mail.send(msg)
                        login_user(user)
                        return 'a confirmation email has been sent.verify your email first'
                else:
                        login_user(user)
                        return 'logged In'
                        
        else:
                return 'wrong email or pass'   

@users.route('/logout')
@login_required
def logout(): 
        logout_user() 
        return 'user logged out'                  


@users.route('/changepassword', methods=['POST'])
def change_password(): 
        if current_user.is_authenticated:
                if User.query.get(current_user.id).confirm_id==False:
                        return 'confirm your email'
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

