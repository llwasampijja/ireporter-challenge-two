"""module containing unit tests for the users route"""

import unittest

from flask import json

from databases.ireporter_db import IreporterDb
from databases.database_helper import DatabaseHelper
from tests.common_test import CommonTest

from app import create_app
from app.utilities.static_strings import (
    URL_LOGIN,
    URL_REGISTER,
    URL_USERS,
    URL_REDFLAGS,

    RESP_SUCCESS_MSG_ADMIN_RIGHTS,

    RESP_ERROR_MSG_USER_STATUS_NORIGHTS,
    RESP_ERROR_MSG_INVALID_ROLE,
    RESP_ERROR_MSG_USER_NOT_FOUND,
    RESP_ERROR_MSG_NOT_LOGGEDIN
)


class TestUserView(unittest.TestCase):
    """testing class extending class TestCase from the unittest module"""
    common_test = CommonTest()

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app()
        self.client = self.app.test_client()

        self.ireporter_db = IreporterDb()
        self.database_helper = DatabaseHelper()
        self.ireporter_db.create_tables()
        self.database_helper.create_admin()
        self.database_helper.create_incident_types()

        # self.client.post(URL_REGISTER, data=json.dumps({
        #     "firstname": "edwardd",
        #     "lastname": "pjothw",
        #     "othernames": "eddry",
        #     "phonenumber": "0763372772",
        #     "email": "edwardpjoth3@bolon.emp",
        #     "username": "edwardpjothedwardme",
        #     "password": "passworD#1"
        # }), content_type="application/json")

        self.test_data1 = {
            "location": "2.00, 3.222",
            "videos": ["Video url"],
            "images": ["images urls"],
            "title": "this road is bad",
            "comment": "4567 The road has very bif potholes"   
        }

        self.test_user1 = {
            "firstname": "edwardd",
            "lastname": "pjothw",
            "othernames": "eddry",
            'phonenumber': "0763372772",
            "email": "edwardpjoth3@bolon.emp",
            "username": "edwardpjothedwardme",
            "password": "passworD#1"
        }

        self.test_user_token = self.common_test.nonadmin_author_token()

        self.admin_jwt_token = self.common_test.admin_jwt_token()

        # self.admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
        #     "username": "edward",
        #     "password": "i@mG8t##"
        # }), content_type="application/json")
        # jwt_token = json.loads(self.admin_login_response.data)["access_token"]

        response = self.client.get(
            URL_USERS + "",
            headers=dict(Authorization='Bearer ' + self.admin_jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.ireporter_db = IreporterDb()
        self.ireporter_db.drop_tables()

    def test_update_user(self):
        """test update user's role by admin"""
        
        # jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        # response = self.client.patch(
        #     URL_USERS + "/2",
        #     headers=dict(Authorization='Bearer ' + jwt_token),
        #     data=json.dumps({
        #         "is_admin": True
        #     }),
        #     content_type="application/json"
        # )
        response = self.common_test.response_patch_user(
            URL_USERS + "/2", {"is_admin": True}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         RESP_SUCCESS_MSG_ADMIN_RIGHTS)

    def test_update_morefields(self):
        """test update user status with more fields than required"""
        # jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        # response = self.client.patch(
        #     URL_USERS + "/2",
        #     headers=dict(Authorization='Bearer ' + jwt_token),
        #     data=json.dumps({
        #         "firstname": "no one",
        #         "is_admin": True
        #     }),
        #     content_type="application/json"
        # )
        response = self.common_test.response_patch_user(
            URL_USERS + "/2", {"firstname": "no one", "is_admin": True}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_USER_STATUS_NORIGHTS)

    def test_update_roleinvalid(self):
        """test update user's role with an invalid value"""
        # jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        # response = self.client.patch(
        #     URL_USERS + "/2",
        #     headers=dict(Authorization='Bearer ' + jwt_token),
        #     data=json.dumps({
        #         "is_admin": "admin"
        #     }),
        #     content_type="application/json"
        # )
        response = self.common_test.response_patch_user(
            URL_USERS + "/2", {"is_admin": "admin"}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_INVALID_ROLE)

    def test_update_nonexist(self):
        """test update a user who doesnt exist on the system"""
        # jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        # response = self.client.patch(
        #     URL_USERS + "/45",
        #     headers=dict(Authorization='Bearer ' + jwt_token),
        #     data=json.dumps({
        #         "is_admin": True
        #     }),
        #     content_type="application/json"
        # )
        response = self.common_test.response_patch_user(
            URL_USERS + "/45", {"is_admin": True}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_USER_NOT_FOUND)

    def test_update_user_nonuser(self):
        """test update user's role by admin"""
        
        # jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_USERS + "/2",
            # headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "is_admin": True
            }),
            content_type="application/json"
        )
        # response = self.common_test.response_patch_user(
        #     URL_USERS + "/2", {"is_admin": True}, self.admin_jwt_token
        # )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_NOT_LOGGEDIN)

    def test_update_primaryadmin(self):
        """test update a primary admin"""
        response = self.common_test.response_patch_user(
            URL_USERS + "/1", {"is_admin": True}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_USER_STATUS_NORIGHTS)

    def test_get_redflags_specific_user_noid(self):
        """unit test for getting all redflags for spefic user"""
        test_user_three = {
            "firstname": "jet",
            "lastname": "li",
            "othernames": "realli",
            "email": "jet@bolon.com",
            "phonenumber": "0761857597",
            "username": "jetli",
            "password": "ABd1234@1"
        }
        self.client.post(
            URL_REGISTER, data=json.dumps(
                test_user_three
            ),
            content_type="application/json"
        )
        test_login_response = self.client.post(
            URL_LOGIN, data=json.dumps({
                "username": "jetli",
                "password": "ABd1234@1"
            }),
            content_type="application/json"
        )
        jwt_token = json.loads(test_login_response.data)["access_token"]
        response = self.common_test.response_get_users(
            URL_USERS + "/3000/red-flags", jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_USER_NOT_FOUND)

    def test_get_interventions_specific_user_listempty(self):
        """unit test for getting all redflags for spefic user"""
        self.common_test.response_register_user(self.test_user1)
        response = self.common_test.response_get_users(
            URL_USERS + "/2/interventions", self.admin_jwt_token
        )
        self.assertEqual(response.status_code, 200)

    def test_get_interventions_specific_user_noright(self):
        """unit test for getting all redflags for spefic user"""
        response = self.common_test.response_get_users(
            URL_USERS + "/1/interventions", self.test_user_token
        )
        self.assertEqual(response.status_code, 401)

    def test_get_redflags_specific_user_listnonempty(self):
        """unit test for getting all redflags for spefic user"""
        post_response = self.common_test.response_post_incident(
            URL_REDFLAGS, self.test_data1, self.test_user_token
        )
        self.assertEqual(post_response.status_code, 201)
        response = self.common_test.response_get_users(
            URL_USERS + "/2/red-flags", self.admin_jwt_token
        )
        self.assertEqual(response.status_code, 200)
