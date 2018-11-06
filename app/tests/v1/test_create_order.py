from .basetest import BaseTest
import json


class TestCreateOrder(BaseTest):

    def test_create_order(self):
        """test that user can create a parcel delivery order """
        resp = self.client.post('/api/v1/parcels/', data=json.dumps(self.test_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_create_order_with_invalid_details(self):
        """ test that user cant create an order with invalid details"""
        resp = self.client.post('/api/v1/parcels/', data=json.dumps(self.invalid_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

