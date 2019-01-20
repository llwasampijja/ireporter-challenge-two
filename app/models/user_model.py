"""this module includes the usermodel obkect and the
userdata class with moethods for manipulating user data"""

import hashlib
class User():
    """user model"""

    def __init__(self, **kwargs):
        """initialising the parameters of the user object"""
        self.user_id = kwargs.get("user_id")
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")
        self.othernames = "ANN"
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
        return self.users_list.append(user)

    def get_users(self):
        """method for getting user items in the users list"""
        return self.users_list

    def update_user(self, user_id, new_user_info):
        """method for updating a user item in the users list"""
        for user in self.users_list:
            if user.get("user_id") == user_id:
                user.update(new_user_info)
                user.pop("password")
                return user
        return None
        
