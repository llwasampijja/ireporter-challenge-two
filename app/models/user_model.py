"""this module includes the usermodel obkect and the
userdata class with moethods for manipulating user data"""
import hashlib

from databases.ireporter_db import IreporterDb

class User():
    """user model"""

    def __init__(self, **kwargs):
        """initialising the parameters of the user object"""
        self.user_id = kwargs.get("user_id")
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")
        self.othernames = "none"
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.phonenumber = kwargs.get("phonenumber")
        self.is_admin = kwargs.get("is_admin")
        self.password = kwargs.get("password")
        self.registered_on = kwargs.get("registered_on")

    def user_dict(self):
        """method to return the dictionary of a user item"""
        return {
            "user_id": self.user_id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "othernames": self.othernames,
            "username": self.username,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "is_admin": self.is_admin,
            "password": self.password,
            "registered_on": self.registered_on
        }


class UsersData():
    """class includeing methods for manipulating user items in users list"""

    ireporter_db = IreporterDb()

    def __init__(self):
        """users data initialiser"""
        self.users_list = [
            {
                "user_id": 1,
                "firstname": "Edward",
                "lastname": "Army",
                "othernames": "eddy",
                "username": "edward",
                "email": "edward@bolon.com",
                "phonenumber": "0775961853",  
                "is_admin": True,
                "password": hashlib.sha224(
                    b"{}").hexdigest().format("i@mG8t##")
            },
        ]
        self.username_current = {"username":None}

    def add_user(self, user):
        """method for adding a user item in the users list"""
        return self.ireporter_db.insert_data_users(
            user.get("firstname"),
            user.get("lastname"),
            user.get("othernames"),
            user.get("username"),
            user.get("email"),
            user.get("phonenumber"),
            user.get("is_admin"),
            user.get("password"),
            user.get("registered_on")
        )

    def get_users(self):
        """method for getting user items in the users list"""
        return self.get_all_dbusers()

    def update_user(self, user_id, new_user_info):
        """method for updating a user item in the users list"""
        for user in self.get_all_dbusers():
            if user.get("user_id") == user_id:
                self.ireporter_db.update_data_user_role(user_id, new_user_info.get("is_admin"))
                return user
        return None

    def get_all_dbusers(self):
        data_from_db = self.ireporter_db.fetch_data_users("app_users")
        dict_user = {}
        list_users = []
        for user in data_from_db:
            dict_user = {
                "user_id": user[0],
                "firstname": user[1],
                "lastname": user[2],
                "othernames": user[3],
                "username": user[4],
                "email": user[5],
                "phonenumber": user[6],
                "is_admin": user[7],
                "password":user[8],
                "registered_on": user[9]
            }
            list_users.append(dict_user)
        return list_users

        
