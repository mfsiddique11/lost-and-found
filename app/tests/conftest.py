import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('app.config.TestingConfig')
    app.testing = True

    with app.app_context():
        # alternative pattern to app.app_context().push()
        # all commands indented under 'with' are run in the app context
        db.create_all()
        yield app  # Note that we changed return for yield, see below for why
        # db.session.remove()
        # db.drop_all()
        return app
