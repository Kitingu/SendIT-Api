from .basetest import BaseTest
import json


class TestUser(BaseTest):

    def test_user_registration(self):
        resp = self.client.post('/api/v1/users/', data=json.dumps(self.test_user),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_register_with_whitespaces(self):
        resp = self.client.post('/api/v1/users/', data=json.dumps(self.invalid_user),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_double_registration(self):
        resp = self.client.post('/api/v1/users/', data=json.dumps(self.test_user),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        resp = self.client.post('/api/v1/users/', data=json.dumps(self.test_user),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 409)

    def test_passwords_do_not_match(self):
        resp = self.client.post('/api/v1/users/', data=json.dumps(self.wrong_pass),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 401)
