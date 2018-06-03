from flask_testing import TestCase
from app import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
