"""module including unit tests covering the red-flags and the interviews"""

import unittest

from flask import json

from app import create_app
from app.utilitiez.static_strings import (
    RESP_UNAUTHORIZED_VIEW,
    RESP_INCIDENT_WROND_STATUS,
    RESP_USER_STATUS_NORIGHTS,
    RESP_INCIDENT_STATUS_UPDATE_SUCCESS,
    RESP_UNAUTHORIZED_DELETE,
    RESP_INCIDENT_DELETE_SUCCESS,
    RESP_INCIDENT_UPDATE_SUCCESS,
    RESP_ADMIN_ONLY,
    RESP_INCIDENT_NOT_FOUND,
    URL_REDFLAGS,
    RESP_INVALID_INCIDENT_INPUT,
    RESP_UNAUTHORIZED_EDIT,
    URL_LOGIN, URL_REGISTER,
    RESP_EMPTY_STRING,
    RESP_CREATE_INCIDENT_SUCCESS)


class TestRedflagView(unittest.TestCase):
    """test class for red-flags extending the TestCase class from the unittest module"""

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app()
        self.client = self.app.test_client(self)
        test_user = {
            "firstname": "Dall",
            "lastname": "Kased",
            "othernames": "eddy2",
            "email": "dall@bolon.com",
            "phonenumber": "0775961857",
            "username": "dallkased",
            "password": "ABd1234@1"
        }
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

        # item is deleted during testing for deleting
        # jwt_token = json.loads(self.login_response.data)["access_token"]
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

    def test_create_redflag(self):
        """unit tests for creating redflags"""
        # redflag to ensure that the list is not empty when one
        # # item is deleted during testing for deleting
        jwt_token = json.loads(self.login_response.data)["access_token"]
        # self.client.post(
        #     URL_REDFLAGS,
        #     headers=dict(Authorization='Bearer ' + jwt_token),
        #     data=json.dumps({
        #         "location": "34, -115",
        #         "videos": ["Video url"],
        #         "images": ["images urls"],
        #         "title": "Cop taking a bribe",
        #         "comment": "He was caught red handed 1"
        #     }),
        #     content_type="application/json"
        # )

        # Test for creating a valid red-flag
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
        self.assertEqual(data.get("message"), RESP_CREATE_INCIDENT_SUCCESS)

        # Test for creating an invalid red-flag missing one required parameter
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
                         RESP_INVALID_INCIDENT_INPUT)

        # Test for creating an invalid red-flag with more parameters than needed
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
                         RESP_INVALID_INCIDENT_INPUT)

        # Test for creating an invalid red-flag with string of vidoes instead of list
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
                         RESP_INVALID_INCIDENT_INPUT)

        # Test for creating an invalid red-flag with an empty string
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
                         RESP_EMPTY_STRING)

        # test add redflag with location with only one coordinate
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
        self.assertEqual(data.get("message"), RESP_INVALID_INCIDENT_INPUT)

        # test add redflag with location with coordinate not in range
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
        self.assertEqual(data.get("message"), RESP_INVALID_INCIDENT_INPUT)

        # test add redflag with location with coordinate not in range
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
        self.assertEqual(data.get("message"), RESP_INVALID_INCIDENT_INPUT)

    def test_get_redflags(self):
        """unit tests for getting all redflags"""
        # test get all redflags
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # test get all redflags when you are not not an admin or concerned citzen
        noone_login_response = self.client.post(
            URL_LOGIN, data=json.dumps({
                "username": "jetli",
                "password": "i@mG8t##"
            }),
            content_type="application/json"
        )
        noone_jwt_token = json.loads(noone_login_response.data)["access_token"]
        response = self.client.get(
            URL_REDFLAGS,
            headers=dict(Authorization='Bearer ' + noone_jwt_token),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("message"),
                         RESP_UNAUTHORIZED_VIEW)

    def test_get_redflag(self):
        """unit tests for getting red-flags"""
        # Test get redflag with available id
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.get(
            URL_REDFLAGS + "/2",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # Test get redflag with with id not available
        response = self.client.get(
            URL_REDFLAGS + "/3435",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_NOT_FOUND)

    def test_update_redflag(self):
        """unit tests for updating a redflag's location"""
        # Test update redflag with wrong url
        new_location = {"location": "1.500, 0.3000"}
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.patch(
            URL_REDFLAGS + "/4/wrong",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

        # Test update redflag with unavailable id
        response = self.client.patch(
            URL_REDFLAGS + "/4000/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(new_location),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_NOT_FOUND)

        # Test update redflag with empty string
        response = self.client.patch(
            URL_REDFLAGS + "/2/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({"location": "  "}),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"),
                         RESP_EMPTY_STRING)

        # Test update redflag with the wrong data type
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
                         RESP_INVALID_INCIDENT_INPUT)

        # test update redflag which one never created
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
                         RESP_UNAUTHORIZED_EDIT)

        # test updated red-flag whose status isnt equal to
        # 'pending investigation'
        response = self.client.patch(
            URL_REDFLAGS + "/2/location",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(
                {"location": "1.500, 0.3000"}),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_UNAUTHORIZED_EDIT)

        # test update red-flag with fields other than location'
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
                         RESP_INVALID_INCIDENT_INPUT)

        # Test update redflag with the right id
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
                         RESP_INCIDENT_UPDATE_SUCCESS)

        # test update red-flag's status as a concerned citzen
        response = self.client.patch(
            URL_REDFLAGS + "/2/status",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps({
                "status": "rejected"
            }),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("message"),
                         RESP_ADMIN_ONLY)

    def test_delete_redflag(self):
        """unit tests for deleting a red-flag"""
        # Test delete red-flag with unavailable id
        jwt_token = json.loads(self.login_response.data)["access_token"]
        response = self.client.delete(
            URL_REDFLAGS + "/300",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"),
                         RESP_INCIDENT_NOT_FOUND)

        # Test delete red-flag with unavailable id
        response = self.client.delete(
            URL_REDFLAGS + "/4",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data.get("message"), RESP_INCIDENT_DELETE_SUCCESS)

        # test delete a red-flag by a user who didn't create it
        response = self.client.delete(
            URL_REDFLAGS + "/1",
            headers=dict(Authorization="Bearer " + jwt_token),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_UNAUTHORIZED_DELETE)

        # test delete red-flag whose status isnt equal to
        # 'pending investigation'
        response = self.client.delete(
            URL_REDFLAGS + "/2",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data.get("message"),
                         RESP_UNAUTHORIZED_DELETE)

    def test_update_redflag_status(self):
        """unit tests for updating status of redflag"""
        # Test update status of redflag by admin
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
                         RESP_INCIDENT_STATUS_UPDATE_SUCCESS)

        # test update red-flag with more than just the status as an admin
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
                         RESP_USER_STATUS_NORIGHTS)

        # test update the status of an incident which doesn't exist
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
        self.assertEqual(response_data.get("message"), RESP_INCIDENT_NOT_FOUND)

        # test update redflag with a wrong status value
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
                         RESP_INCIDENT_WROND_STATUS)

        # test try to create an incident as an admin
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
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data.get("message"),
                         RESP_UNAUTHORIZED_VIEW)
