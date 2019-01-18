"""module with unit test for testing auth_view"""
import unittest

from flask import json

from app import create_app
from app.utilitiez.static_strings import (
    URL_REGISTER,
    URL_LOGIN,

    RESP_SUCCESS_MSG_REGISTRATION,
    RESP_SUCCESS_MSG_AUTH_LOGIN,

    RESP_ERROR_MSG_LOGIN_FAILED,
    RESP_ERROR_MSG_SIGNUP,
    RESP_ERROR_MSG_SIGNUP_FAIL_WRONG_FORMAT,
    RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS,
    RESP_ERROR_MSG_EMPTY_STRING
)


class TestAuthView(unittest.TestCase):
    """class extending the TestcCase class from unittest"""

    def setUp(self):
        """initializing method for the test class"""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_register_user_emptyfield(self):
        """test register with an empty field"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "smith",
            "othernames": "eddy",
            "email": "edwardpjoth@bolon.emp",
            "phonenumber": "0889899999",
            "username": "edwardpjoth",
            "password": "  "
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.data)["message"],
            RESP_ERROR_MSG_SIGNUP_FAIL_WRONG_FORMAT
        )

    def test_register_lessfields(self):
        """test register an invalid user with less fields"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "othernames": "eddy",
            "email": "edwardpjoth@bolon.emp",
            "phonenumber": "0888999777",
            "username": "edwardpjoth",
            "password": "passworD1#"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP)

    def test_register_wrongfield(self):
        """test register with a field which isnt supposed to be their"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstnamef": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            "email": "edwardpjoth@bolon.emp",
            "phonenumber": "0888826272",
            "username": "edwardpjoth",
            "password": "passworD1#"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP)

    def test_register_morefields(self): 
        """test register with more fields than necessary"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            "email": "edwardpjoth@bolon.emp",
            "phonenumber": "0999373634",
            "username": "edwardpjoth",
            "is_admin": True,
            "password": "passworD1#"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP)

    def test_register_wrongtype(self):
        """test register user with a  field of wrong datatype"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": 67,
            "othernames": "edd",
            "email": "edward@bolon.emp",
            "phonenumber": "0888232423",
            "username": "edwardpjoth",
            "password": "passworD1#"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP)

    def test_register_invalidmail(self):
        """test register user with an invalid email"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            'phonenumber': "0777727727",
            "email": "edward.bolon.emp",
            "username": "edwardpjoth",
            "password": "passworD#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP_FAIL_WRONG_FORMAT)

    def test_register_invaliphone(self):
        """test register user with an invalid phonenumber"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            'phonenumber': "4777727727",
            "email": "edwardpjoth@bolon.emp",
            "username": "edwardpjoth",
            "password": "passworD#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP_FAIL_WRONG_FORMAT)

    def test_register_invalidpass(self):
        """test register with an invalid password"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "ann",
            "lastname": "pjoth",
            "othernames": "annthewoman",
            'phonenumber': "0777727727",
            "email": "annpjoth@bolon.emp",
            "username": "edwardpjoth",
            "password": "password#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP_FAIL_WRONG_FORMAT)

    def test_register_invalidothername(self):
        """test register with an invalid othername"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "ann",
            "lastname": "pjoth",
            "othernames": "annthewoman6",
            'phonenumber': "0777727727",
            "email": "annpjoth@bolon.emp",
            "username": "edwardpjoth",
            "password": "password#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP)

    def test_register_invalidfirstname(self):
        """test register with an invalid firstname"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "7gdhu",
            "lastname": "pjoth",
            "othernames": "annthewoman6",
            'phonenumber': "0777727727",
            "email": "annpjoth@bolon.emp",
            "username": "edwardpjoth",
            "password": "password#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP)

    def test_register_invalidusername(self):
        """test register with an invalid username"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            'phonenumber': "0777727727",
            "email": "edwardpjoth@bolon.emp",
            "username": "8776",
            "password": "passworD#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP)

    def test_register_successfully(self):
        """test register user successifully"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            'phonenumber': "0777727727",
            "email": "edwardpjoth@bolon.emp",
            "username": "edwardpjoth",
            "password": "passworD#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_SUCCESS_MSG_REGISTRATION)

    def test_register_withoutothernames(self):
        """test register user successifully without othernames"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "allen",
            "lastname": "garcia",
            "email": "allengarcia@bolon.emp",
            "phonenumber": "0969373634",
            "username": "allengarcia",
            "password": "passworD1#"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_SUCCESS_MSG_REGISTRATION)

    def test_register_takenusername(self):
        """test register user with username already taken"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            'phonenumber': "0787727727",
            "email": "edwardpjoth2@bolon.emp",
            "username": "edwardpjoth",
            "password": "passworD#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS)

    def test_register_takenemail(self):
        """test register user with email already taken"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            'phonenumber': "0797727727",
            "email": "edwardpjoth@bolon.emp",
            "username": "edwardpjoth2",
            "password": "passworD#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS)

    def test_register_takenphone(self):
        """test register user with phone already taken"""
        response = self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edward",
            "lastname": "pjoth",
            "othernames": "eddy",
            'phonenumber': "0777727727",
            "email": "edwardpjoth3@bolon.emp",
            "username": "edwardpjoth3",
            "password": "passworD#1"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS)

    def test_signin_wrongpassword(self):
        """test sign-in with wrong password"""
        response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward5",
            "password": "wrongpassword"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_LOGIN_FAILED)

    def test_signin_emptyfield(self):
        """test sign in with an empty field"""
        response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward6",
            "password": ""
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("message"), RESP_ERROR_MSG_EMPTY_STRING)

    def test_signin_successfully(self):
        """test sign in successfully"""
        response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "allengarcia",
            "password": "passworD1#"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data).get(
            "message"), RESP_SUCCESS_MSG_AUTH_LOGIN)
