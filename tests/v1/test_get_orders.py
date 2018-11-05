from .basetest import BaseTest
import json


class TestGetOrders(BaseTest):
    def test_get_all_orders(self):
        response = self.client.get('/api/v1/parcels')
        self.assertEqual(response.status_code, 200)

    def test_get_parcel_by_id(self):
        response = self.client.get('/api/v1/parcels/1')
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_parcel(self):
        response = self.client.get('/api/v1/parcels/500')
        self.assertEqual(response.status_code, 404)

    def test_get_non_integer(self):
        response = self.client.get('/api/v1/parcels/kasee')
        self.assertEqual(response.status_code, 400)
