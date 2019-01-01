import unittest
from app.models.incident_model import IncidentData

class TestRedflagData(unittest.TestCase):

    def setUp(self):
        self.redflag_data = IncidentData()
        self.redflag_data.create_incident({
            "comment": "He was caught red handed",
            "created_by": "jonmark",
            "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
            "images": "images urls",
            "location": "Kawempe",
            "incident_id": 4,
            "status": "Pending Investigation",
            "type": "redflag",
            "videos": "Video url"
        }, "redflag")

    def test_update_redflag(self):
        new_comment = {"comment": "test comment"}
        data_test = {
                        "incident_id":4,
                        "type": "redflag",
                        "created_by":"jonmark",
                        "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
                        "location":"Kawempe",
                        "status":"Pending Investigation",
                        "videos":"Video url",
                        "images":"images urls",
                        "comment":"test comment"
                    }
        self.assertEqual(self.redflag_data.update_incident(1, new_comment, "redflag","jonmark"), "non_author")
        self.assertEqual(self.redflag_data.update_incident(2, new_comment, "redflag","jonmark"), None)
        self.assertEqual(self.redflag_data.update_incident(4, new_comment, "redflag","jonmark"), data_test)

    def test_delete_redflag(self):
        self.assertEqual(self.redflag_data.delete_incident(3, "redflag","jonmark"), None)
        data_test = {
                        
            "comment": "He was caught red handed",
            "created_by": "jonmark",
            "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
            "images": "images urls",
            "location": "Kawempe",
            "incident_id": 4,
            "status": "Pending Investigation",
            "type": "redflag",
            "videos": "Video url"
                    }
        self.assertEqual(self.redflag_data.delete_incident(4, "redflag","jonmark"), data_test)