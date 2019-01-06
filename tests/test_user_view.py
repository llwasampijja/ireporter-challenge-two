import unittest
from flask import json
from app import create_app
from app.utilitiez.static_strings import URL_REGISTER, URL_LOGIN, URL_USERS, RESP_ADMIN_RIGHTS_SUCCESS, RESP_ROLE_NO_RIGHTS, RESP_ROLE_INVALID, RESP_USER_NOT_FOUND



class TestUserView(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username":"edward",
            "password":"i@mG8t##"
        }), content_type="application/json")
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]

        response = self.client.get(
            URL_USERS + "", headers=dict(Authorization='Bearer ' + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        # self.client.post(URL_REGISTER, data=json.dumps({
        #     "firstnamef": "Edward",
        #     "lastname": "8",
        #     "othernames": "eddy2",
        #     "email": "edward3@bolon.com",
        #     "phonenumber": "0775961853",
        #     "username": "edward3",
        #     "password": "ABd1234@1"
        # }), content_type="application/json")

    def test_update_user(self):
        """test update user's role by admin"""
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        response = self.client.patch(URL_USERS + "/2", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "is_admin": True
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"), RESP_ADMIN_RIGHTS_SUCCESS)

        """test update user status with more fields than required"""
        response = self.client.patch(URL_USERS + "/2", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "firstname":"no one",
            "is_admin":True
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"), RESP_ROLE_NO_RIGHTS)

        """test update user's role with an invalid value"""
        response = self.client.patch(URL_USERS + "/2", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "is_admin":"admin"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("message"), RESP_ROLE_INVALID)

        """test update a user who doesnt exist on the system"""
        response = self.client.patch(URL_USERS + "/45", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "is_admin":True
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("message"), RESP_USER_NOT_FOUND)

        """test update a primary admin"""
        response = self.client.patch(URL_USERS + "/1", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "is_admin":True
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"), RESP_ROLE_NO_RIGHTS)






