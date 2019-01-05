import unittest

from flask import json
from app.models.incident_model import IncidentData
# from app import create_app

class TestInterventionData(unittest.TestCase):

    def setUp(self):
        self.intervention_data = IncidentData()

        self.intervention_data.create_incident({
            "comment": "He was caught red handed",
            "created_by": "jonmark",
            "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
            "images": "images urls",
            "location": "Kawempe",
            "incident_id": 4,
            "status": "Pending Investigation",
            "type": "intervention",
            "videos": "Video url"
        }, "intervention")

    def test_update_intervention(self):
        new_comment = {"comment": "test comment"}
        data_test = {
                        "incident_id":4,
                        "type": "intervention",
                        "created_by":"jonmark",
                        "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
                        "location":"Kawempe",
                        "status":"Pending Investigation",
                        "videos":"Video url",
                        "images":"images urls",
                        "comment":"test comment"
                    }
        self.assertEqual(self.intervention_data.update_incident(1, new_comment, "intervention", "jonmark"), None)
        self.assertEqual(self.intervention_data.update_incident(4, new_comment, "intervention", "jonmark"), data_test)

    def test_delete_intervention(self):
        self.assertEqual(self.intervention_data.delete_incident(3, "intervention", "jonmark"), None)
        data_test = {
                        
            "comment": "He was caught red handed",
            "created_by": "jonmark",
            "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
            "images": "images urls",
            "location": "Kawempe",
            "incident_id": 4,
            "status": "Pending Investigation",
            "type": "intervention",
            "videos": "Video url"
                    }
        self.assertEqual(self.intervention_data.delete_incident(4, "intervention", "jonmark"), data_test)