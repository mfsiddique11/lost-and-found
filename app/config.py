class Config:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:yes@db:3306/lostandfound'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '8be8c10171ba90cd276afbaa99288ffa'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'donotreplytesting121@gmail.com'
    MAIL_PASSWORD = '!qa2ws3ed4rf'


class TestingConfig:
    LOGIN_DISABLED = False,
    TESTING = True,  # Propagate exceptions
    MAIL_SUPPRESS_SEND = True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '8be8c10171ba90cd276afbaa99288ffa'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'donotreplytesting121@gmail.com'
    MAIL_PASSWORD = '!qa2ws3ed4rf'
