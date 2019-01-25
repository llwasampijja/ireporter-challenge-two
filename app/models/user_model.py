"""this module includes the usermodel obkect and the
userdata class with moethods for manipulating user data"""
import hashlib
import re
import datetime
import jwt


from databases.ireporter_db import IreporterDb
from flask import Response, json

from app.utilities.static_strings import (
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXP_DELTA_SECONDS,

    RESP_ERROR_POST_EMPTY_DATA,
    RESP_ERROR_INVALID_USER,
    RESP_ERROR_INVALID_EMAIL,
    RESP_ERROR_INVALID_PHONE,
    RESP_ERROR_INVALID_PASSWORD,
    RESP_ERROR_SIGNUP_FAIL_USER_EXISTS,
    RESP_SUCCESS_MSG_REGISTRATION,
    RESP_SUCCESS_MSG_AUTH_LOGIN,
    RESP_SUCCESS_MSG_ADMIN_RIGHTS,

    RESP_ERROR_INVALID_FIRSTNAME,
    RESP_ERROR_INVALID_LASTNAME,
    # RESP_ERROR_INVALID_EMAIL,
    RESP_ERROR_INVALID_OTHERNAMES,
    RESP_ERROR_INVALID_EMAIL,
    # RESP_ERROR_INVALID_PHONENUMBER,
    # RESP_ERROR_INVALID_PASSWORD,
    RESP_ERROR_INVALID_USERNAME,
    RESP_ERROR_INVALID_LOGIN_CREDS,
    RESP_ERROR_EMPTY_USERNAME,
    RESP_ERROR_EMPTY_PASSWORD,
    RESP_ERROR_LOGIN_FAILED,
    RESP_ERROR_UPDATE_ROLE_FAILED,
    RESP_ERROR_INVALID_ROLE,
    RESP_ERROR_USER_NOT_FOUND,
    RESP_ERROR_MSG_EMPTY_PASSWORD,
    RESP_ERROR_MSG_INVALID_OTHERNAMES
)


