"""module containing unit tests for the users route"""

import unittest

from flask import json

from app import create_app
from app.utilitiez.static_strings import (
    URL_LOGIN,
    URL_USERS,

    RESP_SUCCESS_MSG_ADMIN_RIGHTS,

    RESP_ERROR_MSG_USER_STATUS_NORIGHTS,
    RESP_ERROR_MSG_INVALID_ROLE,
    RESP_ERROR_MSG_USER_NOT_FOUND
)


class TestUserView(unittest.TestCase):
    """testing class extending class TestCase from the unittest module"""

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app()
        self.client = self.app.test_client()

        self.admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward",
            "password": "i@mG8t##"
        }), content_type="application/json")
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]

        response = self.client.get(
            URL_USERS + "",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        """test update user's role by admin"""
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_USERS + "/2",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "is_admin": True
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         RESP_SUCCESS_MSG_ADMIN_RIGHTS)

    def test_update_morefields(self):
        """test update user status with more fields than required"""
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_USERS + "/2",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "firstname": "no one",
                "is_admin": True
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"), RESP_ERROR_MSG_USER_STATUS_NORIGHTS)

    def test_update_roleinvalid(self):
        """test update user's role with an invalid value"""
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_USERS + "/2",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "is_admin": "admin"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("message"), RESP_ERROR_MSG_INVALID_ROLE)

    def test_update_nonexist(self):
        """test update a user who doesnt exist on the system"""
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_USERS + "/45",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "is_admin": True
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("message"), RESP_ERROR_MSG_USER_NOT_FOUND)

    def test_update_primaryadmin(self):
        """test update a primary admin"""
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_USERS + "/1",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "is_admin": True
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"), RESP_ERROR_MSG_USER_STATUS_NORIGHTS)
