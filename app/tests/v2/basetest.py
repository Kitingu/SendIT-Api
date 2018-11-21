import unittest
import json
from manage import db
from app import create_app
from instance.config import app_config


class BaseTest(unittest.TestCase):
    """ this is a class that initialises test data for all the test"""

    def setUp(self):
        self.app = create_app(app_config["testing"])
        self.client = self.app.test_client()
        self.test_user = {
            "email": "asdf@gmail.com",
            "username": "ben",
            "password": "@Ha1_pass",
            "confirm_password": "@Ha1_pass"
        }

        self.invalid_user = {
            "email": "@gmail.com",
            "username": "",
            "password": "@Ha1_pass",
            "confirm_password": "@Ha1_pass"
        }
        self.wrong_pass = {
            "email": "asdf@gmail.com",
            "username": "asdfg",
            "password": "@Ha1_pass",
            "confirm_password": "test_pass"
        }
        self.login = {
            "email": "asdf@gmail.com",
            "password": "@Ha1_pass",
        }

        self.login1 = {
            "email": "as@gmail.com",
            "password": "@Ha1_pass",
        }

        self.invalid_login = {
            "email": "@gmail.com",
            "password": "",
        }
        self.update_order = {"destination": "mathare"}
        self.invalid_update = {"destination": ""}
        self.cancel_order = {"status": "cancel"}
        self.invalid_cancel_status = {"ghvdshgcs": ""}

    def tearDown(self):
        db.drop_tables()


if __name__ == "__main__":
    unittest.main(verbosity=2)
