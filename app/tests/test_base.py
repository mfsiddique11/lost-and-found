# from app import db, create_app
# from flask_testing import TestCase
#
#
# class BaseTestCase(TestCase):
#     def create_app(self):
#         app = create_app()
#         app.config.from_object('app.config.TestingConfig')
#         app.testing = True
#         return app
#
#     def setUp(self):
#         db.create_all()
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
