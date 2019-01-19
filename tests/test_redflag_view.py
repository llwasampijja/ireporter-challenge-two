"""module including unit tests covering the red-flags and the interviews"""

import unittest

from flask import json

from app import create_app
from app.utilitiez.static_strings import (
    URL_REDFLAGS,
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
    RESP_ERROR_MSG_INVALID_LIST_TYPE,
    RESP_ERROR_MSG_INVALID_LOCATION,
    RESP_ERROR_MSG_INVALID_INCIDENT,
    RESP_ERROR_MSG_USER_NOT_FOUND
)


class TestRedflagView(unittest.TestCase):
    """test class for red-flags extending the TestCase class from the unittest module"""

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app()
        self.client = self.app.test_client(self)
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

        # get redflags before logging in
        response = self.client.get(
            URL_REDFLAGS, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data).get("message"), None)

        # get redflags after logging in
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        # post a redflag to ensure that the list is not empty when one
        # item is deleted during testing for deleting
        self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "34, -115",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "Cop taking a bribe",
                "comment": "He was caught red handed 1"
            }),
            content_type="application/json"
        )
        self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "34, -115",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "Cop taking a bribe",
                "comment": "He was caught red handed 2"
            }),
            content_type="application/json"
        )

    def test_create_redflag_success(self):
        """unit test for creating redflag successfully"""     
        jwt_token = json.loads(self.login_response.data)["access_token"]

        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "90, 128",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "Corrupt cop",
                "comment": "He was caught red handed"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"), RESP_SUCCESS_MSG_CREATE_INCIDENT)

    def test_create_redflag_less(self):
        """Test for creating an invalid red-flag missing one required parameter"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "0.342, 143",
                "videos": ["Video url"],
                "images": ["images urls"],
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INVALID_INCIDENT)

    def test_create_redflag_more(self):
        """Test for creating an invalid red-flag with more parameters than needed"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "created_by": "Jon Mark",
                "location": "0.342, 143",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "Cop taking a bribe",
                "comment": "He was caught red handed y"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INVALID_INCIDENT)

    def test_create_redflag_videosstring(self):    
        """Test for creating an invalid red-flag with string of vidoes instead of list"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "0.342, 143",
                "videos": ["Video url"],
                "images": "images urls",
                "title": "Cop taking a bribe",
                "comment": "He was caught red handed k"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INVALID_LIST_TYPE)

    def test_create_redflag_emptystring(self):    
        """Test for creating an invalid red-flag with an empty string"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "0.342, 143",
                "videos": ["Video url"],
                "images": "images urls",
                "title": "  ",
                "comment": "He was caught red handed empty string"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_EMPTY_STRING)

    def test_create_redflag_invalid_string_type(self):    
        """Test for creating an invalid red-flag with an empty string"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "0.342, 143",
                "videos": ["Video url"],
                "images": "images urls",
                "title": 67,
                "comment": "He was caught red handed empty string"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INVALID_STRING_TYPE)

    def test_create_redflag_onecoordinate(self):     
        """test add redflag with location with only one coordinate"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "90",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "Corrupt cop",
                "comment": "He was caught red handed"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), RESP_ERROR_MSG_INVALID_LOCATION)

    def test_create_redflag_outofrangecoordinate(self):     
        """test add redflag with location with coordinate not in range"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "180, 180",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "Corrupt cop",
                "comment": "He was caught red handed"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), RESP_ERROR_MSG_INVALID_LOCATION)

    def test_create_redflag_wrongcordinatetype(self):     
        """test add redflag with location with coordinate not in range"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "0.342r, 143",
                "videos": ["Video url"],
                "images": ["images urls"],
                "title": "Corrupt cop",
                "comment": "He was caught red handed"
            }),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), RESP_ERROR_MSG_INVALID_LOCATION)

    def test_get_redflags(self):
        """unit test for getting all redflags"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_redflag(self):
        """Test get redflag with available id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_REDFLAGS + "/1",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_redflag_noid(self):
        """Test get redflag with with id not available"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_REDFLAGS + "/3435",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_redflag_wrongurl(self):
        """Test update redflag with wrong url"""
        new_location = {"location": "1.500, 0.3000"}
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/4/wrong",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_update_redflag_noid(self):
        """Test update redflag with unavailable id"""
        new_location = {"location": "1.500, 0.3000"}
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/4000/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_redflag_emptystring(self):
        """Test update redflag with empty string"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/2/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({"location": "  "}),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_EMPTY_STRING)

    def test_update_redflag_location_wrongtype(self):
        """Test update redflag with the wrong data type"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/2/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(
                {"location": 334}),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_UDATE_WRONG_LOCATION)

    def test_update_redflag_location_noncreater(self):
        """test update redflag which one never created"""
        self.test_login_response = self.client.post(
            URL_LOGIN,
            data=json.dumps({
                "username": "annsmith",
                "password": "ABd1234@1"
            }),
            content_type="application/json"
        )
        jwt_token = json.loads(self.test_login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/1/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "2.000, 0.400"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_UNAUTHORIZED_EDIT)

    def test_update_redflag_location_nonpending(self):
        """test updated red-flag whose status isnt equal to
         'pending investigation'"""
        self.test_admin_login_response = self.client.post(
            URL_LOGIN,
            data=json.dumps({
                "username": "edward",
                "password": "i@mG8t##"
            }),
            content_type="application/json"
        )
        admin_jwt_token = json.loads(self.test_admin_login_response.data)["access_token"]
        self.client.patch(
            URL_REDFLAGS + "/1/status",
            headers=dict(Authorization='Bearer ' + admin_jwt_token),
            data=json.dumps({"status":"resolved"}),
            content_type="application/json"
        )

        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/1/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(
                {"location": "1.500, 0.3000"}),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_UNAUTHORIZED_EDIT)

    def test_update_redflag_location_morefields(self):
        """test update red-flag with fields other than location"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/3/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "location": "1.500, 0.3000",
                "title": "no a chance"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_UNACCEPTABLE_INPUT)

    def test_update_redflag_location_success(self):
        """Test update redflag with the right id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/3/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(
                {"location": "1.500, 0.3000"}),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_UPDATE)

    def test_update_redflag_status_nonadmin(self):
        """test update red-flag's status as a concerned citzen"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/2/status",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "status": "rejected"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_UNAUTHORIZED_VIEW)

    def test_delete_redflag_noid(self):
        """Test delete red-flag with unavailable id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.delete(
            URL_REDFLAGS + "/300",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_delete_redflag(self):
        """Test delete red-flag with unavailable id"""
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.delete(
            URL_REDFLAGS + "/2",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("message"), RESP_SUCCESS_MSG_INCIDENT_DELETE)

    def test_delete_redflag_nonauthor(self):
        """Test delete redflag which one never created"""
        self.test_login_response = self.client.post(
            URL_LOGIN,
            data=json.dumps({
                "username": "annsmith",
                "password": "ABd1234@1"
            }),
            content_type="application/json"
        )
        jwt_token = json.loads(self.test_login_response.data)["access_token"]
        response = self.client.delete(
            URL_REDFLAGS + "/1",
            headers=dict(Authorization="Bearer " + jwt_token),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_EEROR_MSG_UNAUTHORIZED_DELETE)

    def test_delete_redflag_nonpending(self):
        """Test delete redflag which whose status is nolonger pending investigation"""
        self.test_admin_login_response = self.client.post(
            URL_LOGIN,
            data=json.dumps({
                "username": "edward",
                "password": "i@mG8t##"
            }),
            content_type="application/json"
        )
        admin_jwt_token = json.loads(self.test_admin_login_response.data)["access_token"]
        self.client.patch(
            URL_REDFLAGS + "/1/status",
            headers=dict(Authorization='Bearer ' + admin_jwt_token),
            data=json.dumps({"status":"resolved"}),
            content_type="application/json"
        )

        jwt_token = json.loads(self.login_response.data)["access_token"]   
        response = self.client.delete(
            URL_REDFLAGS + "/1",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_EEROR_MSG_UNAUTHORIZED_DELETE)

    def test_update_redflag_status(self):
        """Test update status of redflag by admin"""
        admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward",
            "password": "i@mG8t##"
        }), content_type="application/json")
        admin_jwt_token = json.loads(admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/3/status",
            headers=dict(Authorization='Bearer ' + admin_jwt_token),
            data=json.dumps({
                "status": "rejected"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data.get("message"),
                         RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE)

    def test_update_redflag_status_morefields(self):
        """test update red-flag with more than just the status as an admin"""
        admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward",
            "password": "i@mG8t##"
        }), content_type="application/json")
        admin_jwt_token = json.loads(admin_login_response.data)["access_token"]
       
        response = self.client.patch(
            URL_REDFLAGS + "/2/status",
            headers=dict(Authorization='Bearer ' + admin_jwt_token),
            data=json.dumps({
                "status": "rejected",
                "comment": "You are lieing, you will be arrested for trying\
                 to destroy the name of a good man"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_ADMIN_NO_RIGHTS)

    def test_update_status_none(self):
        """test update the status of an incident which doesn't exist"""
        admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward",
            "password": "i@mG8t##"
        }), content_type="application/json")
        admin_jwt_token = json.loads(admin_login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/300/status",
            headers=dict(Authorization='Bearer ' + admin_jwt_token),
            data=json.dumps({
                "status": "resolved"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("message"), RESP_ERROR_MSG_INCIDENT_NOT_FOUND)

    def test_update_status_wrong(self):
        """test update redflag with a wrong status value"""
        admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward",
            "password": "i@mG8t##"
        }), content_type="application/json")
        admin_jwt_token = json.loads(admin_login_response.data)["access_token"]
        
        response = self.client.patch(
            URL_REDFLAGS + "/1/status",
            headers=dict(Authorization="Bearer " + admin_jwt_token),
            data=json.dumps({
                "status": "wrong value"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_UPDATE_STATUS)

        
    def test_admin_create_redflag(self):
        """test try to create an incident as an admin"""
        admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward",
            "password": "i@mG8t##"
        }), content_type="application/json")
        admin_jwt_token = json.loads(admin_login_response.data)["access_token"]
        response = self.client.post(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + admin_jwt_token),
            data=json.dumps({
                "location": "0.00938, 2.46287",
                "videos": ["Video url"],
                "images": "images urls",
                "title": "Cop taking a bribe",
                "comment": "He was caught red handed admin post"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_ERROR_MSG_UNAUTHORIZED_VIEW)
