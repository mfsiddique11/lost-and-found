class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:yes@db:3306/lostandfound'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Host = '0.0.0.0'
    PORT = 5000
    CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
    CELERY_RESULT_BACKEND = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'

    SECRET_KEY = '8be8c10171ba90cd276afbaa99288ffa'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'donotreplytesting121@gmail.com'
    MAIL_PASSWORD = '!qa2ws3ed4rf'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    # LOGIN_DISABLED = False
    TESTING = True
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
