from .basetest import BaseTest
import json


class TestUser(BaseTest):
    def test_user_registration(self):
        """test that user can register"""
        resp = self.client.post("/api/v2/users", data=json.dumps(self.test_user),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        self.assertIn("User registered successfully", str(resp.data))

    def test_register_with_whitespaces(self):
        """test that username cannot contain whitespaces"""
        resp = self.client.post("/api/v1/users", data=json.dumps(self.invalid_user),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("fields cannot be blank", str(resp.data))

    def test_double_registration(self):
        """test that user can't be registered twice"""
        resp = self.client.post("/api/v1/users", data=json.dumps(self.test_user),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = self.client.post("/api/v1/users", data=json.dumps(self.test_user),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 409)
        self.assertIn("already exists", str(resp.data))
