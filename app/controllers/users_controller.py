
"""controller module for users includes methods to connect the user models and views"""
import datetime
import hashlib
import jwt

from flask import Response, json

from app.models.user_model import User, UsersData
from app.validators.general_validator import GeneralValidator
from app.validators.user_validator import UserValidator
from app.utilities.static_strings import (

    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXP_DELTA_SECONDS,

    RESP_SUCCESS_MSG_REGISTRATION,
    RESP_SUCCESS_MSG_ADMIN_RIGHTS,
    RESP_SUCCESS_MSG_AUTH_LOGIN,

    RESP_ERROR_SIGNUP_FAIL_USER_EXISTS,
    RESP_ERROR_POST_EMPTY_DATA,
    RESP_ERROR_LOGIN_FAILED,
    RESP_ERROR_UPDATE_ROLE_FAILED,
    RESP_ERROR_INVALID_ROLE,
    RESP_ERROR_USER_NOT_FOUND,
    RESP_ERROR_INVALID_USER,
    RESP_ERROR_INVALID_OTHERNAME,
    RESP_ERROR_INVALID_NAME ,
    RESP_ERROR_INVALID_USERNAME,
    RESP_ERROR_INVALID_EMAIL,
    RESP_ERROR_INVALID_PHONE,
    RESP_ERROR_INVALID_PASSWORD
)


class UsersController():
    """controller class for the user"""
    usersdata = UsersData()
    my_validator = GeneralValidator()
    user_validator = UserValidator()

    def get_users(self):
        """method for getting all users"""
        return Response(
            json.dumps({
                "status": 200,
                "data": self.usersdata.get_users()
            }),
            content_type="application/json",
            status=200)
    
    def export_users(self):
        return self.usersdata.get_users()

    def get_user(self, user_id):
        """method for getting a single user by id"""
        get_user_instance = self.usersdata.get_user(user_id)
        if get_user_instance is None:
            return RESP_ERROR_USER_NOT_FOUND
        else:
            get_user_instance.pop("password")
            return Response(json.dumps({
                "status": 200,
                "data": [get_user_instance]
            }), content_type="application/json", status=200)    

    def adduser(self, request_info):
        """method for registering a user (signing up)"""
        firstname = request_info.get("firstname")
        lastname = request_info.get("lastname")
        othernames = request_info.get("othernames")
        username = request_info.get("username")
        email = request_info.get("email")
        phonenumber = request_info.get("phonenumber")
        is_admin = False
        password = request_info.get("password")
        registered_on = datetime.datetime.now()
        
        if self.response_signupfail(request_info, (firstname, lastname), username):
            return self.response_signupfail(request_info, (firstname, lastname), username)

        if self.response_invalid_values(email, phonenumber, password):
            return self.response_invalid_values(email, phonenumber, password)



        if self.user_validator.username_in_db(username, self.usersdata.get_users())\
            or self.user_validator.email_in_db(email, self.usersdata.get_users())\
            or self.user_validator.phonenumber_in_db(phonenumber, self.usersdata.get_users()):
            return RESP_ERROR_SIGNUP_FAIL_USER_EXISTS

        hashed_password = hashlib.sha224(b"{}").hexdigest().format(password)

        new_user = User(
            # user_id=user_id,
            firstname=firstname,
            lastname=lastname,
            othernames=othernames,
            username=username,
            email=email,
            phonenumber=phonenumber,
            is_admin=is_admin,
            password=hashed_password,
            registered_on=registered_on
        )

        user_id  = self.usersdata.add_user(new_user.user_dict())[0][0]
        newuser_dict = (new_user.user_dict())
        newuser_dict.pop("password")

        user_details = {
                    "user_id": user_id,
                    "username": newuser_dict.get("username"),
                    "is_admin": newuser_dict.get("is_admin")
                }
        payload = {
                'user_identity': user_details,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

        newuser_dict.update({"user_id": user_id})

        return Response(json.dumps({
            "status": 201,
            "data": [newuser_dict],
            "message": RESP_SUCCESS_MSG_REGISTRATION,
            "access_token": str(jwt_token)[2:-1]
        }), content_type="application/json", status=201)

    def signin(self, request_info):
        """method for signing in a user"""
        for login_key, login_val in request_info.items():
            if self.my_validator.empty_string(login_val):
                return RESP_ERROR_POST_EMPTY_DATA

        username = request_info.get("username")
        hashed_password = hashlib.sha224(
            b"{}").hexdigest().format(request_info.get("username"))

        for user in self.usersdata.get_users():
            if user.get("username") == username and user.get(
                    "password") == hashed_password:
                user_details = {
                    "user_id": user.get("user_id"),
                    "username": user.get("username"),
                    "is_admin": user.get("is_admin")
                }
                payload = {
                        'user_identity': user_details,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                        }
                jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

                return Response(json.dumps({
                    "status": 200,
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
                }), content_type="application/json", status=200)
        return RESP_ERROR_LOGIN_FAILED

    def update_user_role(self, user_id, request_info):
        """method for updating a user's role"""
        if request_info is None or "is_admin" not in request_info or len(
                request_info) != 1 or user_id == 1:
            return RESP_ERROR_UPDATE_ROLE_FAILED

        if self.user_validator.invalid_admin_state(
                request_info.get("is_admin")):
            return RESP_ERROR_INVALID_ROLE

        user_modified = self.usersdata.update_user(user_id, request_info)

        if user_modified is None:
            return RESP_ERROR_USER_NOT_FOUND
        else:
            return Response(json.dumps({
                "status": 201,
                "data": [user_modified],
                "message": RESP_SUCCESS_MSG_ADMIN_RIGHTS
            }), content_type="application/json", status=201)

    def response_signupfail(self, request_info, names_turple, username):
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
        if GeneralValidator.invalid_item(request_info, minimum_user_properties, all_user_fields):
            return RESP_ERROR_INVALID_USER
        elif any(UserValidator.invalid_name(item) for item in names_turple):
            return RESP_ERROR_INVALID_NAME
        elif self.user_validator.invalid_othername(request_info):
            return RESP_ERROR_INVALID_OTHERNAME
        elif UserValidator.invalid_username(username):
            return RESP_ERROR_INVALID_USERNAME

    def response_invalid_values(self, email, phone, password):
        if self.user_validator.invalid_email(email):
            return RESP_ERROR_INVALID_EMAIL
        elif self.user_validator.invalid_phone_number(str(phone)):
            return RESP_ERROR_INVALID_PHONE
        elif self.user_validator.invalid_password(password):
            return RESP_ERROR_INVALID_PASSWORD

