import secrets
from datetime import datetime

from flask import request, jsonify, session, Blueprint, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

from app import db, bcrypt, mail, celery
from app.models.user_model import User

from app.web.users.schemas import *
from app.common.decorators.validate_json import validate_json

users = Blueprint('users', '__name__')


@users.route('/user/register', methods=['POST'])
@validate_json(add_user_schema)
def register():
    if current_user.is_authenticated:
        return jsonify({"Error": 'already loggedIn'}), 404

    if User.query.filter_by(email=request.json['email']).first() is not None:
        return jsonify({"Error": 'email already exists'}), 409

    if User.query.filter_by(username=request.json['username']).first() is not None:
        return jsonify({"Error": 'username already exists'}), 409

    if request.json['password'] != request.json['confirm_password']:
        return jsonify({"Error": 'password doesnt match'})

    hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    new_user = User(username=request.json['username'],
                    email=request.json['email'],
                    password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    resp = sendmail(current_user.id, request.json['email'])
    return jsonify(current_user.id), 201


@users.route("/user/confirm-email/<token>")
@login_required
def confirm_email(token):
    user = User.query.get(current_user.id)

    if user.confirm_id:
        return jsonify({"Error": 'Email already verified'}), 400

    if session['token' + str(current_user.id)] != token:
        return jsonify({"Error": 'Wrong token'}), 400

    user.confirm_id = True
    user.confirmed_on = datetime.now()
    session.pop('token' + str(current_user.id))
    db.session.commit()
    return jsonify({"Action": 'Email confirmed'}), 201


@users.route('/user/login', methods=['POST'])
@validate_json(login_user_schema)
def login():
    if current_user.is_authenticated:
        return jsonify({"Error": 'already loggedIn'}), 404

    user = User.query.filter_by(email=request.json['email']).first()
    print(user.password)
    if not user and bcrypt.check_password_hash(user.password, request.json['password']):
        return jsonify({"Error": 'Wrong email or password'}, user.email, user.password), 401

    if not user.confirm_id:
        login_user(user)
        sendmail(user.id, user.email)
        return jsonify({"Action": 'verification email sent'}), 200

    login_user(user)
    return jsonify({"Action": 'loggedIn'}), 200


@users.route('/user/change-password', methods=['POST'])
@validate_json(change_password_schema)
# @login_required
def change_password():
    if not current_user.is_authenticated:
        return jsonify({"Error": 'Not loggedIn'}), 404

    if not User.query.get(current_user.id).confirm_id:
        return jsonify({"Error": 'Email is not verified'}), 400

    user = User.query.get(current_user.id)

    if user and bcrypt.check_password_hash(user.password, request.json['old_password']):
        return jsonify({"Error": 'old password is wrong'}), 400

    if request.json['new_password'] != request.json['confirm_password']:
        return jsonify({"Error": 'password doesnt match'})

    hashed_password = bcrypt.generate_password_hash(request.json['new_password']).decode('utf-8')
    user.password = hashed_password
    db.session.commit()
    return jsonify({"Action": 'password changed'}), 201


@users.route('/user/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"Action": 'Logged Out'}), 200


@users.route('/user', methods=['DELETE'])
def delete_user():
    user = User.query.all()
    for u in user:
        db.session.delete(u)
        db.session.commit()
    return jsonify({"Action": 'del hogae'}), 200


@celery.task
def sendmail(uid, recipient):
    session['token' + str(uid)] = secrets.token_hex(8)
    msg = Message('Email verification request',
                  sender='donotreplytesting121@gmail.com',
                  recipients=[recipient])
    msg.body = url_for("users.confirm_email", token=session['token' + str(uid)], _external=True)
    mail.send(msg)
    return 'verification email has been sent'
