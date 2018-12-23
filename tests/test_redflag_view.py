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
        self.client.post("api/v1/red-flags", data = json.dumps({
            "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "status":"Pending Investigation",
            "videos":["Video url"],
            "images":["images urls"],
            "comment":"He was caught red handed"
        }), content_type="application/json")
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
        self.assertEqual(response.status_code, 406)
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
        
