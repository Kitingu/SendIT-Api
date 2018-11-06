import unittest
from app import create_app
from app.api.v1.models.orders_model import OrdersModel

db = OrdersModel


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

        self.invalid_order = {"parcel_id": "",
                              "weight": "",
                              "pick_up_location": 123,
                              "destination": "",
                              "price": 500}
        self.update_order = {"destination": "mathare"}
        self.invalid_update = {"destination": 1234225}

    def tearDown(self):
        pass
