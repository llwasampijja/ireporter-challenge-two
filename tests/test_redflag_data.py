import unittest
from app.data.redflag_data import RedflagData

class TestRedflagData(unittest.TestCase):

    def setUp(self):
        self.redflag_data = RedflagData()
        self.redflag_data.create_redflag({
            "comment": "He was caught red handed",
            "created_by": "Jon Mark",
            "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
            "images": "images urls",
            "location": "Kawempe",
            "redflag_id": 4,
            "status": "Pending Investigation",
            "type": "redflag",
            "videos": "Video url"
        })

    def test_update_redflag(self):
        new_comment = {"comment": "test comment"}
        data_test = {
                        "redflag_id":4,
                        "type": "redflag",
                        "created_by":"Jon Mark",
                        "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
                        "location":"Kawempe",
                        "status":"Pending Investigation",
                        "videos":"Video url",
                        "images":"images urls",
                        "comment":"test comment"
                    }
        self.assertEqual(self.redflag_data.update_redflag(1, new_comment), None)
        self.assertEqual(self.redflag_data.update_redflag(4, new_comment), data_test)

    def test_delete_redflag(self):
        self.assertEqual(self.redflag_data.delete_redflag(3), None)
        data_test = {
                        
            "comment": "He was caught red handed",
            "created_by": "Jon Mark",
            "created_on": "Thu, 20 Dec 2018 07:23:22 GMT",
            "images": "images urls",
            "location": "Kawempe",
            "redflag_id": 4,
            "status": "Pending Investigation",
            "type": "redflag",
            "videos": "Video url"
                    }
        self.assertEqual(self.redflag_data.delete_redflag(4), data_test)