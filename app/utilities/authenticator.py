"""this module includes decorators for authenticating users """
from functools import wraps
import jwt

from flask import request, Response

from app.utilities.static_strings import (
    RESP_ERROR_UNAUTHORIZED_VIEW,
    RESP_ERROR_ADMIN_ONLY,
    RESP_ERROR_NOT_LOGGEDIN
)


class Authenticator():
    """class authenticator"""

    @staticmethod
    def authorized(fxn):
        """decorator for authorizing both admins and registered non admin users"""
        @wraps(fxn)
        def wrapper(*args, **kwargs):
            user_identity = Authenticator.get_identity(Authenticator, Authenticator.get_token(Authenticator))
            if isinstance(user_identity, Response):
                return user_identity
            if str(user_identity["is_admin"]).lower() == "true" \
                    or str(user_identity["is_admin"]).lower() == "false":
                return fxn(*args, **kwargs)

        return wrapper

    @staticmethod
    def concerned_citzen(fxn):
        """decorator for authorizing only registered no admin users"""
        @wraps(fxn)
        def wrapper(*args, **kwargs):
            user_identity = Authenticator.get_identity(Authenticator, Authenticator.get_token(Authenticator))
            if isinstance(user_identity, Response):
                return user_identity
            elif not user_identity["is_admin"]:
                return fxn(*args, **kwargs)
            else:
                return RESP_ERROR_UNAUTHORIZED_VIEW
        return wrapper

    @staticmethod
    def admin_only(fxn):
        """decorator for authorizing only admins"""
        @wraps(fxn)
        def wrapper(*args, **kwargs):
            user_identity = Authenticator.get_identity(Authenticator, Authenticator.get_token(Authenticator))
            if isinstance(user_identity, Response):
                return user_identity

            if user_identity["is_admin"]:
                return fxn(*args, **kwargs)
            else:
                return RESP_ERROR_ADMIN_ONLY
        return wrapper 


    def get_token(self):
        header = request.headers.get("Authorization")
        if not header:
            return RESP_ERROR_UNAUTHORIZED_VIEW
        token = str(header).split(" ")[1]
        return token


    def get_identity(self, jwt_token):
        try:
            my_payload = jwt.decode(jwt_token, "thereisgoodintheworld", algorithms="HS256")
            return my_payload.get("user_identity")
        except:
            return RESP_ERROR_NOT_LOGGEDIN