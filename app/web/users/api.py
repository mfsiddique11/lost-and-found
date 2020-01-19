from datetime import datetime

from flask import request, jsonify, session, Blueprint, url_for
from flask_login import login_user, logout_user, current_user, login_required

from app import db, bcrypt
from app.models.user_model import User, Role

from app.web.users.schemas import *
from app.common.decorators.validate_json import validate_json

users = Blueprint('users', '__name__')


@users.route('/user/register', methods=['POST'])
@validate_json(add_user_schema)
def register():
    from app.common.email import sendmail

    if current_user.is_authenticated:
        if not current_user.confirmed_at:
            token = current_user.generate_confirmation_token()
            url = url_for('users.confirm_email', token=token)
            sendmail.delay(url, request.json['email'])

            return jsonify({"Action": 'verification email sent'}), 200
        return jsonify({"Error": 'already loggedIn'}), 404

    user = User.query.filter_by(email=request.json['email']).first()
    if user is not None:
        if not user.confirmed_at:
            login_user(user)
            token = user.generate_confirmation_token()
            url = url_for('users.confirm_email', token=token)
            sendmail.delay(url, request.json['email'])

            return jsonify({"Action": 'verification email sent'}), 200

        return jsonify({"Error": 'already registered'}), 409

    if User.query.filter_by(username=request.json['username']).first() is not None:
        return jsonify({"Error": 'username already exists'}), 409

    if request.json['password'] != request.json['confirm_password']:
        return jsonify({"Error": 'password doesnt match'})

    role = db.session.query(Role).filter_by(name='member').first()

    user = User(username=request.json['username'],
                email=request.json['email'],
                password=request.json['password'])
    role.users.append(user)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    token = user.generate_confirmation_token()
    url = url_for('users.confirm_email', token=token)
    sendmail.delay(url, request.json['email'])

    resp = jsonify(user.to_json())
    resp.status_code = 201
    return resp


@users.route("/user/confirm-email/<token>")
@login_required
def confirm_email(token):

    if current_user.confirmed_at:
        return jsonify({"Error": 'Email already verified'}), 400

    if not current_user.confirm(token):
        return jsonify({"Error": 'Wrong token'}), 400

    db.session.commit()
    return jsonify({"Action": 'Email confirmed'}), 201


@users.route('/user/login', methods=['POST'])
@validate_json(login_user_schema)
def login():
    from app.common.email import sendmail

    if current_user.is_authenticated:
        return jsonify({"Error": 'already loggedIn'}), 404

    user = User.query.filter_by(email=request.json['email']).first()

    if not user and user.verify_password(request.json['password']):
        return jsonify({"Error": 'Wrong email or password'}, user.email, user.password), 401

    if not user.confirmed_at:
        login_user(user)
        sendmail.delay(user.id, user.email)
        return jsonify({"Action": 'verification email sent'}), 200

    login_user(user)
    return jsonify({"Action": 'loggedIn'}), 200


@users.route('/user/<user_id>/change-password', methods=['POST'])
@validate_json(change_password_schema)
@login_required
def change_password(user_id):
    if not current_user.is_authenticated:
        return jsonify({"Error": 'Not loggedIn'}), 404

    if not User.query.get(user_id).confirm_at:
        return jsonify({"Error": 'Email is not verified'}), 400

    user = User.query.get(user_id)

    if user and user.verify_password(request.json['old_password']):
        return jsonify({"Error": 'old password is wrong'}), 400

    if request.json['new_password'] != request.json['confirm_password']:
        return jsonify({"Error": 'password doesnt match'})

    user.change_password(request.json['new_password'])
    db.session.commit()
    return jsonify({"Action": 'password changed'}, user.to_json()), 201


@users.route('/user/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"Action": 'Logged Out'}), 200


@users.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify({"Action": 'user deleted'}), 204
