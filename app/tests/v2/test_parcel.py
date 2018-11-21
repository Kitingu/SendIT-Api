from .basetest import BaseTest
import json


class TestUser(BaseTest):
    def test_user_registration(self):
        """test that user can register"""
        resp = self.client.post("/api/v2/users", data=json.dumps(self.test_user),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        self.assertIn("User registered successfully", str(resp.data))