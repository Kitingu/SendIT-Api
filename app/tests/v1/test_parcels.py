from .basetest import BaseTest
import json


class TestCreateOrder(BaseTest):
    ################# test create parcel orders ###############
    def test_create_order(self):
        """test that user can create a parcel delivery order """
        register = self.client.post('/api/v1/users', data=json.dumps(self.test_user),
                                    content_type='application/json')
        self.assertEqual(register.status_code, 201)

        resp = self.client.post('/api/v1/parcels', data=json.dumps(self.test_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_create_order_with_invalid_details(self):
        """ test that user cant create an order with invalid details"""
        register = self.client.post('/api/v1/users', data=json.dumps(self.test_user),
                                    content_type='application/json')
        self.assertEqual(register.status_code, 201)
        resp = self.client.post('/api/v1/parcels', data=json.dumps(self.invalid_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)


    def test_get_all_orders(self):
        response = self.client.get('/api/v1/parcels')
        self.assertEqual(response.status_code, 200)

    def test_get_parcel_by_id(self):
        register = self.client.post('/api/v1/users', data=json.dumps(self.test_user),
                                    content_type='application/json')
        self.assertEqual(register.status_code, 201)
        resp = self.client.post('/api/v1/parcels', data=json.dumps(self.test_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = self.client.get('/api/v1/parcels/1')
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_parcel(self):
        response = self.client.get('/api/v1/parcels/500')
        self.assertEqual(response.status_code, 404)

    def test_get_non_integer(self):
        response = self.client.get('/api/v1/parcels/kasee')
        self.assertEqual(response.status_code, 404)

    ###################### test update parcels ############################

    def test_update_parcel(self):
        """test that user can update the destination of a parcel delivery order """
        register = self.client.post('/api/v1/users', data=json.dumps(self.test_user),
                                    content_type='application/json')
        self.assertEqual(register.status_code, 201)
        resp = self.client.post('/api/v1/parcels/', data=json.dumps(self.test_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = self.client.put('/api/v1/parcels/1/destination', data=json.dumps(self.update_order),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_cancel_order(self):
        """test that user can cancel a  parcel delivery order """
        register = self.client.post('/api/v1/users', data=json.dumps(self.test_user),
                                    content_type='application/json')
        self.assertEqual(register.status_code, 201)
        resp = self.client.post('/api/v1/parcels/', data=json.dumps(self.test_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = self.client.put('/api/v1/parcels/1/cancel')
        self.assertEqual(response.status_code, 200)

    def test_update_destination_with_invalid_details(self):
        register = self.client.post('/api/v1/users', data=json.dumps(self.test_user),
                                    content_type='application/json')
        self.assertEqual(register.status_code, 201)
        resp = self.client.post('/api/v1/parcels/', data=json.dumps(self.test_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = self.client.put('/api/v1/parcels/1/destination', data=json.dumps(self.invalid_update),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_cancel_non_existing_order(self):
        register = self.client.post('/api/v1/users', data=json.dumps(self.test_user),
                                    content_type='application/json')
        self.assertEqual(register.status_code, 201)
        resp = self.client.post('/api/v1/parcels/', data=json.dumps(self.test_order),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        response = self.client.put('/api/v1/parcels/500/cancel')
        self.assertEqual(response.status_code, 404)
