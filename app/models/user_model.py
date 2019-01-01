import hashlib
class User():
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")
        self.othernames = kwargs.get("othernames")
        self.email = kwargs.get("email")
        self.phonenumber = kwargs.get("phonenumber")
        self.username = kwargs.get("username")
        self.registered_on = kwargs.get("registered_on")
        self.is_admin = kwargs.get("is_admin")
        self.password = kwargs.get("password")

    def user_dict(self):
        return {
            "user_id": self.user_id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "othernames": self.othernames,
            "email": self.email,
            "phonenumber": self.phonenumber,
            "username": self.username,
            "registered_on": self.registered_on,
            "is_admin": self.is_admin,
            "password": self.password
        }


class UsersData():

    def __init__(self):

        self.users_list = [
            {
                "user_id": 1,
                "firstname": "Edward",
                "lastname": "Army",
                "othernames": "eddy",
                "email": "edward@bolon.com",
                "phonenumber": "0775961853",
                "username": "edward",
                "is_admin": True,
                "password": hashlib.sha224(
            b"{}").hexdigest().format("i@mG8t##")
            },
            {
                "user_id": 2,
                "firstname": "Jet",
                "lastname": "Li",
                "othernames": "The Real Li",
                "email": "jetli@bolon.com",
                "phonenumber": "0775961853",
                "username": "jetli",
                "is_admin": "admin",
                "password": hashlib.sha224(
            b"{}").hexdigest().format("i@mG8t##")
            }
        ]
        self.username_current = {"username":None}

    def add_user(self, user):
        return self.users_list.append(user)

    def get_users(self):
        return self.users_list

    def update_user(self, user_id, new_user_info):
        for user in self.users_list:
            if user.get("user_id") == user_id:
                user.update(new_user_info)
                user.pop("password")
                return user
        return None

    # def get_logged_user(self, username):
    #     return self.username_current.update({"username":username})
