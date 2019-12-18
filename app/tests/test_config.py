def test_testing_config(app):
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db.sqlite'




