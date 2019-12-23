from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config, TestingConfig

app = Flask(__name__)
# app.testing=True
# app.login_disabled=True
app.config.from_object(Config)

mail = Mail(app)

app.config['CELERY_BROKER_URL'] = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'

celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

db = SQLAlchemy(app)
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

# login_manager.login_view = return jsonify({"Error": "LogIn is required"}), 403


from app.web.users.api import users
from app.web.posts.api import posts
from app.web.categories.api import categories

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(categories)


def create_app():
    app = Flask(__name__)
    app.testing = True
    app.config['TESTING'] = True
    app.config.from_object(TestingConfig)

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
