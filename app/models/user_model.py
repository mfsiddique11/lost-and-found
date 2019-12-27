from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, default=None)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    profile = db.relationship('Profile', backref='user_profile', cascade="all, delete-orphan", uselist=False)
    posts = db.relationship('Post', backref='poster', cascade="all, delete-orphan", lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_confirmed": True if self.confirmed_at else False,
            "is_admin": self.is_admin
        }

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(password, self.password)

    def change_password(self, password):
        self.hash_password(password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed_at = datetime.utcnow()
        db.session.add(self)
        return True


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), db.Enum("admin", "member"), unique=True, nullable=False)

    users = db.relationship('User', backref='user_role', cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    address = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(64), index=True)

    pictures = db.relationship('Picture', backref='user_pic', cascade="all, delete-orphan", lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, first_name, last_name, address, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "phone": self.phone
        }
