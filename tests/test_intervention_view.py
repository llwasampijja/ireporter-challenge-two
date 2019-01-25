"""module including unit testing class for some of the
 intervention incident fields some of the intervention
 incident are covered by the unit tests for the redflags"""

import unittest
import hashlib
import datetime

from flask import json

from databases.ireporter_db import IreporterDb
from databases.database_helper import DatabaseHelper

from app import create_app
from app.utilities.static_strings import (
    URL_INTERVENTIONS,
    URL_LOGIN,
    URL_REGISTER,

    RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE,
    RESP_SUCCESS_MSG_INCIDENT_DELETE,
    RESP_SUCCESS_MSG_INCIDENT_UPDATE,
    RESP_SUCCESS_MSG_CREATE_INCIDENT,

    RESP_ERROR_MSG_UNAUTHORIZED_EDIT,
    RESP_ERROR_MSG_UNAUTHORIZED_VIEW,
    RESP_ERROR_MSG_USER_STATUS_NORIGHTS,
    RESP_EEROR_MSG_UNAUTHORIZED_DELETE,
    RESP_ERROR_MSG_UNACCEPTABLE_INPUT,
    RESP_ERROR_MSG_UDATE_WRONG_LOCATION,
    RESP_ERROR_MSG_UPDATE_STATUS,
    RESP_ERROR_MSG_INCIDENT_NOT_FOUND,
    RESP_ERROR_MSG_EMPTY_STRING,
    RESP_ERROR_MSG_ADMIN_NO_RIGHTS,
    RESP_ERROR_MSG_INVALID_STRING_TYPE,
    RESP_ERROR_MSG_INVALID_LOCATION,
    RESP_ERROR_MSG_INVALID_INCIDENT,
    RESP_ERROR_MSG_USER_NOT_FOUND,
    RESP_ERROR_MSG_INVALID_EDIT_STRING_TYPE,
    RESP_ERROR_MSG_FORBIDDEN_INCIDENT_UPDATE,
    RESP_ERROR_MSG_BAD_REQUEST,
    RESP_ERROR_MSG_INCIDENT_DUPLICATE,
    RESP_ERROR_MSG_INVALID_IMAGES,
    RESP_ERROR_MSG_INVALID_TITLE,
    RESP_ERROR_MSG_INVALID_COMMENT,
    RESP_ERROR_MSG_INVALID_LOCATION,
    RESP_ERROR_MSG_UDATE_WRONG_LOCATION,
    RESP_ERROR_MSG_INVALID_IMAGES
)


class TestInterventionView(unittest.TestCase):
    """unit testing class for intervention"""

    def setUp(self):
        """initializing method for every unit test"""
        
        self.app = create_app()
        self.client = self.app.test_client(self)

        self.ireporter_db = IreporterDb()
        self.database_helper = DatabaseHelper()
        self.ireporter_db.drop_tables()
        self.ireporter_db.create_tables()
        self.database_helper.create_incident_types()

        test_user = {
            "firstname": "Dall",
            "lastname": "Kased",
            "othernames": "eddy",
            "email": "dall@bolon.com",
            "phonenumber": "0775961753",
            "username": "dallkased",
            "password": "ABd1234@1"
        }

        self.database_helper.create_admin()

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
        self.assertEqual(response.status_code, 400)

        # add intervention to ensure that the list is not empty when one item is
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

    def tearDown(self):
        self.ireporter_db.drop_tables()

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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
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
                "images": ["image.jpg"],
                "comment": "School is bad"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INVALID_INCIDENT)

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
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INVALID_INCIDENT)

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
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INVALID_IMAGES)

    # def test_create_emptystring(self):
    #     """Test for creating an invalid intervention with an empty string"""
    #     jwt_token = json.loads(self.login_response.data)["access_token"]
    #     response = self.client.post(
    #         URL_INTERVENTIONS,
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps({
    #             "location": "2.00, 3.222",
    #             "videos": ["Video url"],
    #             "images": ["images urls"],
    #             "title": "this road is bad",
    #             "comment": "  "
    #         }),
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(data.get("error"),
    #                      RESP_ERROR_MSG_EMPTY_STRING)

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
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    # def test_update_noid(self):
    #     """Test update intervention with unavailable id"""
    #     jwt_token = json.loads(self.login_response.data)["access_token"]
    #     new_location = {"location": "1.500, 0.3000"}
    #     response = self.client.patch(
    #         URL_INTERVENTIONS + "/40/location",
    #         data=json.dumps(new_location),
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data.get("error"),
    #                      RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    # def test_update_intervention(self):
    #     """Test update intervention with the right id"""
    #     new_location = {"location": "1.500, 0.3000"}
    #     jwt_token = json.loads(self.login_response.data)["access_token"]
    #     response = self.client.patch(
    #         URL_INTERVENTIONS + "/1/location",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps(new_location),
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data.get("message"),
    #                      RESP_SUCCESS_MSG_INCIDENT_UPDATE)

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
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_UDATE_WRONG_LOCATION)

    # def test_update_wrongtype(self):
    #     """Test update intervention with wrong data type"""
    #     jwt_token = json.loads(self.login_response.data)["access_token"]
    #     new_location = {"location": 67}
    #     response = self.client.patch(
    #         URL_INTERVENTIONS + "/1/location",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps(new_location),
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(data.get("error"),
    #                      RESP_ERROR_MSG_INVALID_EDIT_STRING_TYPE)

    # def test_update_intervention_comment_success(self):
    #     """Test update intervention's comment with the right id"""
    #     new_location = {"comment": "1.500, 0.3000"}
    #     jwt_token = json.loads(self.login_response.data)["access_token"]
    #     response = self.client.patch(
    #         URL_INTERVENTIONS + "/1/comment",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps(new_location),
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data.get("message"),
    #                      RESP_SUCCESS_MSG_INCIDENT_UPDATE)

    # def test_update_intervention_status(self):
    #     """Test update intervention status by admin"""
    #     new_status = {"status": "resolved"}
    #     admin_login_response = self.client.post(
    #         URL_LOGIN, data=json.dumps({
    #             "username": "edward",
    #             "password": "i@mG8t##"
    #         }),
    #         content_type="application/json"
    #     )
    #     jwt_token = json.loads(admin_login_response.data)["access_token"]
    #     response = self.client.patch(
    #         URL_INTERVENTIONS + "/1/status",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         data=json.dumps(new_status),
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(data.get("message"),
    #                      RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE)

    # def test_delete_intervention_noid(self):
    #     """Test delete intervention with unavailable id"""
    #     jwt_token = json.loads(self.login_response.data)["access_token"]
    #     response = self.client.delete(
    #         URL_INTERVENTIONS + "/300",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data.get("error"),
    #                      RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    # def test_delete_intervention_success(self):
    #     """Test delete intervention with available id"""
    #     jwt_token = json.loads(self.login_response.data)["access_token"]
    #     response = self.client.delete(
    #         URL_INTERVENTIONS + "/1",
    #         headers=dict(Authorization='Bearer ' + jwt_token),
    #         content_type="application/json"
    #     )
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data.get("message"),
    #                      RESP_SUCCESS_MSG_INCIDENT_DELETE)
