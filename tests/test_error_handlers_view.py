"""unit tests for error handling"""

import unittest

from flask import json

from app import create_app
from app.utilities.static_strings import (
    URL_LOGIN,
    URL_REGISTER,
    URL_BASE,

    WELCOME_MSG,

    RESP_ERROR_MSG_PAGE_NOT,
    RESP_ERROR_MSG_METHOD_NOT_ALLOWED,
    RESP_ERROR_MSG_BAD_REQUEST,
    RESP_ERROR_MSG_INTERNAL_SERVER_ERROR
)


class TestErroHandlersView(unittest.TestCase):
    """class extending TestCase class from the unitcase module"""

    def setUp(self):
        """initializing method for every unit test"""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_bad_request_error(self):
        """unit test for bad request error"""
        login_reponse = self.client.post(
            URL_LOGIN,
            data="It's supposed to be json format",
            content_type="application/json"
        )
        response_data = json.loads(login_reponse.data.decode())
        self.assertEqual(login_reponse.status_code, 400)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_BAD_REQUEST)

    def test_page_not_found(self):
        """unit test for page not found error"""
        response = self.client.get(
            "url/not/exist", content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_PAGE_NOT)

    def test_method_not_allowed(self):
        """unit test for method not allowed error"""
        response = self.client.patch(URL_REGISTER, data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_METHOD_NOT_ALLOWED)

    def test_internal_server_error(self):
        """unit test for internal servel error"""
        response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="text")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_INTERNAL_SERVER_ERROR)

    def test_index_page(self):
        """unit test for success to index endpoint"""
        response = self.client.get(URL_BASE, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data).get("message"), WELCOME_MSG)
