import unittest,json
from app import create_app
from app.api.v1.models.orders_model import OrdersModel
from app.api.v1.models.user_model import UserModel

Order_obj = OrdersModel()
User_obj = UserModel()


class BaseTest(unittest.TestCase):
    """ this is a class that initialises test data for all the test"""


    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.test_order = {
            "sender_name": "ben",
            "receiver_name": "Asael",
            "receiver_contact": "Asael@gmail.com",
            "weight": 10,
            "pickup_location": "Kiambu",
            "destination": "Nairobi"
        }

        self.invalid_order = {
            "sender_name": "ben",
            "parcel_id": "",
            "receiver_contact": "Asael@gmail.com",
            "weight": "",
            "pick_up_location": 123,
            "destination": ""}
        self.test_user = {
            "email": "asdf@gmail.com",
            "username": "ben",
            "password": "test_pass",
            "confirm_password": "test_pass"
        }

        self.invalid_user = {
            "email": "@gmail.com",
            "username": "",
            "password": "test_pass",
            "confirm_password": "test_pass"
        }
        self.wrong_pass = {
            "email": "asdf@gmail.com",
            "username": "bababayao",
            "password": "test_p",
            "confirm_password": "test_pass"
        }

        self.login1 = {
            "email": "as@gmail.com",
            "password": "test_pass",
        }

        self.invalid_login = {
            "email": "@gmail.com",
            "password": "",
        }
        self.update_order = {"destination": "mathare"}
        self.invalid_update = {"destination": ''}
        self.cancel_order = {"status": "cancel"}
        self.invalid_cancel_status = {"ghvdshgcs": ''}




    def tearDown(self):
        Order_obj.db.clear()
        User_obj.db.clear()


if __name__ == '__main__':
    unittest.main(verbosity=2)
