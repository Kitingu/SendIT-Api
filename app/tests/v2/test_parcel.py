from .basetest import BaseTest
import json


class TestParcels(BaseTest):
    def test_create_parcel(self):
        """test that user can register"""
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.test_order),
                                content_type="application/json", headers=self.user_header)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("order submitted successfully", str(resp.data))

        """test missing authorization header"""
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.test_order),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 401)
        self.assertIn("Missing Authorization Header", str(resp.data))

    def test_create_invalid_parcel(self):
        """test that user can't register invalid parcel"""
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.invalid_order),
                                content_type="application/json", headers=self.user_header)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("not a valid input", str(resp.data))

    def test_create_while_not_logged_in(self):
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.test_order),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 401)
        self.assertIn("Missing Authorization Header", str(resp.data))

    def test_change_destination(self):
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.test_order),
                                content_type="application/json", headers=self.user_header)
        self.assertEqual(resp.status_code, 201)
        response = self.client.put('/api/v2/parcels/1/destination', data=json.dumps(self.update_order),
                                   content_type='application/json', headers=self.user_header)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        response = self.client.put('/api/v2/parcels/8/destination', data=json.dumps(self.update_order),
                                   content_type='application/json', headers=self.user_header)
        print(response.data)
        self.assertEqual(response.status_code, 404)

    def test_change_destination_with_invalid_details(self):
        """test that user can't change destination with invalid details"""
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.test_order),
                                content_type="application/json", headers=self.user_header)
        self.assertEqual(resp.status_code, 201)
        response = self.client.put('/api/v2/parcels/1/destination', data=json.dumps(self.invalid_update),
                                   content_type='application/json', headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_cancel_order(self):
        """test that user can cancel an order"""
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.test_order),
                                content_type="application/json", headers=self.user_header)
        self.assertEqual(resp.status_code, 201)
        response = self.client.put("/api/v2/parcels/1/cancel", content_type="application/json",
                                   headers=self.user_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("order cancelled successfully", str(response.data))
        response = self.client.put("/api/v2/parcels/900/cancel", content_type="application/json",
                                   headers=self.user_header)
        self.assertEqual(response.status_code, 404)

    def test_get_all_orders(self):
        resp = self.client.get('/api/v2/parcels', headers=self.user_header)
        self.assertEqual(resp.status_code, 200)

    def test_get_single_order(self):
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.test_order),
                                content_type="application/json", headers=self.user_header)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/api/v2/parcels/1', headers=self.user_header)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/api/v2/parcels/5', headers=self.user_header)
        self.assertEqual(resp.status_code, 404)


    def test_change_location(self):
        resp = self.client.post("/api/v2/parcels", data=json.dumps(self.test_order),
                                content_type="application/json", headers=self.user_header)
        self.assertEqual(resp.status_code, 201)
        response = self.client.put("/api/v2/parcels/1/changelocation", data=json.dumps(self.changelocation),
        content_type="application/json",headers=self.user_header)
        self.assertEqual(response.status_code, 200)
        response = self.client.put("/api/v2/parcels/5/changelocation", data=json.dumps(self.changelocation),
        content_type="application/json",headers=self.user_header)
        self.assertEqual(response.status_code, 404)
