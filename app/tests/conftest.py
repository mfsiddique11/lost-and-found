import pytest
from flask_login import LoginManager

from app import create_app, db



@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    app_context = app.test_request_context()
    app_context.push()
    app.config.from_object('app.config.TestingConfig')
    with app.app_context():
        # alternative pattern to app.app_context().push()
        # all commands indented under 'with' are run in the app context
        db.create_all()
        yield app
        db.drop_all()
