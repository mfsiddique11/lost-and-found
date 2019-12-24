from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from app.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)


    with app.app_context():
        db.init_app(app)
        db.app = app
        login_manager.init_app(app)
        mail.init_app(app)
        bcrypt.init_app(app)

        from app.web.users.api import users
        from app.web.posts.api import posts
        from app.web.categories.api import categories

        app.register_blueprint(users)
        app.register_blueprint(posts)
        app.register_blueprint(categories)

    return app


