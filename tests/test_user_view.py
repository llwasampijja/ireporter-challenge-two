import unittest
from app import create_app
from flask import json


class TestUserView(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.admin_login_response = self.client.post("api/v1/auth/users/login", data=json.dumps({
            "username":"edward",
            "password":"i@mG8t##"
        }), content_type="application/json")
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]

        response = self.client.get(
            "api/v1/auth/users", headers=dict(Authorization='Bearer ' + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.client.post("api/v1/auth/users", data=json.dumps({
            "firstnamef": "Edward",
            "lastname": "8",
            "othernames": "eddy2",
            "email": "edward3@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward3",
            "password": "ABd1234@1"
        }), content_type="application/json")

    def test_add_user(self):
        """Add an invalid user """
        response = self.client.post("api/v1/auth/users/register", data=json.dumps({
            "firstnamef": "Edward",
            "lastname": "8",
            "othernames": "eddy2",
            "email": "edward8@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward8",
            "password": "ABd1234@1"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "An invalid user or Wrong datatype entered")

        """Add user with an empty string, ie for name"""
        response = self.client.post("api/v1/auth/users/register", data=json.dumps({
            "firstname": "Edward",
            "lastname": "  ",
            "othernames": "eddy2",
            "email": "edward9@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward9",
            "password": "ABd1234@1"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Entered an empty field or an invalid email address, phonenumber or password")

        """Add user with an invalid email address"""
        response = self.client.post("api/v1/auth/users/register", data=json.dumps({
            "firstname": "Edward",
            "lastname": "  Army",
            "othernames": "eddy2",
            "email": "edward10@boloncom",
            "phonenumber": "0775961853",
            "username": "edward10",
            "password": "ABd1234@1"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Entered an empty field or an invalid email address, phonenumber or password")

        
        """Add user with an invalid phone number"""
        response = self.client.post("api/v1/auth/users/register", data=json.dumps({
            "firstname": "Edward",
            "lastname": "  Army",
            "othernames": "eddy2",
            "email": "edward@boloncom",
            "phonenumber": "0775961853",
            "username": "edward",
            "password": "ABd1234@1"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Entered an empty field or an invalid email address, phonenumber or password")

        """Add duplicate user"""
        response = self.client.post("api/v1/auth/users/register", data=json.dumps({
            "firstname": "Edward",
            "lastname": " Army",
            "othernames": "eddy3",
            "email": "edward@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward",
            "password": "ABd1234@1"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Email address or username is already taken")

        """Add user with an invalid password"""
        response = self.client.post("api/v1/auth/users/register", data=json.dumps({
            "firstname": "Edward",
            "lastname": "Army",
            "othernames": "eddy2",
            "email": "edward4@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward4",
            "password": "ABd12341"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Entered an empty field or an invalid email address, phonenumber or password")

        # """Add user with an invalid admin status"""
        # response = self.client.post("api/v1/auth/users", data=json.dumps({
        #     "firstname": "Edward",
        #     "lastname": "Army",
        #     "othernames": "eddy2",
        #     "email": "edward5@bolon.com",
        #     "phonenumber": "0775961853",
        #     "username": "edward5",
        #     "password": "ABd1234@1"
        # }), content_type="application/json")
        # data = json.loads(response.data.decode())
        # self.assertEqual(response.status_code, 400)
        # self.assertEqual(data.get("message"), "An invalid user or Wrong datatype entered")

        """Add user with an invalid name, i.e., integer name"""
        response = self.client.post("api/v1/auth/users/register", data=json.dumps({
            "firstname": "Edward",
            "lastname": 3,
            "othernames": "eddy2",
            "email": "edward5@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward5",
            "password": "ABd1234@1"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "An invalid user or Wrong datatype entered")

        """Add user with valid fields"""
        response = self.client.post("api/v1/auth/users/register", data=json.dumps({
            "firstname": "Edward",
            "lastname": "Kased",
            "othernames": "eddy2",
            "email": "edward6@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward6",
            "password": "ABd1234@1"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"), "User account created successifully")

    def test_update_user(self):
        """test update user's role by admin"""
        jwt_token = json.loads(self.admin_login_response.data)["access_token"]
        response = self.client.patch("api/v1/auth/users/2", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "is_admin": True
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"), "The admin rights of the user have been updated successifully")

        """test update user status with more fields than required"""
        response = self.client.patch("api/v1/auth/users/2", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "firstname":"no one",
            "is_admin":True
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"), "An administrator can only edit a user's role")

        """test update user's role with an invalid value"""
        response = self.client.patch("api/v1/auth/users/2", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "is_admin":"admin"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("message"), "The value can either be true (admin) or false (not admin)")

        """test update a user who doesnt exist on the system"""
        response = self.client.patch("api/v1/auth/users/45", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "is_admin":True
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("message"), "That specified user wasn't found on the system")


    def test_signin(self):
        """test sign-in with wrong password"""
        response = self.client.post("api/v1/auth/users/login", data=json.dumps({
            "username":"edward5",
            "password":"wrongpassword"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("message"), "Failed to login, username or password is incorrect")

        """test sign in with an empty field"""
        response = self.client.post("api/v1/auth/users/login", data=json.dumps({
            "username":"edward6",
            "password":""
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("message"), "No empty fields are allowed")



