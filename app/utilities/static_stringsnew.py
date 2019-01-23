"""This module includes all strings and responses which are constant accross the app"""
from flask import Response, json

RESP_SUCCESS_MSG_REGISTRATION = "User successfully signed up"
RESP_ERROR_MSG_FIRSTNAME = "Entered an invalid firstname"
RESP_ERROR_MSG_INVALID_LASTNAME = "Entered an invalid lastname"
RESP_ERROR_MSG_INVALID_OTHERNAMES = "Entered an invalid othernames"
RESP_ERROR_MSG_INVALID_USERNAME = "Entered an invalid username"
RESP_ERROR_MSG_INVALID_EMAIL = "Entered an invalid email"
RESP_ERROR_MSG_INVALID_PHONENUMBER = "Entered an invalid phonenumber"
RESP_ERROR_MSG_INVALID_PASSWORD = "Entered an invalid password"


RESP_ERROR_INVALID_FIRSTNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_FIRSTNAME
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_LASTNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_LASTNAME
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_EMAIL = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_EMAIL
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_OTHERNAMES = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_OTHERNAMES
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_EMAIL = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_EMAIL
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_PHONENUMBER = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_PHONENUMBER
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_PASSWORD = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_PASSWORD
}), content_type="application/json", status=400)
RESP_ERROR_INVALID_USERNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_USERNAME
}), content_type="application/json", status=400)