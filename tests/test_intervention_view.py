"""module including unit testing class for some of the
 intervention incident fields some of the intervention
 incident are covered by the unit tests for the redflags"""

import unittest
import hashlib
import datetime

from flask import json

from databases.ireporter_db import IreporterDb
from databases.database_helper import DatabaseHelper
from tests.common_test import CommonTest

from app import create_app
from app.utilities.static_strings import (
    URL_LOGIN,
    URL_REGISTER,
    URL_INTERVENTIONS,

    RESP_SUCCESS_MSG_CREATE_INCIDENT,
    RESP_SUCCESS_MSG_INCIDENT_UPDATE,
    RESP_SUCCESS_MSG_INCIDENT_DELETE,
    RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE,

    RESP_ERROR_MSG_UDATE_WRONG_LOCATION,
    RESP_ERROR_MSG_INCIDENT_NOT_FOUND,
    RESP_ERROR_MSG_INCIDENT_DUPLICATE,
    RESP_ERROR_MSG_EMPTY_STRING,
    RESP_ERROR_MSG_INVALID_STRING_TYPE,
    RESP_ERROR_MSG_INVALID_LIST_TYPE,
    RESP_ERROR_MSG_INVALID_LOCATION,
    RESP_ERROR_MSG_INVALID_INCIDENT,
    RESP_ERROR_MSG_USER_NOT_FOUND,
    RESP_ERROR_MSG_INVALID_EDIT_STRING_TYPE
)


class TestInterventionView(unittest.TestCase):
    """unit testing class for intervention"""

    common_test = CommonTest()

    def setUp(self):
        """initializing method for every unit test"""
        
        self.app = create_app()
        self.client = self.app.test_client(self)

        self.ireporter_db = IreporterDb()
        self.database_helper = DatabaseHelper()
        self.ireporter_db.create_tables()
        self.database_helper.create_incident_types()

        self.test_data1 = {
            "location": "2.00, 3.222",
            "videos": ["Video url"],
            "images": ["images urls"],
            "title": "bad hospital",
            "comment": "The road has very bif potholes"
        }

        self.database_helper.create_admin()

        # get list of interventions before logging in
        response = self.client.get(
            URL_INTERVENTIONS,
            content_type="application/json"
        )

        self.jwt_token = self.common_test.nonadmin_author_token()
        self.admin_jwt_token = self.common_test.admin_jwt_token()

        # get list of interventions after logging in
        response = self.client.get(
            URL_INTERVENTIONS,
            headers=dict(Authorization='Bearer ' + self.jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # add intervention to ensure that the list is not empty when one item is
        #  deleted during testing for deleting
        self.common_test.response_post_incident(
            URL_INTERVENTIONS, self.test_data1, self.jwt_token
        )

    def tearDown(self):
        self.ireporter_db = IreporterDb()
        self.ireporter_db.drop_tables()

    def test_create_intervention(self):
        """Test for creating a valid intervention"""
        self.test_data1.update({"comment": "This Hospital's sanitation is really worrying"})
        response = self.common_test.response_post_incident(
            URL_INTERVENTIONS, self.test_data1, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_SUCCESS_MSG_CREATE_INCIDENT)

    def test_create_duplicate(self):
        """Test for creating a duplicate intervention"""
        response = self.common_test.response_post_incident(
            URL_INTERVENTIONS, self.test_data1, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_DUPLICATE)

    def test_create_lessattributes(self):
        """Test for creating an invalid intervention missing one required parameter"""
        self.test_data1.pop("title")
        response = self.common_test.response_post_incident(
            URL_INTERVENTIONS, self.test_data1, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INVALID_INCIDENT)

    def test_create_moreattributes(self):
        """Test for creating an invalid intervention with more parameters than needed"""
        self.test_data1.update({"created_by":  "JonMark"})
        response = self.common_test.response_post_incident(
            URL_INTERVENTIONS, self.test_data1, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INVALID_INCIDENT)

    def test_create_stringvideos(self):
        """Test for creating an invalid intervention with string of vidoes instead of list"""
        self.test_data1.update({"videos":  "JonMark"})
        response = self.common_test.response_post_incident(
            URL_INTERVENTIONS, self.test_data1, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INVALID_LIST_TYPE)

    def test_create_emptystring(self):
        """Test for creating an invalid intervention with an empty string"""
        self.test_data1.update({"comment":  "  "})
        response = self.common_test.response_post_incident(
            URL_INTERVENTIONS, self.test_data1, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_EMPTY_STRING)

    def test_get_interventions(self):
        """unit test for getting all interventions"""
        response = self.common_test.response_get_incidents(
            URL_INTERVENTIONS, self.jwt_token
        )
        self.assertEqual(response.status_code, 200)

    def test_get_intervention(self):
        """ Test get intervention with available id"""
        response = self.common_test.response_get_incident(
            URL_INTERVENTIONS, 1, self.jwt_token
        )
        self.assertEqual(response.status_code, 200)

        
    def test_get_intervention_noid(self):
        """Test get intervention with with id not available"""
        response = self.common_test.response_get_incident(
            URL_INTERVENTIONS, 19990, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_noid(self):
        """Test update intervention with unavailable id"""
        response = self.common_test.response_patch_incident(
            URL_INTERVENTIONS, 233737, "location", {"location": "1.500, 0.3000"}, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_intervention(self):
        """Test update intervention with the right id"""
        response = self.common_test.response_patch_incident(
            URL_INTERVENTIONS, 1, "location", {"location": "1.500, 0.3000"}, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_UPDATE)

    def test_update_wrongurl(self):
        """Test update intervention with wrong url"""  
        response = self.common_test.response_patch_incident(
            URL_INTERVENTIONS, 1, "wrong", {"location": "1.500, 0.3000"}, self.jwt_token
        )
        self.assertEqual(response.status_code, 404)

    def test_update_emptystring(self):
        """Test update intervention with empty string"""
        response = self.common_test.response_patch_incident(
            URL_INTERVENTIONS, 233737, "location", {"location": "  "}, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_EMPTY_STRING)

    def test_update_wrongtype(self):
        """Test update intervention with wrong data type"""
        response = self.common_test.response_patch_incident(
            URL_INTERVENTIONS, 233737, "location", {"location": 67}, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INVALID_EDIT_STRING_TYPE)

    def test_update_intervention_comment_success(self):
        """Test update intervention's comment with the right id"""
        response = self.common_test.response_patch_incident(
            URL_INTERVENTIONS, 1, "comment", {"comment": "1.500, 0.3000"}, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_UPDATE)

    def test_update_intervention_status(self):
        """Test update intervention status by admin"""
        response = self.common_test.response_patch_incident(
            URL_INTERVENTIONS, 1, "status", {"status": "resolved"}, self.admin_jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE)

    def test_delete_intervention_noid(self):
        """Test delete intervention with unavailable id"""
        response = self.common_test.response_delete_incident(
            URL_INTERVENTIONS, 3009, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_delete_intervention_success(self):
        """Test delete intervention with available id"""
        response = self.common_test.response_delete_incident(
            URL_INTERVENTIONS, 1, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_DELETE)
