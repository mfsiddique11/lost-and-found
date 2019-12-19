from app import db, create_app
from flask_testing import TestCase

from app import app, db


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app
