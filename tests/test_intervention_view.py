import unittest
from app.models.incident_model import IncidentData
from app.controllers.incident_controller import IncidentController
from app import create_app
from flask import Response, json


class TestInterventionView (unittest.TestCase):

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
        }),content_type="application/json")

        # """try to get list of interventions without logging in first"""
        # response = self.client.get(
        #     "api/v1/interventions", content_type="application/json")
        # data = json.loads(response.data.decode())
        # self.assertEqual(response.status_code, 401)
        # self.assertEqual(data.get("message"),None)

        # """get list of interventions after logging in """
        # jwt_token = json.loads(self.login_response.data)["access_token"]
        # response = self.client.get(
        #     "api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), content_type="application/json")
        # data = json.loads(response.data.decode())
        # self.assertEqual(response.status_code, 404)
        # self.assertEqual(data.get("message"),"incidents list is empty")

    def test_create_intervention(self):
        """intervention to ensure that the list is not empty when one item is deleted during testing for deleting"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        self.client.post("api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "Kawempe",
            "status": "Pending Investigation",
            "videos": ["Video url"],
            "images": ["images urls"],
            "comment": "He was caught red handed"
        }), content_type="application/json")

        """Test for creating a valid intervention"""
        response = self.client.post("api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "Kawempe",
            "status": "Pending Investigation",
            "videos": ["Video url"],
            "images": ["images urls"],
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         "Incident created successifully")

        """Test for creating an invalid intervention missing one required parameter"""
        response = self.client.post("api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), data=json.dumps({
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

        """Test for creating an invalid intervention with more parameters than needed"""
        response = self.client.post("api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), data=json.dumps({
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

        """Test for creating an invalid intervention with string of vidoes instead of list"""
        response = self.client.post("api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), data=json.dumps({
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

        """Test for creating an invalid intervention with an int value instead of string for status"""
        response = self.client.post("api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), data=json.dumps({
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

        """Test for creating an invalid intervention with an empty string"""
        response = self.client.post("api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "",
            "status": 55,
            "videos": ["Video url"],
            "images": "images urls",
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         "No empty fields are allowed")

        """Test for creating an invalid intervention with an invalid status"""
        response = self.client.post("api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), data=json.dumps({
            "created_by": "Jon Mark",
            "location": "0.2009, 1.3443",
            "status": "wrong status",
            "videos": ["Video url"],
            "images": ["images urls"],
            "comment": "He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         "Wrong Status given")

    def test_get_interventions(self):
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            "api/v1/interventions", headers=dict(Authorization='Bearer '+ jwt_token), content_type="application/json")
        self.assertEqual(response.status_code, 200)