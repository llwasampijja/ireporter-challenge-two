"""This module includes all strings and responses which are constant accross the app"""
from flask import Response, json

RESP_SUCCESS_MSG_REGISTRATION = "User successfully signed up"
RESP_ERROR_MSG_FIRSTNAME = "Bad request, check your input and try again"


RESP_ERROR_INVALID_FIRSTNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_LASTNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_EMAIL = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_OTHERNAMES = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_EMAIL = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_PHONENUMBER = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_PASSWORD = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_USERNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)