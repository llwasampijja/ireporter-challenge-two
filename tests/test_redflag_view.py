"""module including unit tests covering the red-flags and the interviews"""

import unittest

from flask import json

from databases.ireporter_db import IreporterDb
from databases.database_helper import DatabaseHelper
from tests.common_test import CommonTest

from app import create_app
from app.utilities.static_strings import (
    URL_REDFLAGS,
    URL_LOGIN,
    URL_REGISTER,

    EXPIRED_TOKEN,

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
    RESP_ERROR_MSG_INVALID_LIST_TYPE,
    RESP_ERROR_MSG_INVALID_LOCATION,
    RESP_ERROR_MSG_INVALID_INCIDENT,
    RESP_ERROR_MSG_USER_NOT_FOUND,
    RESP_ERROR_MSG_INVALID_EDIT_STRING_TYPE,
    RESP_ERROR_MSG_FORBIDDEN_INCIDENT_UPDATE,
    RESP_ERROR_MSG_BAD_REQUEST,
    RESP_ERROR_MSG_INCIDENT_DUPLICATE,
    RESP_ERROR_MSG_NOT_LOGGEDIN,
    RESP_ERROR_MSG_CONCERNED_CITZENS_ONLY,
    RESP_ERROR_MSG_ADMIN_ONLY,
    RESP_ERROR_MSG_SESSION_EXPIRED
)


