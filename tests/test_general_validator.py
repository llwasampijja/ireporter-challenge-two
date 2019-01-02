import unittest
from app.validators.general_validator import GeneralValidator

class TestGeneralValidator(unittest.TestCase):
    def setUp(self):
        self.general_validator_obj = GeneralValidator()

    def test_check_empty_string(self):
        self.assertTrue(self.general_validator_obj.check_empty_string(""), msg="field shouldnt be empty")
        self.assertFalse(self.general_validator_obj.check_empty_string("The boy"), msg="great")
        self.assertTrue(self.general_validator_obj.check_empty_string("  "), msg="field shouldnt be empty")

    def test_check_str_datatype(self):
        self.assertTrue(self.general_validator_obj.check_str_datatype(3))
        self.assertFalse(self.general_validator_obj.check_str_datatype("posted something"))

    def test_check_status_value(self):
        self.assertFalse(self.general_validator_obj.check_status_value("resolved"))
        self.assertFalse(self.general_validator_obj.check_status_value("pending investigation"))
        self.assertFalse(self.general_validator_obj.check_status_value("rejected"))
        self.assertFalse(self.general_validator_obj.check_status_value("under investigation"))
        self.assertTrue(self.general_validator_obj.check_status_value("some string"))

    def test_invalid_incident(self):
        
        self.assertFalse(self.general_validator_obj.invalid_incident({
            # "created_by":"Jon Mark",
            "location":"8",
            # "status":"Pending Investigation",
            "videos":["Video url"],
            "images":["8"],
            "comment":"He was caught red handed"}))
        self.assertTrue(self.general_validator_obj.invalid_incident({
            "created_by":"Jon Mark",
            "location":"8",
            "allien":"8",
            "status":"Pending Investigation",
            "videos":["Video url"],
            "images":["8"],
            "comment":"He was caught red handed"}))
    
    def test_check_list_datatype(self):
        self.assertFalse(self.general_validator_obj.check_list_datatype(["video url"]))
        self.assertTrue(self.general_validator_obj.check_list_datatype([6,8]))
        self.assertTrue(self.general_validator_obj.check_list_datatype("video url"))
        self.assertTrue(self.general_validator_obj.check_list_datatype(6))