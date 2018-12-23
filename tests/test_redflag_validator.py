import unittest
from app.validators.redflag_validator import RedflagValidator

class TestRedflagValidator(unittest.TestCase):
    def setUp(self):
        self.redflagValidator = RedflagValidator()

    def test_check_empty_string(self):
        self.assertTrue(self.redflagValidator.check_empty_string(""), msg="field shouldnt be empty")
        self.assertFalse(self.redflagValidator.check_empty_string("The boy"), msg="great")
        self.assertTrue(self.redflagValidator.check_empty_string("  "), msg="field shouldnt be empty")

    def test_check_str_datatype(self):
        self.assertTrue(self.redflagValidator.check_str_datatype(3))
        self.assertFalse(self.redflagValidator.check_str_datatype("posted something"))

    def test_check_int_datatype(self):
        self.assertTrue(self.redflagValidator.check_int_datatype(3))
        self.assertFalse(self.redflagValidator.check_int_datatype("posted something"))

    def test_check_status_value(self):
        self.assertFalse(self.redflagValidator.check_status_value("resolved"))
        self.assertFalse(self.redflagValidator.check_status_value("pending investigation"))
        self.assertFalse(self.redflagValidator.check_status_value("rejected"))
        self.assertTrue(self.redflagValidator.check_status_value("some string"))
