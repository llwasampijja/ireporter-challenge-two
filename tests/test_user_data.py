import unittest
from app.models.user_model import UsersData


class TestUserData(unittest.TestCase):

    def setUp(self):
        self.user_data = UsersData()
        self.user_data.add_user({
            "firstname": "Edward",
            "lastname": "8",
            "othernames": "eddy2",
            "email": "edward2@bolon.com",
            "phonenumber": "0775961853",
            "username": "edward2",
            "is_admin": "true",
            "password": "ABd1234@1"
        })

    def test_get_users(self):
        pass
