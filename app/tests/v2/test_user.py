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
        resp = self.client.post('/api/v2/users', data=json.dumps(self.invalid_user),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn("fields cannot be blank", str(resp.data))

    def test_double_registration(self):
        """test that user can't be registered twice"""
        resp = self.client.post('/api/v2/users', data=json.dumps(self.test_user),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        resp = self.client.post('/api/v2/users', data=json.dumps(self.test_user),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 409)
        self.assertIn("already exists", str(resp.data))

    def test_passwords_do_not_match(self):
        """Test if user passwords match or not"""
        resp = self.client.post('/api/v2/users', data=json.dumps(self.wrong_pass),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 401)
        self.assertIn("passwords do not match", str(resp.data))

    def test_login_non_registered(self):
        """Test user can't login unless they are registered"""
        resp = self.client.post('/api/v2/users/login', data=json.dumps(self.login1),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn("user does not exist", str(resp.data))

    def test_login_with_invalid_details(self):
        """Test user cannot be logged in with invalid details"""
        resp = self.client.post('/api/v2/users/login', data=json.dumps(self.invalid_login),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn("please enter a valid email", str(resp.data))

    def test_user_login(self):
        """Test that user can be logged in successfully"""
        self.client.post('/api/v2/users', data=json.dumps(self.test_user),
                         content_type='application/json')
        resp = self.client.post('/api/v2/users/login', data=json.dumps(self.login),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", str(resp.data))
