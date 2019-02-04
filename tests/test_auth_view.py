"""module with unit test for testing auth_view"""
import unittest

from flask import json

from databases.ireporter_db import IreporterDb
from databases.database_helper import DatabaseHelper
from tests.common_test import CommonTest

from app import create_app
from app.utilities.static_strings import (
    URL_REGISTER,
    URL_LOGIN,

    RESP_SUCCESS_MSG_REGISTRATION,
    RESP_SUCCESS_MSG_AUTH_LOGIN,

    RESP_ERROR_MSG_LOGIN_FAILED,
    RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS,
    RESP_ERROR_MSG_EMPTY_STRING,
    RESP_ERROR_MSG_INVALID_USER,
    RESP_ERROR_MSG_INVALID_OTHERNAME,
    RESP_ERROR_MSG_INVALID_NAME,
    RESP_ERROR_MSG_INVALID_USERNAME,
    RESP_ERROR_MSG_INVALID_EMAIL,
    RESP_ERROR_MSG_INVALID_PHONE,
    RESP_ERROR_MSG_INVALID_PASSWORD
)


class TestAuthView(unittest.TestCase):
    """class extending the TestcCase class from unittest"""
    common_test = CommonTest()
    def setUp(self):
        """initializing method for the test class"""
        self.app = create_app()
        self.client = self.app.test_client()

        self.ireporter_db = IreporterDb()
        self.database_helper = DatabaseHelper()
        self.ireporter_db.create_tables()
        self.database_helper.create_incident_types()
        self.database_helper.create_admin()

        self.test_user1 = {
            "firstname": "edwardd",
            "lastname": "pjothw",
            "othernames": "eddry",
            'phonenumber': "0763372772",
            "email": "edwardpjoth3@bolon.emp",
            "username": "edwardpjothedwardme",
            "password": "passworD#1"
        }

        self.test_user2 = {
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            'phonenumber': "0777727727",
            "email": "edward@bolonyes.emp",
            "username": "edwardpjoth",
            "password": "passworD#1"
        }

        self.common_test.response_register_user(self.test_user1)

    def tearDown(self):
        self.ireporter_db = IreporterDb()
        self.ireporter_db.drop_tables()

    def test_register_user_emptyfield(self):
        """test register with an empty field"""
        self.test_user1.update({"password": "  "})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.data)["error"],
            RESP_ERROR_MSG_INVALID_PASSWORD
        )

    def test_register_lessfields(self):
        """test register an invalid user with less fields"""
        self.test_user1.pop("lastname")
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_USER)

    def test_register_wrongfield(self):
        """test register with a field which isnt supposed to be their"""
        self.test_user1.pop("firstname")
        self.test_user1.update({"firstnamef": "edward"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_USER)

    def test_register_morefields(self): 
        """test register with more fields than necessary"""
        self.test_user1.update({"is_admin": True})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_USER)

    def test_register_wrongtype(self):
        """test register user with a  field of wrong datatype"""
        self.test_user1.update({"lastname": 67})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_NAME)

    def test_register_invalidmail(self):
        """test register user with an invalid email"""
        self.test_user2.update({"email": "edward.bolon.emp"})
        response = self.common_test.response_register_user(self.test_user2)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_EMAIL)

    def test_register_invaliphone(self):
        """test register user with an invalid phonenumber"""
        self.test_user1.update({"phonenumber": "4777727727"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_PHONE)

    def test_register_invalidpass(self):
        """test register with an invalid password"""
        self.test_user1.update({"password": "password#1"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_PASSWORD)

    def test_register_invalidothername(self):
        """test register with an invalid othername"""
        self.test_user1.update({"othernames": "annthewoman6"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_OTHERNAME)

    def test_register_invalidfirstname(self):
        """test register with an invalid firstname"""
        self.test_user1.update({"firstname": "7gdhu"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_NAME)

    def test_register_invalidusername(self):
        """test register with an invalid username"""
        self.test_user1.update({"username": "8776"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_INVALID_USERNAME)

    def test_register_asuccessfully(self):
        """test register user successifully"""
        response = self.common_test.response_register_user(self.test_user2)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_SUCCESS_MSG_REGISTRATION)

    def test_register_withoutothernames(self):
        """test register user successifully without othernames"""
        self.test_user2.pop("othernames")
        response = self.common_test.response_register_user(self.test_user2)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_SUCCESS_MSG_REGISTRATION)

    def test_register_takenusername(self):
        """test register user with username already taken"""
        self.test_user1.update({"username": "edwardpjothedwardme"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS)

    def test_register_takenemail(self):
        """test register user with email already taken"""
        self.test_user1.update({"email": "edwardpjoth3@bolon.emp"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS)

    def test_register_takenphone(self):
        """test register user with phone already taken"""
        self.test_user1.update({"phonenumber": "0777727727"})
        response = self.common_test.response_register_user(self.test_user1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "error"), RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS)

    def test_signin_wrongpassword(self):
        """test sign-in with wrong password"""
        response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward5",
            "password": "wrongpassword"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_LOGIN_FAILED)

    def test_signin_emptyfield(self):
        """test sign in with an empty field"""
        response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward6",
            "password": ""
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_EMPTY_STRING)

    def test_signin_successfully(self):
        """test sign in successfully"""
        response = self.common_test.response_login_user()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_SUCCESS_MSG_AUTH_LOGIN)

