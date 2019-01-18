"""module including unit testing class for some of the
 intervention incident fields some of the intervention
 incident are covered by the unit tests for the redflags"""

import unittest

from flask import json

from app import create_app
from app.utilitiez.static_strings import (
    URL_LOGIN,
    URL_REGISTER,
    URL_INTERVENTIONS,

    RESP_SUCCESS_MSG_CREATE_INCIDENT,
    RESP_SUCCESS_MSG_INCIDENT_UPDATE,
    RESP_SUCCESS_MSG_INCIDENT_DELETE,
    RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE,

    RESP_ERROR_MSG_POST_INCIDENT_WRONG_DATA,
    RESP_ERROR_MSG_UDATE_WRONG_LOCATION,
    RESP_ERROR_MSG_INCIDENT_NOT_FOUND,
    RESP_ERROR_MSG_INCIDENT_DUPLICATE,
    RESP_ERROR_MSG_EMPTY_STRING
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
            "othernames": "eddy",
            "email": "dall@bolon.com",
            "phonenumber": "0775961753",
            "username": "dallkased",
            "password": "ABd1234@1"
        }
        # get list of interventions before logging in
        response = self.client.get(
            URL_INTERVENTIONS,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        self.client.post(URL_REGISTER, data=json.dumps(test_user),
                         content_type="application/json")
        self.login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "dallkased",
            "password": "ABd1234@1"
        }), content_type="application/json")

        jwt_token = json.loads(self.login_response.data)["access_token"]

        # get list of interventions after logging in
        response = self.client.get(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # intervention to ensure that the list is not empty when one item is
        #  deleted during testing for deleting
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

    def test_create_intervention(self):
        """Test for creating a valid intervention"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
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
                         RESP_SUCCESS_MSG_CREATE_INCIDENT)
    def test_create_duplicate(self):
        """Test for creating a duplicate intervention"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
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
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INCIDENT_DUPLICATE)

    def test_create_lessattributes(self):
        """Test for creating an invalid intervention missing one required parameter"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
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
                         RESP_ERROR_MSG_POST_INCIDENT_WRONG_DATA)

    def test_create_moreattributes(self):
        """Test for creating an invalid intervention with more parameters than needed"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
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
                         RESP_ERROR_MSG_POST_INCIDENT_WRONG_DATA)

    def test_create_stringvideos(self):
        """Test for creating an invalid intervention with string of vidoes instead of list"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
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
                         RESP_ERROR_MSG_POST_INCIDENT_WRONG_DATA)

    def test_create_emptystring(self):
        """Test for creating an invalid intervention with an empty string"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
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
                         RESP_ERROR_MSG_EMPTY_STRING)

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
        """ Test get intervention with available id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_INTERVENTIONS + "/1",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        
    def test_get_intervention_noid(self):
        """Test get intervention with with id not available"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_INTERVENTIONS + "/19",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_noid(self):
        """Test update intervention with unavailable id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        new_location = {"location": "1.500, 0.3000"}
        response = self.client.patch(
            URL_INTERVENTIONS + "/4/location",
            data=json.dumps(new_location),
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_intervention(self):
        """Test update intervention with the right id"""
        new_location = {"location": "1.500, 0.3000"}
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_INTERVENTIONS + "/1/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_UPDATE)

    def test_update_wrongurl(self):
        """Test update intervention with wrong url"""  
        jwt_token = json.loads(self.login_response.data)["access_token"]
        new_location = {"location": "1.500, 0.3000"}
        response = self.client.patch(
            URL_INTERVENTIONS + "/4/wrong",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_update_emptystring(self):
        """Test update intervention with empty string"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
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
                         RESP_ERROR_MSG_EMPTY_STRING)

    def test_update_wrongtype(self):
        """Test update intervention with wrong data type"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
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
                         RESP_ERROR_MSG_UDATE_WRONG_LOCATION)

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
                         RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE)

    def test_delete_intervention_noid(self):
        """Test delete intervention with unavailable id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.delete(
            URL_INTERVENTIONS + "/3",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_delete_intervention_success(self):
        """Test delete intervention with available id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.delete(
            URL_INTERVENTIONS + "/2",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_DELETE)
