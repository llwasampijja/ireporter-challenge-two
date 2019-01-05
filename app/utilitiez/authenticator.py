from flask import Response, json
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
import hashlib

from app.utilitiez.static_strings import RESP_UNAUTHORIZED_VIEW, RESP_ADMIN_ONLY


class Authenticator():

    def authorized(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            if user_identity["is_admin"]  == True or user_identity["is_admin"] == False:
                return fn(*args, **kwargs)
            else:
                return Response(json.dumps({
                    "status": 403,
                    "message": RESP_UNAUTHORIZED_VIEW
                }), content_type="application/json", status=403)
                
        return wrapper

    def concerned_citzen(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            if not user_identity["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return Response(json.dumps({
                    "message": RESP_UNAUTHORIZED_VIEW
                }), content_type="application/json", status=403)
        return wrapper

    def admin_only(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            if user_identity["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return Response(json.dumps({
                    "message": RESP_ADMIN_ONLY
                }), content_type="application/json", status=403)

        return wrapper