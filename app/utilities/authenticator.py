"""this module includes decorators for authenticating users """
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.utilities.static_strings import (
    RESP_ERROR_UNAUTHORIZED_VIEW,
    RESP_ERROR_ADMIN_ONLY
)


class Authenticator():
    """class authenticator"""

    @staticmethod
    def authorized(fxn):
        """decorator for authorizing both admins and registered non admin users"""
        @wraps(fxn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            if str(user_identity["is_admin"]).lower() == "true" \
                    or str(user_identity["is_admin"]).lower() == "false":
                return fxn(*args, **kwargs)

        return wrapper

    @staticmethod
    def concerned_citzen(fxn):
        """decorator for authorizing only registered no admin users"""
        @wraps(fxn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            if not user_identity["is_admin"]:
                return fxn(*args, **kwargs)
            else:
                return RESP_ERROR_UNAUTHORIZED_VIEW
        return wrapper

    @staticmethod
    def admin_only(fxn):
        """decorator for authorizing only admins"""
        @wraps(fxn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            if user_identity["is_admin"]:
                return fxn(*args, **kwargs)
            else:
                return RESP_ERROR_ADMIN_ONLY
        return wrapper 
