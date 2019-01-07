
"""controller module for users includes methods to connect the user models and views"""
import datetime
import hashlib

from flask import Response, json
from flask_jwt_extended import create_access_token

from app.models.user_model import User, UsersData
from app.validators.general_validator import GeneralValidator
from app.validators.user_validator import UserValidator
from app.utilitiez.static_strings import (
    RESP_INVALID_USER_INPUT,
    RESP_REGISTRATION_SUCCESS,
    RESP_ALREADY_TAKEN,
    RESP_EMPTY_INVALID_EMAIL_PASSWORD_PHONE,
    RESP_ROLE_INVALID,
    RESP_USER_NOT_FOUND,
    RESP_ADMIN_RIGHTS_SUCCESS,
    RESP_ROLE_NO_RIGHTS,
    RESP_AUTH_LOGIN_FAILED,
    RESP_AUTH_LOGIN_SUCCESS,
    RESP_EMPTY_STRING)


class UsersController():
    """controller class for the user"""
    usersdata = UsersData()
    my_validator = GeneralValidator()
    user_validator = UserValidator()

    def get_users(self):
        """method for getting all users"""
        return Response(
            json.dumps(self.usersdata.get_users()),
            content_type="application/json",
            status=200)

    def adduser(self, request_info):
        """method for registering a user (signing up)"""
        firstname = request_info.get("firstname")
        lastname = request_info.get("lastname")
        othernames = request_info.get("othernames")
        email = request_info.get("email")
        phonenumber = request_info.get("phonenumber")
        username = request_info.get("username")
        registered_on = datetime.datetime.now()
        is_admin = False
        password = request_info.get("password")

        user_id = self.my_validator.create_id(
            self.usersdata.get_users(), "user_id")

        user_properties = [firstname, lastname, othernames, username]

        if self.user_validator.invalid_user(request_info) or any(
                self.my_validator.check_str_datatype(item) for item in user_properties):
            return Response(json.dumps({
                "status": 400,
                "message": RESP_INVALID_USER_INPUT
            }), content_type="application/json", status=400)

        if self.user_validator.valid_email(email) or \
            self.user_validator.validate_phone_numbers(str(phonenumber)) or \
            not self.user_validator.valid_password(password) or\
            any(self.my_validator.check_empty_string(item) for item in user_properties):
            return Response(json.dumps({
                "status": 400,
                "message": RESP_EMPTY_INVALID_EMAIL_PASSWORD_PHONE
            }), content_type="application/json", status=400)

        if self.user_validator.username_in_db(username, self.usersdata.get_users())\
            or self.user_validator.email_in_db(email, self.usersdata.get_users())\
            or self.user_validator.phonenumber_in_db(phonenumber, self.usersdata.get_users()):
            return Response(json.dumps({
                "status": 400,
                "message": RESP_ALREADY_TAKEN
            }), content_type="application/json", status=400)

        hashed_password = hashlib.sha224(b"{}").hexdigest().format(password)

        new_user = User(
            user_id=user_id,
            firstname=firstname,
            lastname=lastname,
            othernames=othernames,
            email=email,
            phonenumber=phonenumber,
            username=username,
            registered_on=registered_on,
            is_admin=is_admin,
            password=hashed_password)

        self.usersdata.add_user(new_user.user_dict())
        newuser_dict = (new_user.user_dict())
        newuser_dict.pop("password")

        return Response(json.dumps({
            "status": 201,
            "data": [newuser_dict],
            "message": RESP_REGISTRATION_SUCCESS
        }), content_type="application/json", status=201)

    def signin(self, request_info):
        """method for signing in a user"""
        for login_key, login_val in request_info.items():
            if self.my_validator.check_empty_string(login_val):
                return Response(json.dumps({
                    "status": 400,
                    "message": RESP_EMPTY_STRING
                }), content_type="application/json", status=400)

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

                access_token = create_access_token(
                    identity=user_details,
                    expires_delta=datetime.timedelta(
                        days=30))
                response = Response(json.dumps({
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
                    "access_token": access_token,
                    "message": RESP_AUTH_LOGIN_SUCCESS
                }), content_type="application/json", status=201)
                response.set_cookie("username", user.get("username"))
                return response
        # else:
        return Response(json.dumps({
            "status": 403,
            "message": RESP_AUTH_LOGIN_FAILED
        }), content_type="application/json", status=403)

    def update_user_role(self, user_id, request_info):
        """method for updating a user's role"""
        if request_info is None or "is_admin" not in request_info or len(
                request_info) != 1 or user_id == 1:
            return Response(json.dumps({
                "message": RESP_ROLE_NO_RIGHTS
            }), content_type="application/json", status=401)

        if self.user_validator.invalid_admin_state(
                request_info.get("is_admin")):
            return Response(json.dumps({
                "message": RESP_ROLE_INVALID
            }), content_type="application/json", status=400)

        user_modified = self.usersdata.update_user(user_id, request_info)

        if user_modified is None:
            return Response(json.dumps({
                "status": 404,
                "message": RESP_USER_NOT_FOUND
            }), content_type="application/json", status=404)
        else:
            return Response(json.dumps({
                "status": 201,
                "data": [user_modified],
                "message": RESP_ADMIN_RIGHTS_SUCCESS
            }), content_type="application/json", status=201)
