"""this module includes the usermodel obkect and the
userdata class with moethods for manipulating user data"""
import hashlib
import re

from databases.ireporter_db import IreporterDb

class User():
    """user model"""

    def create_user(self, request_data):
        if validate_name(request_data.get("firstname")):
            return RESP_
    
    def login_user(self, request_data):
        pass

    def edit_userrole(self, request_data):
        pass

    def validate_name(self, name):
        """method checks if a provided name is valid"""
        if any(not item.isalpha() for item in str(name)):
            return True
        return False

    def validate_password(self, password):
        """method checks for an unacceptable password"""
        special_characters = ['$', '#', '@']
        password = password.replace(" ", "")
        test_conditions = [
            (len(password) >= 8 and len(password) <= 12),
            (any(x.isupper() for x in password) and any(x.islower()
                                                        for x in password)),
            (any(y in password for y in special_characters)
             and any(y.isdigit() for y in password))
        ]
        if all(condition is True for condition in test_conditions):
            return False
        return True

    def user_in_db(self, user_field, users_list, user_key):
        """refactored method to check if a user is already in the system"""
        if any(user.get(user_key) == user_field for user in users_list):
            return True
        return False

    def invalid_admin_state(self, isadmin):
        """method checks is is_admin as a valid value"""
        if isinstance(isadmin, bool):
            return False
        return True

    def validate_email(self, email):
        """method checks if the email is in the correct format"""
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if email_pattern.match(email):
            return False
        return True

    def validate_phonenumber(self, phonenumber):
        """check if phonenumber has the correct number of digits for uganda"""
        if all(digit.isdigit() for digit in phonenumber) \
                and len(phonenumber) <= 10 and phonenumber.startswith("0"):
            return False
        return True

    def validate_othernames(self, othernames, request_data):
        """method checks if othernames is provided by the user and if \
        provided it checks if it is a valid name"""
        if "othernames" in request_data \
        and self.validate_name(request_data.get("othernames")):
            return True
        return False
        
    def validate_username(self, username):
        """method checks if a provided username is valid"""
        word_letters = re.sub('[^a-zA-Z-0-9]+', '', str(username))
        if any(item.isalpha() for item in word_letters):
            return False
        return True

    def username_in_db(self, username, users_list):
        """method checks if a username is already in the system"""
        return self.user_in_db(username, users_list, "username")

    def email_in_db(self, email, users_list):
        """method checks if email already in the system"""
        return self.user_in_db(email, users_list, "email")

    def phonenumber_in_db(self, phonenumber, users_list):
        """method checks if phonenumber already in the system"""
        return self.user_in_db(phonenumber, users_list, "phonenumber")


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

        
