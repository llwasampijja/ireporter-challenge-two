import unittest
from flask import json, Response
from app import create_app

class TestErroHandlersView(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_bad_request_error(self):
        login_reponse = self.client.post("api/v1/auth/users/login", data="It's supposed to be json format", content_type="application/json")
        response_data = json.loads(login_reponse.data.decode())
        self.assertEqual(login_reponse.status_code, 400)
        self.assertEqual(response_data.get("message"), "Bad request, check your input and try again")

    def test_page_not_found(self):
        response = self.client.get("url/not/exist", content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("message"), "No such page on this site")

    def test_method_not_allowed(self):
        response = self.client.patch("api/v1/auth/users/register", data=json.dumps({
            "username":"username",
            "password":"password"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response_data.get("message"), "method not allowed")