class User():
    """user model"""

    ireporter_db = IreporterDb()

    def create_user(self, request_data):
        othernames = ""
        if any(self.check_empty_str(user_field) for  key_vale, user_field in request_data.items()):
            return RESP_ERROR_POST_EMPTY_DATA

        if self.validate_user(request_data):
            return RESP_ERROR_INVALID_USER

        if self.validate_name(request_data.get("firstname")):
            return RESP_ERROR_INVALID_FIRSTNAME

        if self.validate_name(request_data.get("lastname")):
            return RESP_ERROR_INVALID_LASTNAME

        if self.validate_othernames(request_data.get("othernames"), request_data):
            return RESP_ERROR_MSG_INVALID_OTHERNAMES
        othernames = self.validate_othernames(request_data.get("othernames"), request_data)

        if self.validate_username(request_data.get("username")):
            return RESP_ERROR_INVALID_USERNAME

        if self.validate_email(request_data.get("email")):
            return RESP_ERROR_INVALID_EMAIL

        if self.validate_phonenumber(request_data.get("phonenumber")):
            return RESP_ERROR_INVALID_PHONE

        if self.validate_password(request_data.get("password")):
            return RESP_ERROR_INVALID_PASSWORD

        if self.duplicate_user(request_data.get("username"), request_data.get("email"), request_data.get("phonenumber")):
            return RESP_ERROR_SIGNUP_FAIL_USER_EXISTS


        user_id = self.ireporter_db.insert_data_users(
            request_data.get("firstname"),
            request_data.get("lastname"),
            othernames,
            request_data.get("username"),
            request_data.get("email"),
            request_data.get("phonenumber"),
            False,
            hashlib.sha224(
            b"{}").hexdigest().format(request_data.get("password")),
            datetime.datetime.now()
        )

        new_user = {
            "user_id": user_id[0][0],
            "firstname": request_data.get("firstname"),
            "lastname": request_data.get("lastname"),
            "othernames": othernames,
            "username": request_data.get("username"),
            "email": request_data.get("email"),
            "phonenumber": request_data.get("phonenumber"),
            "is_admin": False,
            "registered_on":datetime.datetime.now()
        }

        payload = {
                'user_identity': {
                    "user_id":user_id[0][0],
                    "is_admin":False
                },
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

        return Response(json.dumps({
            "status": new_user,
            "message": RESP_SUCCESS_MSG_REGISTRATION,
            "access_token": str(jwt_token)[2:-1]
        }), content_type="application/json", status=201)


    def validate_user(self, request_info):
        """this method checks if a request contains all and only required fields"""
        minimum_turple = (
            "firstname",
            "lastname",
            "phonenumber",
            "email",
            "username",
            "password"
        )

        maxmmum_tuple = (
            "firstname",
            "lastname",
            "othernames",
            "phonenumber",
            "email",
            "username",
            "password"
        )

        if any(item not in request_info for item in minimum_turple) \
        or any(item not in maxmmum_tuple for item in request_info):
            return True
        return False

    def duplicate_user(self, username, email, phonenumber):
        if self.username_in_db(username, UsersData.get_all_dbusers(UsersData))\
            or self.email_in_db(email, UsersData.get_all_dbusers(UsersData))\
            or self.phonenumber_in_db(phonenumber, UsersData.get_all_dbusers(UsersData)):
            return True
        return False

    def check_empty_str(self, test_string):
        """this method checks for empty incident and user fields"""
        if str(test_string).replace(" ", "") == "":
            return True
        return False

    def login_user(self, request_info):
        """method for signing in a user"""
        login_creds = ("username", "password")

        if not request_info or any(item not in request_info for item in login_creds) \
        or any(item not in login_creds for item in request_info):
            return RESP_ERROR_INVALID_LOGIN_CREDS
        
        if self.check_empty_str(request_info.get("username")):
            return RESP_ERROR_EMPTY_USERNAME

        if self.check_empty_str(request_info.get("password")):
            return RESP_ERROR_MSG_EMPTY_PASSWORD

        

        username = request_info.get("username")
        hashed_password = hashlib.sha224(
            b"{}").hexdigest().format(request_info.get("password"))

        for user in UsersData.get_all_dbusers(UsersData):
            if user.get("password") != hashed_password:
                print("valid password")

            if user.get("username") == username and user.get("password")== user.get("password"):
                user_details = {
                    "user_id": user.get("user_id"),
                    "is_admin": user.get("is_admin")
                }
                payload = {
                        'user_identity': user_details,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                        }
                jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
                return Response(json.dumps({
                    "status": 201,
                    "data": [
                        {
                            "user_id": user.get("user_id"),
                            "firstname": user.get("firstname"),
                            "lastname": user.get("lastname"),
                            "othernames": user.get("othernames"),
                            "email": user.get("email"),
                            "phonenumber": user.get("phonenumber"),
                            "username": user.get("username"),
                            "is_admin": user.get("is_admin")
                        }
                    ],
                    "access_token": str(jwt_token)[2:-1],
                    "message": RESP_SUCCESS_MSG_AUTH_LOGIN
                }), content_type="application/json", status=201)
        return RESP_ERROR_LOGIN_FAILED

    def edit_userrole(self, user_id, request_info):
        """method for updating a user's role"""
        if request_info is None or "is_admin" not in request_info or len(
                request_info) != 1 or user_id == 1:
            return RESP_ERROR_UPDATE_ROLE_FAILED

        if self.invalid_admin_state(
                request_info.get("is_admin")):
            return RESP_ERROR_INVALID_ROLE

        user_modified = self.ireporter_db.update_data_user_role(user_id, request_info.get("is_admin"))


        if not user_modified:
            return RESP_ERROR_USER_NOT_FOUND
        else:
            return Response(json.dumps({
                "status": 201,
                "data": [user_modified],
                "message": RESP_SUCCESS_MSG_ADMIN_RIGHTS
            }), content_type="application/json", status=201)

    
    def invalid_admin_state(self, isadmin):
        """method checks is is_admin as a valid value"""
        if isinstance(isadmin, bool):
            return False
        return True

    def validate_name(self, name):
        """method checks if a provided name is valid"""
        if any(not item.isalpha() for item in str(name)):
            return True
        return False

    def validate_userobj(self, request_data):
        minimum_user_properties = (
            "firstname",
            "lastname",
            "email",
            "phonenumber",
            "username",
            "password"
        )
        all_user_fields = (
            "firstname",
            "lastname",
            "othernames",
            "email",
            "phonenumber",
            "username",
            "password"
            )

        if any(item not in request_data for item in minimum_user_properties) \
        or any(item not in all_user_fields for item in request_data):
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

    # def update_user(self, user_id, new_user_info):
    #     """method for updating a user item in the users list"""
    #     for user in self.get_all_dbusers():
    #         if user.get("user_id") == user_id:
    #             self.ireporter_db.update_data_user_role(user_id, new_user_info.get("is_admin"))
    #             return user
    #     return None

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

        
