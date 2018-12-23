import unittest
from app.data.redflag_data import RedflagData
from app.controllers.redflag_controller import RedflagController
from app import create_app
from flask import Response, json


class TestRedflagView (unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client(self)
        
    def test_create_redflag(self):
        """redflag to ensure that the list is not empty when one item is deleted during testing for deleting"""
        self.client.post("api/v1/red-flags", data = json.dumps({
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "status":"Pending Investigation",
            "videos":["Video url"],
            "images":["images urls"],
            "comment":"He was caught red handed"
        }), content_type="application/json")

        """Test for creating a valid red-flag"""
        response = self.client.post("api/v1/red-flags", data = json.dumps({
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "status":"Pending Investigation",
            "videos":["Video url"],
            "images":["images urls"],
            "comment":"He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 202)
        self.assertEqual(data.get("message"), "Red-Flag created successifully")
   
        """Test for creating an invalid red-flag missing one required parameter"""
        response = self.client.post("api/v1/red-flags", data = json.dumps({
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "videos":["Video url"],
            "images":["images urls"],
            "comment":"He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Unaccepted datatype or Inavlid Redflag") 

   
        """Test for creating an invalid red-flag with more parameters than needed"""
        response = self.client.post("api/v1/red-flags", data = json.dumps({
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "videos":["Video url"],
            "images":["images urls"],
            "comment":"He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Unaccepted datatype or Inavlid Redflag")

        """Test for creating an invalid red-flag with string of vidoes instead of list"""
        response = self.client.post("api/v1/red-flags", data = json.dumps({
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "status":"Pending Investigation",
            "videos":["Video url"],
            "images":"images urls",
            "comment":"He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Unaccepted datatype or Inavlid Redflag")

        """Test for creating an invalid red-flag with an int value instead of string for status"""
        response = self.client.post("api/v1/red-flags", data = json.dumps({
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "status":55,
            "videos":["Video url"],
            "images":"images urls",
            "comment":"He was caught red handed"
        }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Unaccepted datatype or Inavlid Redflag")           

    def test_get_redflags(self):
        response = self.client.get("api/v1/red-flags", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_redflag(self):
        """Test get redflag with available id"""
        response = self.client.get("api/v1/red-flags/1", content_type="application/json")
        self.assertEqual(response.status_code, 200)

        """Test get redflag with with id not available"""
        response = self.client.get("api/v1/red-flags/19", content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"), "No redflag of that specific id found")

    def test_update_redflag(self):
        new_location = {"location":"1.500, 0.3000"}

        """Test update redflag with wrong url"""
        response = self.client.patch("api/v1/red-flags/4/wrong", data = json.dumps(new_location), content_type="application/json")
        self.assertEqual(response.status_code, 404)

        """Test update redflag with unavailable id"""
        response = self.client.patch("api/v1/red-flags/4/location", data = json.dumps(new_location), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data.get("message"), "Unaccepted datatype or Inavlid Redflag")

        """Test update redflag with the right id"""
        response = self.client.patch("api/v1/red-flags/1/location", data = json.dumps({"location":"1.500, 0.3000"}), content_type="application/json")
        data = json.loads(response.data.decode())

    def test_delete_redflag(self):
        """Test delete red-flag with unavailable id"""
        response = self.client.delete("api/v1/red-flags/3", content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("message"), "No redflag of that specific id found")

        """Test delete red-flag with unavailable id"""
        response = self.client.delete("api/v1/red-flags/2", content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 202)
        self.assertEqual(data.get("message"), "Red-flag deleted successfully")
        