class TestRedflagView(unittest.TestCase):
    """test class for red-flags extending the TestCase class from the unittest module"""

    common_test = CommonTest()
    # test_data = {
    #         "location": "90, 128",
    #         "videos": ["Video url"],
    #         "images": ["images urls"],
    #         "title": "Corrupt cop",
    #         "comment": "He was caught red handed"
    #     }

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app()
        self.client = self.app.test_client(self)

        self.ireporter_db = IreporterDb()
        self.database_helper = DatabaseHelper()
        self.ireporter_db.create_tables()
        self.database_helper.create_incident_types()
        self.database_helper.create_admin()

        test_user = {
            "firstname": "Dall",
            "lastname": "Kased",
            "othernames": "eddy",
            "email": "dall@bolon.com",
            "phonenumber": "0775961857",
            "username": "dallkased",
            "password": "ABd1234@1"
        }
        test_user2 = {
            "firstname": "Ann",
            "lastname": "Smith",
            "othernames": "ann",
            "email": "ann@bolon.com",
            "phonenumber": "0759617857",
            "username": "annsmith",
            "password": "ABd1234@1"
        }

        self.test_data = {
            "location": "90, 128",
            "videos": ["Video url"],
            "images": ["images urls"],
            "title": "Corrupt cop",
            "comment": "He was caught red handed"
        }

        self.test_data2 = {
            "location": "34, -115",
            "videos": ["Video url"],
            "images": ["images urls"],
            "title": "Cop taking a bribe",
            "comment": "He was caught red handed 2"
        }

        self.test_data3 = {
            "location": "34, -115",
            "videos": ["Video url"],
            "images": ["images urls"],
            "title": "Cop taking a bribe",
            "comment": "He was caught red handed 1"
        }

        self.client.post(
            URL_REGISTER,
            data=json.dumps(test_user2),
            content_type="application/json"
        )
        self.client.post(
            URL_REGISTER,
            data=json.dumps(test_user),
            content_type="application/json"
        )
        self.login_response = self.client.post(
            URL_LOGIN,
            data=json.dumps({
                "username": "dallkased",
                "password": "ABd1234@1"
            }),
            content_type="application/json"
        )

        # get redflags after logging in
        self.admin_jwt_token = self.common_test.admin_jwt_token()
        self.jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + self.jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        # post a redflag to ensure that the list is not empty when one
        # item is deleted during testing for deleting
        self.common_test.response_post_incident(
            URL_REDFLAGS, self.test_data3, self.jwt_token
        )
        self.common_test.response_post_incident(
            URL_REDFLAGS, self.test_data2, self.jwt_token
        )

    def tearDown(self):
        self.ireporter_db = IreporterDb()
        self.ireporter_db.drop_tables()

    def test_create_redflag_success(self):
        """unit test for creating redflag successfully"""     
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"), RESP_SUCCESS_MSG_CREATE_INCIDENT)

    def test_create_redflag_less(self):
        """Test for creating an invalid red-flag missing one required parameter"""
        self.test_data.pop("comment")
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_INVALID_INCIDENT)

    def test_create_redflag_more(self):
        """Test for creating an invalid red-flag with more parameters than needed"""
        self.test_data.update({"created_by": "jonmark"})
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_INVALID_INCIDENT)

    def test_create_redflag_videosstring(self):    
        """Test for creating an invalid red-flag with string of vidoes instead of list"""
        self.test_data.update({"images": "jonmark"})
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_INVALID_LIST_TYPE)

    def test_create_redflag_emptystring(self):    
        """Test for creating an invalid red-flag with an empty string"""
        self.test_data.update({"title": "  "})
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_EMPTY_STRING)

    def test_create_redflag_invalid_string_type(self):    
        """Test for creating an invalid red-flag with a non string type title"""
        self.test_data.update({"title": 878})
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_INVALID_STRING_TYPE)

    def test_create_redflag_onecoordinate(self):     
        """test add redflag with location with only one coordinate"""
        self.test_data.update({"location": "90"})
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_INVALID_LOCATION)

    def test_create_redflag_outofrangecoordinate(self):     
        """test add redflag with location with coordinate not in range"""
        self.test_data.update({"location": "180, 90"})
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_INVALID_LOCATION)

    def test_create_redflag_wrongcordinatetype(self):     
        """test add redflag with location with coordinate not a float"""
        self.test_data.update({"location": "0.342r, 143"})
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_INVALID_LOCATION)

    def test_get_redflags(self):
        """unit test for getting all redflags"""
        response = self.common_test.response_get_incidents(
            URL_REDFLAGS, self.jwt_token
        )
        self.assertEqual(response.status_code, 200)

    def test_get_redflag(self):
        """Test get redflag with available id"""
        response = self.common_test.response_get_incident(
            URL_REDFLAGS, 1, self.jwt_token
        )
        self.assertEqual(response.status_code, 200)

    def test_get_redflag_noid(self):
        """Test get redflag with with id not available"""
        response = self.common_test.response_get_incident(
            URL_REDFLAGS, 3435, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_redflag_wrongurl(self):
        """Test update redflag with wrong url"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "wrong", {"location": "1.500, 0.3000"}, self.jwt_token
        )
        self.assertEqual(response.status_code, 404)

    def test_update_redflag_noid(self):
        """Test update redflag with unavailable id"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 2000, "location", {"location": "1.500, 0.3000"}, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_redflag_emptystring(self):
        """Test update redflag with empty string"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 2, "location", {"location": "  "}, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_EMPTY_STRING)

    def test_update_redflag_location_wrongtype(self):
        """Test update redflag with the wrong data type"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 2, "location", {"location": 334}, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INVALID_EDIT_STRING_TYPE)

    def test_update_redflag_location_noncreater(self):
        """test update redflag which one never created"""
        jwt_token = self.common_test.nonadmin_jwt_token()
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "location", {"location": "1.500, 0.3000"}, jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_UNAUTHORIZED_EDIT)

    def test_update_redflag_location_nonpending(self):
        """test updated red-flag whose status isnt equal to
         'pending investigation'"""
        self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "status", {"status": "resolved"}, self.admin_jwt_token
        )
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "location", {"location": "1.500, 0.3000"}, self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_UNAUTHORIZED_EDIT)

    def test_update_redflag_location_morefields(self):
        """test update red-flag with fields other than location"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "location", {"location": "0.3000","title": "no a chance"}, self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_UNACCEPTABLE_INPUT)

    def test_update_redflag_location_success(self):
        """Test update redflag with the right id"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "location", {"location": "1.500, 0.3000"}, self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_UPDATE)

    def test_update_redflag_location_wrong_data(self):
        """Test update redflag with the right id"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "location", {"location": "0.3000"}, self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_UDATE_WRONG_LOCATION)

    def test_update_redflag_status_nonadmin(self):
        """test update red-flag's status as a concerned citzen"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "status", {"status": "rejected"}, self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_ADMIN_ONLY)

    def test_update_redflag_comment_asuccess(self):
        """unit test for updating the redflag's comment successfully"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "comment", {"comment": "Every one say that man taking money from a poor shop keeper"},
            self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_UPDATE)

    def test_update_redflag_comment_duplicate(self):
        """unit test for updating the redflag's comment as a duplicated"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "comment", {"comment": "He was caught red handed 1"}, self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_DUPLICATE)

    def test_update_redflag_comment_empty(self):
        """unit test for updating the redflag's comment successfully"""
        response = self.client.patch(
            URL_REDFLAGS + "/3/comment",
            headers=dict(Authorization='Bearer ' + self.jwt_token),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_BAD_REQUEST)

    def test_update_redflag_comment_wrong_route(self):
        """unit test for updating the redflag's comment successfully"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 3, "comment", {"location": "1.500, 0.3000"}, self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_FORBIDDEN_INCIDENT_UPDATE)

    def test_delete_redflag_noid(self):
        """Test delete red-flag with unavailable id"""
        response = self.common_test.response_delete_incident(
            URL_REDFLAGS, 300, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("error"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_delete_redflag(self):
        """Test delete red-flag with unavailable id"""
        response = self.common_test.response_delete_incident(
            URL_REDFLAGS, 2, self.jwt_token
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("message"), RESP_SUCCESS_MSG_INCIDENT_DELETE)

    def test_delete_redflag_nonauthor(self):
        """Test delete redflag which one never created"""
        non_admin_token = self.common_test.nonadmin_jwt_token()
        response = self.common_test.response_delete_incident(
            URL_REDFLAGS, 1, non_admin_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"),
                         RESP_EEROR_MSG_UNAUTHORIZED_DELETE)

    def test_delete_redflag_nonpending(self):
        """Test delete redflag which whose status is nolonger pending investigation"""
        self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "status", {"status":"resolved"}, self.admin_jwt_token
        )
        response = self.common_test.response_delete_incident(
            URL_REDFLAGS, 1, self.jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"),
                         RESP_EEROR_MSG_UNAUTHORIZED_DELETE)

    def test_update_redflag_status(self):
        """Test update status of redflag by admin"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "status", {"status": "rejected"}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE)

    def test_update_redflag_status_morefields(self):
        """test update red-flag with more than just the status as an admin"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 2, "status", {"status": "resolved", "comment": "You are"}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_ADMIN_NO_RIGHTS)

    def test_update_status_none(self):
        """test update the status of an incident which doesn't exist"""
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 300, "status", {"status": "resolved"}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_status_wrong(self):
        """test update redflag with a wrong status value"""    
        response = self.common_test.response_patch_incident(
            URL_REDFLAGS, 1, "status", {"status": "wrong value"}, self.admin_jwt_token
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_UPDATE_STATUS)

        
    def test_admin_create_redflag(self):
        """test try to create an incident as an admin"""
        response = response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, self.admin_jwt_token)
        response_data = json.loads(response.data.decode())
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_CONCERNED_CITZENS_ONLY)

    def test_acess_protected_route(self):
        response = self.client.post(
            URL_REDFLAGS,
            data=json.dumps(self.test_data),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("error"),
                         RESP_ERROR_MSG_NOT_LOGGEDIN)

    def test_use_expired_token(self):
        """unit test for creating redflag successfully"""     
        jwt_token = EXPIRED_TOKEN     
        response = self.common_test.response_post_incident(URL_REDFLAGS, self.test_data, jwt_token)
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("error"), RESP_ERROR_MSG_SESSION_EXPIRED)
