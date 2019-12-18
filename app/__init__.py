from flask import Flask, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.config['TESTING'] = True

db = SQLAlchemy(app)
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

# login_manager.login_view = return jsonify({"Error": "LogIn is required"}), 403

mail = Mail(app)

from app.users.api import users
from app.posts.api import posts
from app.categories.api import categories

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(categories)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db = SQLAlchemy(app)

    db.init_app(app)

    login_manager = LoginManager(app)

    # login_manager.login_view = return jsonify({"Error": "LogIn is required"}), 403

    mail = Mail(app)

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(categories)

    # @app.route('/ping', methods=['GET'])
    # def ping_pong():
    #     return jsonify({
    #         'status': 'Epic success',
    #         'message': 'pong!'
    #     })
    return app
