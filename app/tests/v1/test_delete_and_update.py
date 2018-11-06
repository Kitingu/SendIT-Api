from .basetest import BaseTest
import json


class TestUpdateAndDelete(BaseTest):

    def test_update_parcel(self):
        """test that user can update the destination of a parcel delivery order """
        resp = self.client.post('/api/v1/parcels', data=json.dumps(self.test_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = self.client.put('/api/v1/parcels/1', data=json.dumbs(self.update_order),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        """ test that user cant create an order with invalid details"""
        resp = self.client.post('/api/v1/parcels', data=json.dumps(self.invalid_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = self.client.delete('/api/v1/parcels/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existing(self):
        response = self.client.delete('/api/v1/parcels/100')
        self.assertEqual(response.status_code, 404)

    def test_update_parcel(self):
        """test that user cannot delete non existing parcel delivery order """
        response = self.client.put('/api/v1/parcels/100', data=json.dumbs(self.update_order),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_with_invalid_details(self):
        resp = self.client.post('/api/v1/parcels', data=json.dumps(self.test_order),
                               content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = self.client.put('/api/v1/parcels/1', data=json.dumbs(self.invalid_update),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
