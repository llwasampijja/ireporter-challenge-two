"""module containing unit tests for the users route"""

import unittest

from flask import json

from databases.ireporter_db import IreporterDb
from databases.database_helper import DatabaseHelper

from app import create_app
from app.utilities.static_strings import (
    URL_LOGIN,
    URL_REGISTER,
    URL_USERS,
    URL_REDFLAGS,

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

        self.ireporter_db = IreporterDb()
        self.database_helper = DatabaseHelper()
        self.ireporter_db.drop_tables()
        self.ireporter_db.create_tables()
        self.database_helper.create_admin()
        self.database_helper.create_incident_types()

        self.client.post(URL_REGISTER, data=json.dumps({
            "firstname": "edwardd",
            "lastname": "pjothw",
            "othernames": "eddry",
            'phonenumber': "0763372772",
            "email": "edwardpjoth3@bolon.emp",
            "username": "edwardpjothedwardme",
            "password": "passworD#1"
        }), content_type="application/json")

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

    # def test_update_morefields(self):
    #     """test update user status with more fields than required"""
    #     jwt_token = json.loads(self.admin_login_response.data)["access_token"]
    #     response = self.client.patch(
    #         URL_USERS + "/2",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps({
    #             "firstname": "no one",
    #             "is_admin": True
    #         }),
    #         content_type="application/json"
    #     )
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_USER_STATUS_NORIGHTS)

    # def test_update_roleinvalid(self):
    #     """test update user's role with an invalid value"""
    #     jwt_token = json.loads(self.admin_login_response.data)["access_token"]
    #     response = self.client.patch(
    #         URL_USERS + "/2",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps({
    #             "is_admin": "admin"
    #         }),
    #         content_type="application/json"
    #     )
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_INVALID_ROLE)

    # def test_update_nonexist(self):
    #     """test update a user who doesnt exist on the system"""
    #     jwt_token = json.loads(self.admin_login_response.data)["access_token"]
    #     response = self.client.patch(
    #         URL_USERS + "/45",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps({
    #             "is_admin": True
    #         }),
    #         content_type="application/json"
    #     )
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_USER_NOT_FOUND)

    # def test_update_primaryadmin(self):
    #     """test update a primary admin"""
    #     jwt_token = json.loads(self.admin_login_response.data)["access_token"]
    #     response = self.client.patch(
    #         URL_USERS + "/1",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps({
    #             "is_admin": True
    #         }),
    #         content_type="application/json"
    #     )
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_USER_STATUS_NORIGHTS)

    # def test_get_redflags_specific_user_noid(self):
    #     """unit test for getting all redflags for spefic user"""
    #     test_user_three = {
    #         "firstname": "jet",
    #         "lastname": "li",
    #         "othernames": "realli",
    #         "email": "jet@bolon.com",
    #         "phonenumber": "0761857597",
    #         "username": "jetli",
    #         "password": "ABd1234@1"
    #     }
    #     self.client.post(
    #         URL_REGISTER, data=json.dumps(
    #             test_user_three
    #         ),
    #         content_type="application/json"
    #     )
    #     test_login_response = self.client.post(
    #         URL_LOGIN, data=json.dumps({
    #             "username": "jetli",
    #             "password": "ABd1234@1"
    #         }),
    #         content_type="application/json"
    #     )

    #     jwt_token = json.loads(test_login_response.data)["access_token"]
    #     response = self.client.get(
    #         URL_USERS + "/3000/red-flags",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         content_type="application/json"
    #     )
    #     response_data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_USER_NOT_FOUND)

    # def test_get_interventions_specific_user_listempty(self):
    #     """unit test for getting all redflags for spefic user"""
    #     test_user_three = {
    #         "firstname": "jet",
    #         "lastname": "li",
    #         "othernames": "realli",
    #         "email": "jet@bolon.com",
    #         "phonenumber": "0761857597",
    #         "username": "jetli",
    #         "password": "ABd1234@1"
    #     }
    #     self.client.post(
    #         URL_REGISTER, data=json.dumps(
    #             test_user_three
    #         ),
    #         content_type="application/json"
    #     )

    #     admin_jwt_token = json.loads(self.admin_login_response.data)["access_token"]
    #     response = self.client.get(
    #         URL_USERS + "/2/interventions",
    #         headers=dict(Authorization='Bearer ' + admin_jwt_token),
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_get_interventions_specific_user_noright(self):
    #     """unit test for getting all redflags for spefic user"""

    #     test_login_response = self.client.post(
    #         URL_LOGIN, data=json.dumps({
    #             "username": "edwardpjothedwardme",
    #             "password": "ABd1234@1"
    #         }),
    #         content_type="application/json"
    #     )

    #     jwt_token = json.loads(test_login_response.data)["access_token"]
    #     response = self.client.get(
    #         URL_USERS + "/1/interventions",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 401)

    # def test_get_redflags_specific_user_listnonempty(self):
    #     """unit test for getting all redflags for spefic user"""
    #     test_user_three = {
    #         "firstname": "jet",
    #         "lastname": "li",
    #         "othernames": "realli",
    #         "email": "jet@bolon.com",
    #         "phonenumber": "0761857597",
    #         "username": "jetli",
    #         "password": "ABd1234@1"
    #     }
    #     self.client.post(
    #         URL_REGISTER, data=json.dumps(
    #             test_user_three
    #         ),
    #         content_type="application/json"
    #     )
    #     test_login_response = self.client.post(
    #         URL_LOGIN, data=json.dumps({
    #             "username": "jetli",
    #             "password": "ABd1234@1"
    #         }),
    #         content_type="application/json"
    #     )

    #     jwt_token = json.loads(test_login_response.data)["access_token"]
    #     post_response = self.client.post(
    #         URL_REDFLAGS,
    #         headers = dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps({
    #             "location": "2.00, 3.222",
    #             "videos": ["Video url"],
    #             "images": ["images urls"],
    #             "title": "this road is bad",
    #             "comment": "4567 The road has very bif potholes"
    #         }),
    #         content_type="application/json"
    #     )
    #     admin_jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        
    #     self.assertEqual(post_response.status_code, 201)
    #     response = self.client.get(
    #         URL_USERS + "/3/red-flags",
    #         headers=dict(Authorization='Bearer ' + admin_jwt_token),
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 200)
