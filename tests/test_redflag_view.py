import unittest
from app.models.incident_model import IncidentData
from app.controllers.incident_controller import IncidentController
from app import create_app
from flask import Response, json


class TestRedflagView (unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client(self)
        test_user = {
            "firstname": "Dall",
            "lastname": "Kased",
            "othernames": "eddy2",
            "email": "dall@bolon.com",
            "phonenumber": "0775961853",
            "username": "dallkased",
            "password": "ABd1234@1"
        }
        self.client.post("api/v1/auth/users/register", data=json.dumps(test_user),
                         content_type="application/json")
        self.login_response = self.client.post("api/v1/auth/users/login", data=json.dumps({
            "username": "dallkased",
            "password": "ABd1234@1"
        }), content_type="application/json")

        """get redflags before logging in"""
        response = self.client.get(
            "api/v1/red-flags", content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data.get("message"), None)

        """get redflags after logging in"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get("api/v1/red-flags", headers=dict(
            Authorization='Bearer ' + jwt_token), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_create_redflag(self):
        """redflag to ensure that the list is not empty when one item is deleted during testing for deleting"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "Kawempe",
            "status": "Pending Investigation",
            "videos": ["Video url"],
            "images": ["images urls"],
            "comment": "He was caught red handed"
        }), content_type="application/json")

        """Test for creating a valid red-flag"""
        response = self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "Kawempe",
            "status": "Pending Investigation",
            "videos": ["Video url"],
            "images": ["images urls"],
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"), "Incident created successifully")

        """Test for creating an invalid red-flag missing one required parameter"""
        response = self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "Kawempe",
            "videos": ["Video url"],
            "images": ["images urls"],
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         "Unaccepted datatype or Inavlid incident")

        """Test for creating an invalid red-flag with more parameters than needed"""
        response = self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "Kawempe",
            "videos": ["Video url"],
            "images": ["images urls"],
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         "Unaccepted datatype or Inavlid incident")

        """Test for creating an invalid red-flag with string of vidoes instead of list"""
        response = self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "Kawempe",
            "status": "Pending Investigation",
            "videos": ["Video url"],
            "images": "images urls",
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         "Unaccepted datatype or Inavlid incident")

        """Test for creating an invalid red-flag with an int value instead of string for status"""
        response = self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "Kawempe",
            "status": 55,
            "videos": ["Video url"],
            "images": "images urls",
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         "Unaccepted datatype or Inavlid incident")

        """Test for creating an invalid red-flag with an empty string"""
        response = self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": " ",
            "status": "pending investigation",
            "videos": ["Video url"],
            "images": "images urls",
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         "No empty fields are allowed")

        """Test for creating an invalid red-flag with a wrong status"""
        response = self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "0.333, 1.45343",
            "status": "status doesnt exist",
            "videos": ["Video url"],
            "images": ["images urls"],
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         "Wrong Status given")

    def test_get_redflags(self):
        """test get all redflags"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            "api/v1/red-flags", headers=dict(Authorization='Bearer ' + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        """test get all redflags when you are not not an admin or concerned citzen"""
        noone_login_response = self.client.post("api/v1/auth/users/login", data=json.dumps({
            "username": "jetli",
            "password": "i@mG8t##"
        }), content_type="application/json")
        noone_jwt_token = json.loads(noone_login_response.data)["access_token"]
        response = self.client.get("api/v1/red-flags", headers=dict(
            Authorization='Bearer ' + noone_jwt_token), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("message"),
                         "You are not authorised to access this content")

    def test_get_redflag(self):
        """Test get redflag with available id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            "api/v1/red-flags/2", headers=dict(Authorization='Bearer ' + jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        """Test get redflag with with id not available"""
        response = self.client.get(
            "api/v1/red-flags/19", headers=dict(Authorization='Bearer ' + jwt_token), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         "No incident of that specific id found")

    def test_update_redflag(self):
        """Test update redflag with wrong url"""
        new_location = {"location": "1.500, 0.3000"}
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            "api/v1/red-flags/4/wrong",  headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps(new_location), content_type="application/json")
        self.assertEqual(response.status_code, 404)

        """Test update redflag with unavailable id"""
        response = self.client.patch(
            "api/v1/red-flags/4/location", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps(new_location), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         "No incident of that specific id found")

        """Test update redflag with empty string"""
        response = self.client.patch(
            "api/v1/red-flags/2/location", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({"location": "  "}), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         "No empty fields are allowed")

        """Test update redflag with the wrong data type """
        response = self.client.patch("api/v1/red-flags/2/location", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps(
            {"location": 334}), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         "Unaccepted datatype or Inavlid incident")

        """test update redflag which one never created"""
        # self.client.post("api/v1/auth/users/register", data=json.dumps({
        #     "firstname": "ann",
        #     "lastname": "smith",
        #     "othernames": "bolon",
        #     "email": "ann@bolon.com",
        #     "phonenumber": "0775961853",
        #     "username": "ann",
        #     "password": "ABd1234@1"
        # }), content_type="application/json")
        # ann_login_reponse = self.client.post("api/v1/auth/users/login", data=json.dumps({
        #     "username":"ann",
        #     "password":"ABd1234@1"
        # }), content_type="application/json")
        # ann_jwt_token = json.loads(ann_login_reponse.data)["access_token"]
        response = self.client.patch("api/v1/red-flags/1/location", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "location": "2.000, 0.400"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         "You are not authorised to edit this incident.")

        """Test update redflag with the right id"""
        response = self.client.patch("api/v1/red-flags/2/location", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps(
            {"location": "1.500, 0.3000"}), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         "Updated incident record’s location")

        """test update red-flag's status as a concerned citzen"""
        response = self.client.patch("api/v1/red-flags/2/status", headers=dict(Authorization='Bearer ' + jwt_token), data=json.dumps({
            "status": "rejected"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("message"),
                         "This feature is only available to adminitrators")

    def test_delete_redflag(self):
        """Test delete red-flag with unavailable id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.delete(
            "api/v1/red-flags/300", headers=dict(Authorization='Bearer ' + jwt_token), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         "No incident of that specific id found")

        """Test delete red-flag with unavailable id"""
        response = self.client.delete(
            "api/v1/red-flags/3", headers=dict(Authorization='Bearer ' + jwt_token), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"), "Incident deleted successfully")

    def test_update_redflag_status(self):
        """Test update status of redflag by admin"""
        admin_login_response = self.client.post("api/v1/auth/users/login", data=json.dumps({
            "username": "edward",
            "password": "i@mG8t##"
        }), content_type="application/json")
        admin_jwt_token = json.loads(admin_login_response.data)["access_token"]
        response = self.client.patch("api/v1/red-flags/2/status", headers=dict(Authorization='Bearer ' + admin_jwt_token), data=json.dumps({
            "status": "rejected"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         "Updated incident record’s status")

        """test update red-flag with more than just the status as an admin"""
        response = self.client.patch("api/v1/red-flags/2/status", headers=dict(Authorization='Bearer ' + admin_jwt_token), data=json.dumps({
            "status":"rejected",
            "comment":"You are lieing, you will be arrested for trying to destroy the name of a good man"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"), "An admin can only edit the status of an incident, nothing more. The only accepted values include: 'pending investigation', 'resolved' and 'rejected'")

        """test update the status of an incident which doesn't exist"""
        response = self.client.patch("api/v1/red-flags/300/status", headers=dict(Authorization='Bearer ' + admin_jwt_token), data=json.dumps({
            "status":"resolved"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("message"), "No incident of that specific id found")


        """test try to create an incident as an admin"""
        response = self.client.post("api/v1/red-flags", headers=dict(Authorization='Bearer ' + admin_jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": " ",
            "status": "pending investigation",
            "videos": ["Video url"],
            "images": "images urls",
            "comment": "He was caught red handed"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("message"),
                         "You are not authorised to access this content")
