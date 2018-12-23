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
        test_data = {
            # "redflag_id":4,
            "report_type":"redflag",
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "status":"Pending Investigation",
            "videos":"Video url",
            "images":"images urls",
            "comment":"He was caught red handed"
        }
        test_data2 = {
            # "redflag_id":3,
            "report_type":"redflag",
            "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
            "created_by":"Jon Mark",
            "location":"Kawempe",
            "status":"Pending Investigation",
            "videos":"Video url",
            "images":"images urls",
            "comment":"He was caught red handed"
        }
        self.client.post("api/v1/red-flags", data = json.dumps(test_data2), content_type="application/json")
        response = self.client.post("api/v1/red-flags", data = json.dumps(test_data), content_type="application/json")
        self.assertEqual(response.status_code, 202)
        

    def test_get_redflags(self):
        response = self.client.get("api/v1/red-flags", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_redflag(self):
        response = self.client.get("api/v1/red-flags/1", content_type="application/json")
        response2 = self.client.get("api/v1/red-flags/19", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)

    def test_update_redflag(self):
        new_comment = {"comment":""}
        response = self.client.patch("api/v1/red-flags/4/comment", data = json.dumps(new_comment), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_redflag(self):
        response = self.client.delete("api/v1/red-flags/3", content_type="application/json")
        self.assertEqual(response.status_code, 404)
        pass