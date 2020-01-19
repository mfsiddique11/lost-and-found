import pytest
from app import create_app, db, TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    app_context = app.test_request_context()
    app_context.push()
    with app.app_context():
        # alternative pattern to app.app_context().push()
        # all commands indented under 'with' are run in the app context
        db.create_all()
        yield app
        db.drop_all()
