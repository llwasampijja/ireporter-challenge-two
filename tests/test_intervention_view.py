"""module including unit testing class for some of the
 intervention incident fields some of the intervention
 incident are covered by the unit tests for the redflags"""

import unittest

from flask import json

from app import create_app
from app.utilitiez.static_strings import (
    URL_LOGIN,
    RESP_INCIDENT_DUPLICATE,
    RESP_INCIDENT_UPDATE_SUCCESS,
    RESP_INCIDENT_DELETE_SUCCESS,
    RESP_INCIDENT_STATUS_UPDATE_SUCCESS,
    RESP_INCIDENT_NOT_FOUND, URL_REGISTER,
    URL_INTERVENTIONS, RESP_EMPTY_STRING,
    RESP_CREATE_INCIDENT_SUCCESS,
    RESP_INVALID_INCIDENT_INPUT
)


class TestInterventionView(unittest.TestCase):
    """unit testing class for intervention"""

    def setUp(self):
        """initializing method for every unit test"""
        self.app = create_app()
        self.client = self.app.test_client(self)

        test_user = {
            "firstname": "Dall",
            "lastname": "Kased",
            "othernames": "eddy2",
            "email": "dall@bolon.com",
            "phonenumber": "0775961753",
            "username": "dallkased",
            "password": "ABd1234@1"
        }
        self.client.post(URL_REGISTER, data=json.dumps(test_user),
                         content_type="application/json")
        self.login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "dallkased",
            "password": "ABd1234@1"
        }), content_type="application/json")

        # """try to get list of interventions without logging in first"""
        # response = self.client.get(
        #     URL_INTERVENTIONS, content_type="application/json")
        # data = json.loads(response.data.decode())
        # self.assertEqual(response.status_code, 401)
        # self.assertEqual(data.get("message"),None)

        # get list of interventions after logging in
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        # data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(data.get("message"),"incidents list is empty")

    def test_create_intervention(self):
        """create an intervention unit tests"""
        # intervention to ensure that the list is not empty when one item is
        #  deleted during testing for deleting
        jwt_token = json.loads(self.login_response.data)["access_token"]
        self.client.post(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "2.00, 3.222",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "this road is bad",
                "comment": "The road has very bif potholes"
            }),
            content_type="application/json"
        )

        # Test for creating a valid intervention
        response = self.client.post(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "2.00, 3.222",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "bad hospital",
                "comment": "This Hospital's sanitation is really worrying"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_CREATE_INCIDENT_SUCCESS)

        # Test for creating a duplicate intervention
        response = self.client.post(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "2.00, 3.222",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "we need a market",
                "comment": "This Hospital's sanitation is really worrying"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_DUPLICATE)

        # Test for creating an invalid intervention missing one required parameter
        response = self.client.post(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "2.00, 3.222",
                "videos": ["Video url"],
                "comment": "Schoo;l is bad"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_INVALID_INCIDENT_INPUT)

        # Test for creating an invalid intervention with more parameters than needed
        response = self.client.post(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "created_by": "Jon Mark",
                "location": "2.00, 3.222",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "this road is bad",
                "comment": "when i saw the road i was so sad"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_INVALID_INCIDENT_INPUT)

        #Test for creating an invalid intervention with string of vidoes instead of list
        response = self.client.post(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "2.00, 3.222",
                "videos": ["Video url"],
                "images": "images urls",
                "title": "this road is bad",
                "comment": "I saw the headmaster takeing a bribe from parents"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_INVALID_INCIDENT_INPUT)

        # Test for creating an invalid intervention with an empty string
        response = self.client.post(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "2.00, 3.222",
                "videos": ["Video url"],
                "images": "images urls",
                "title": "this road is bad",
                "comment": "  "
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_EMPTY_STRING)

    def test_get_interventions(self):
        """unit test for getting all interventions"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_intervention(self):
        """unit tests for getting an inintervention by id"""
        # Test get intervention with available id
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_INTERVENTIONS + "/1",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Test get intervention with with id not available
        response = self.client.get(
            URL_INTERVENTIONS + "/19",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_NOT_FOUND)

    def test_update_intervention(self):
        """unit tests for updating the location of an intervention"""
        new_location = {"location": "1.500, 0.3000"}
        jwt_token = json.loads(self.login_response.data)["access_token"]

        # Test update intervention with wrong url
        response = self.client.patch(
            URL_INTERVENTIONS + "/4/wrong",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

        # Test update intervention with unavailable id
        response = self.client.patch(
            URL_INTERVENTIONS + "/4/location",
            data=json.dumps(new_location),
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_NOT_FOUND)

        # Test update intervention with the right id
        response = self.client.patch(
            URL_INTERVENTIONS + "/1/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(
                {"location": "1.500, 0.3000"}),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_UPDATE_SUCCESS)

        # Test update intervention with empty string
        new_location = {"location": " "}
        response = self.client.patch(
            URL_INTERVENTIONS + "/1/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_EMPTY_STRING)

        # Test update intervention with wrong data type
        new_location = {"location": 67}
        response = self.client.patch(
            URL_INTERVENTIONS + "/1/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_INVALID_INCIDENT_INPUT)

    def test_update_intervention_status(self):
        """unit test for uodating the status of an intervention incident"""
        # Test update intervention status by admin
        new_status = {"status": "resolved"}
        admin_login_response = self.client.post(
            URL_LOGIN, data=json.dumps({
                "username": "edward",
                "password": "i@mG8t##"
            }),
            content_type="application/json"
        )
        jwt_token = json.loads(admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_INTERVENTIONS + "/1/status",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_status),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_STATUS_UPDATE_SUCCESS)

    def test_delete_intervention(self):
        """unit tests for deleting an instance"""
        # Test delete intervention with unavailable id
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.delete(
            URL_INTERVENTIONS + "/3",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_NOT_FOUND)

        # Test delete intervention with available id
        response = self.client.delete(
            URL_INTERVENTIONS + "/2",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_DELETE_SUCCESS)
