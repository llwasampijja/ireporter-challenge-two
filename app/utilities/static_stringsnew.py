"""This module includes all strings and responses which are constant accross the app"""
from flask import Response, json

RESP_SUCCESS_MSG_REGISTRATION = "User successfully signed up"
RESP_SUCCESS_MSG_AUTH_LOGIN = "User successfully logged in"
RESP_SUCCESS_MSG_ADMIN_RIGHTS = "The admin rights of the user have been updated successfully"
RESP_SUCCESS_MSG_CREATE_INCIDENT = "Incident created successfully"
RESP_SUCCESS_MSG_INCIDENT_DELETE = "Incident was deleted successfully"
RESP_SUCCESS_MSG_INCIDENT_UPDATE = "Updated the incident record’s location successfully"
RESP_SUCCESS_MSG_INCIDENT_LIST_EMPTY = "Incidents list is empty"
RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE = "Updated the incident record’s status successfully"


RESP_ERROR_MSG_FIRSTNAME = "Entered an invalid firstname"
RESP_ERROR_MSG_INVALID_LASTNAME = "Entered an invalid lastname"
RESP_ERROR_MSG_INVALID_OTHERNAMES = "Entered an invalid othernames"
RESP_ERROR_MSG_INVALID_USERNAME = "Entered an invalid username"
RESP_ERROR_MSG_INVALID_EMAIL = "Entered an invalid email"
RESP_ERROR_MSG_INVALID_PHONENUMBER = "Entered an invalid phonenumber"
RESP_ERROR_MSG_INVALID_PASSWORD = "Entered an invalid password"
RESP_ERROR_MSG_INVALID_LOGIN_CREDS = "Entered an invalid password"
RESP_ERROR_EMPTY_USERNAME = "Enter a empty username"
RESP_ERROR_EMPTY_PASSWORD = "Enter a empty password"
RESP_ERROR_MSG_LOGIN_FAILED = "Failed to login. username or password is incorrect"
RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS = "Failed to Signup. Attempting to sign-up with an Email address, phonenumber or username  which is/are already registered on the system"



RESP_ERROR_SIGNUP_FAIL_USER_EXISTS = Response(json.dumps({
    "status": 400,
    "message": RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS
}), content_type="application/json", status=400)

RESP_ERROR_UPDATE_ROLE_FAILED = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_LOGIN_FAILED
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_ROLE = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_LOGIN_FAILED
}), content_type="application/json", status=400)
RESP_ERROR_USER_NOT_FOUND = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_LOGIN_FAILED
}), content_type="application/json", status=400)

RESP_ERROR_LOGIN_FAILED = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_LOGIN_FAILED
}), content_type="application/json", status=400)

RESP_ERROR_EMPTY_USERNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_EMPTY_USERNAME
}), content_type="application/json", status=400)

RESP_ERROR_EMPTY_PASSWORD = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_EMPTY_PASSWORD
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_LOGIN_CREDS = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_LOGIN_CREDS
}), content_type="application/json", status=400)

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