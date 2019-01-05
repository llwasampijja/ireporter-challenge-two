import unittest
from app.validators.user_validator import UserValidator

class TestUserValidity(unittest.TestCase):

    def setUp(self):
        self.uservalidator = UserValidator()

    def test_email_in_db(self):
        self.assertTrue(self.uservalidator.email_in_db("dallkased@bolon.empire", [{"email":"dallkased@bolon.empire"}]))
        self.assertFalse(self.uservalidator.email_in_db("dallkased@bolon.empire", [{"email":"llwasa@bolon.empire"}]))
    
    def test_username_in_db(self):
        self.assertTrue(self.uservalidator.username_in_db("dallkased", [{"username":"dallkased"}]))
        self.assertFalse(self.uservalidator.username_in_db("llwasampijja", [{"username":"llwasa"}]))

    def test_phonenumber_in_db(self):
        self.assertTrue(self.uservalidator.phonenumber_in_db("0775961853", [{"phonenumber":"0775961853"}]))
        self.assertFalse(self.uservalidator.phonenumber_in_db("0715961853", [{"phonenumber":"0775961853"}]))

    def test_validate_phone_numbers(self):
        self.assertTrue(self.uservalidator.validate_phone_numbers("3715961853"))
        self.assertFalse(self.uservalidator.validate_phone_numbers("0715961853"))

    def test_valid_email(self):
        self.assertFalse(self.uservalidator.valid_email("llwasa@bolon.emp"))
        self.assertTrue(self.uservalidator.valid_email("llwasabolon.emp"))

    def test_invalid_admin_state(self):
        self.assertTrue(self.uservalidator.invalid_admin_state("admin"))
        self.assertFalse(self.uservalidator.invalid_admin_state(True))
        self.assertFalse(self.uservalidator.invalid_admin_state(False))
        self.assertFalse(self.uservalidator.invalid_admin_state(False))

    def test_valid_password(self):
        self.assertFalse(self.uservalidator.valid_password("eiyiyn2"))
        self.assertTrue(self.uservalidator.valid_password("Auy23jrhG@"))

    def test_invalid_user(self):
        self.assertFalse(self.uservalidator.invalid_user({
            "firstname": "Edward",
            "lastname": "Kased",
            "othernames": "eddy2",
            "email": "edward6@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward6",
            "password": "ABd1234@1"
        }))
        self.assertTrue(self.uservalidator.invalid_user({
            "firstnamef": "Edward",
            "lastname": "8",
            "othernames": "eddy2",
            "email": "edward8@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward8",
            "is_admin": "true",
            "password": "ABd1234@1"
        }))