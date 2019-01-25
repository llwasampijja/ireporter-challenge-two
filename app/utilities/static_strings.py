"""This module includes all strings and responses which are constant accross the app"""
from flask import Response, json

# welcome message
WELCOME_MSG = "Welcome to Lwasa Lamech's iReporter"

# url string constants for users and authentication
URL_REGISTER = "/api/v1/auth/register"
URL_LOGIN = "/api/v1/auth/login"
URL_USERS = "/api/v1/users"
URL_BASE = "/api/v1"

# url string constants for incidents
URL_REDFLAGS = "/api/v1/red-flags"
URL_INTERVENTIONS = "/api/v1/interventions"

JWT_SECRET = "thereisgoodintheworld"
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20000

# swagger url string constants
SWAGGER_UI_URL = "/api/v1/docs"
# remote API documenation url
API_URL = "https://llwasampijja.github.io/ireporter-challenge-two/ireporter_challenge_two.json"

# dictionary for routes
MY_ROUTES = {
    "01. Register": "/auth/register",
    "02. Login": "/auth/login",
    "03. Create a Red-flag": "/red-flags",
    "04. Get all Red-flags": "/red-flags",
    "05. Get a Red-flag": "/red-flags/redflag_id",
    "06. Update a Red-flag's location": "/red-flags/redflag_id/location",
    "07. Update a Red-flag's status": "/red-flags/redflag_id/status",
    "08. Delete a Red-flag": "/red-flags/redflag_id",
    "09. Create an Intervention": "/interventions",
    "10. Get All Interventions": "/interventions",
    "11. Get an Intervention": "/interventions/intervention_id",
    "12. Update an Intervention's location": "/interventions/intervention_id/location",
    "13. Update an Intervention's status": "/interventions/intervention_id/status",
    "14. Delete  an Intervention": "/interventions/intervention_id",
    "15. Get all users": "/users",
    "16. Update a user's role": "users/user_id"
}


# string constants for success message responses
RESP_SUCCESS_MSG_REGISTRATION = "User account created and logged in successfully"
RESP_SUCCESS_MSG_ADMIN_RIGHTS = "The admin rights of the user have been updated successfully"
RESP_SUCCESS_MSG_CREATE_INCIDENT = "Incident created successfully"
RESP_SUCCESS_MSG_INCIDENT_DELETE = "Incident was deleted successfully"
RESP_SUCCESS_MSG_INCIDENT_UPDATE_COMMENT = "Updated the incident record’s comment successfully"
RESP_SUCCESS_MSG_INCIDENT_UPDATE_STATUS = "Updated the incident record’s status successfully"
RESP_SUCCESS_MSG_INCIDENT_UPDATE_LOCATION = "Updated the incident record’s location successfully"

RESP_SUCCESS_MSG_INCIDENT_LIST_EMPTY = "Incidents list is empty"
RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE = "Updated the incident record’s status successfully"
RESP_SUCCESS_MSG_AUTH_LOGIN = "Logged in successfully"

RESP_SUCCESS_MSG_INDEX_MESSAGE = {
    "NB": "Add these endpoints to the versioned base url, i.e immediately after '/api/v1'",
    "Admin Credentials": "username = 'edward', password = 'i@mG8t##'",
    "Endpoints": MY_ROUTES
}

# string constants for general error messages
RESP_ERROR_MSG_BAD_REQUEST = "Bad request, check your input and try again"
RESP_ERROR_MSG_PAGE_NOT = "No such page exists on this site"
RESP_ERROR_MSG_METHOD_NOT_ALLOWED = "Method not allowed"
RESP_ERROR_MSG_INTERNAL_SERVER_ERROR = "An internal server error occured. Try again later when this issue is resolved by the site administrators or make sure you are submitting the correct and allowed format of data"

RESP_ERROR_MSG_UNAUTHORIZED_VIEW = "You are not authorised to access this content"
RESP_ERROR_MSG_EMPTY_STRING = "Empty fields are not allowed"
RESP_ERROR_MSG_UNACCEPTABLE_INPUT = "Operation failed. You entered an unacceptable value for the operation"
RESP_ERROR_MSG_UDATE_WRONG_LOCATION = "Failed to update the incident's location. You provided wrong values.The location field must be a string of two floating values separated by a comma ',', i.e: A latitude and longitude. The latitude must be in the ranges 0 to 90 or -90 to 0. The longitude must be in the ranges 0 to 180 or -180 to 0"
RESP_EEROR_MSG_UNAUTHORIZED_DELETE = "You are not authorised to delete this incident"
RESP_ERROR_MSG_UNAUTHORIZED_EDIT = "You are not authorised to edit this incident"
RESP_ERROR_MSG_USER_NOT_FOUND = "That specified user wasn't found on the system"
RESP_ERROR_MSG_INVALID_ROLE = "Failed to update user's role. Entered an invalid value. A valid value must either be true (admin) or false (not admin)"
RESP_ERROR_MSG_ROLE_NO_RIGHTS = "An administrator can only edit a user's role"
RESP_ERROR_MSG_LOGIN_FAILED = "Failed to login. username or password is incorrect"
RESP_ERROR_MSG_UPDATE_STATUS = "Failed to update the incident's status. You provided an invalid value. A valid value must either be 'pending investigation', 'under investigation', 'resolved' or 'rejected'"
RESP_ERROR_MSG_INCIDENT_NOT_FOUND = "No incident of that specific id was found on the system"
RESP_ERROR_MSG_INCIDENT_DUPLICATE = "Failed to add incident. An incident similar to this already exists on the system. Creating a duplicate of an incident isn't allowed"
RESP_ERROR_MSG_USER_STATUS_NORIGHTS = "Failed to update the incident's status. An admin can only edit the status of an incident, and nothing more. The only accepted values include: 'pending investigation','under investigation', 'resolved' and 'rejected'"
RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS = "Failed to Signup. Attempting to sign-up with an Email address, phonenumber or username  which is/are already registered on the system"
RESP_ERROR_MSG_ADMIN_NO_RIGHTS = "Operation failed: An admin can't edit any other field of an incident except the status"
RESP_ERROR_MSG_INVALID_USER = "You have less or more fields than the required number. They must include: firstname, lastname, othernames, email, phonenumber, username, password."
RESP_ERROR_MSG_INVALID_USERNAME = "ERROR: You have entered an invalid username. May contain numbers but must contain at least one letter"
RESP_ERROR_MSG_INVALID_EMAIL = "ERROR: Entered an invalid email. Email must be in the format 'username@company.doman'"
RESP_ERROR_MSG_INVALID_PHONE = "ERROR: Entered an invalid phonenumber. Phonenumber must start with 0 and iinclude 0 other digits."
RESP_ERROR_MSG_INVALID_PASSWORD = "ERROR: Entered an invalid password. Password string must have a length of atleast 8 characters and atmost 12 characters; include at list one uppercase letter, lowercase lettter and number; and must contain atleast a '$', '#' or '@'"
RESP_ERROR_MSG_INVALID_STRING_TYPE = "ERROR: Entered a non string value  for either location, title or comment"
RESP_ERROR_MSG_INVALID_LOCATION = "Failed to update the incident's location. You provided wrong values.The location field must be a string of two floating values separated by a comma ',', i.e: A latitude and longitude. The latitude must be in the ranges 0 to 90 or -90 to 0. The longitude must be in the ranges 0 to 180 or -180 to 0"
RESP_ERROR_MSG_INVALID_STATUS = ""
RESP_ERROR_MSG_INVALID_INCIDENT = "Entered more or less fields than the required: Required fields include: location, videos, images, title, and comment"
RESP_ERROR_MSG_FORBIDDEN_INCIDENT_UPDATE = "Action is forbidden: Attempting to edit a comment on an edit location endpoint or vice versa"
RESP_ERROR_MSG_ENTERED_NOTHING = "The request body is empty"
RESP_ERROR_MSG_INVALID_EDIT_STRING_TYPE = "The value must be of string type"
RESP_ERROR_MSG_INVALID_EDIT_COMMENT = "Editting comment requires you to input only the comment value"
RESP_SUCCESS_MSG_REGISTRATION = "User successfully signed up"
RESP_SUCCESS_MSG_AUTH_LOGIN = "User successfully logged in"
RESP_SUCCESS_MSG_ADMIN_RIGHTS = "The admin rights of the user have been updated successfully"
RESP_SUCCESS_MSG_CREATE_INCIDENT = "Incident created successfully"
RESP_SUCCESS_MSG_INCIDENT_DELETE = "Incident was deleted successfully"
RESP_SUCCESS_MSG_INCIDENT_UPDATE = "Updated the incident record’s location successfully"
RESP_SUCCESS_MSG_INCIDENT_LIST_EMPTY = "Incidents list is empty"
RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE = "Updated the incident record’s status successfully"


RESP_ERROR_MSG_INVALID_NAME_FIRSTNAME = "You have entered an invalid firstname. Must be from a-z or A-Z"
RESP_ERROR_MSG_INVALID_LASTNAME = "You have entered an invalid lastname. Must be from a-z or A-Z"
RESP_ERROR_MSG_INVALID_OTHERNAMES = "You have entered an invalid other name. Must be from a-z or A-Z"
RESP_ERROR_MSG_INVALID_USERNAME = "Entered an invalid username"
RESP_ERROR_MSG_INVALID_EMAIL = "Entered an invalid email"
RESP_ERROR_MSG_INVALID_LOGIN_CREDS = "Entered an invalid password"
RESP_ERROR_EMPTY_USERNAME = "Enter a empty username"
RESP_ERROR_MSG_EMPTY_PASSWORD = "Enter a empty password"
RESP_ERROR_MSG_LOGIN_FAILED = "Failed to login. username or password is incorrect"
RESP_ERROR_MSG_NO_ACCESS = "You have no rights to view this content"
RESP_ERROR_MSG_INVALID_TITLE = "You entered an invalid title. The minimum number of characters is 20"
RESP_ERROR_MSG_INVALID_IMAGES = "Entered a non list of strings value  for either images"
RESP_ERROR_MSG_INVALID_VIDEOS = "Entered a non list of strings value  for either videos"
RESP_ERROR_MSG_INVALID_COMMENT = "You entered an invalid comment. The minimum number of characters is 100"


RESP_ERROR_NO_ACCESS = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_IMAGES
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_IMAGES = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_IMAGES
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_VIDEOS = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_VIDEOS
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_COMMENT = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_COMMENT
}), content_type="application/json", status=400)

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
    "error": RESP_ERROR_MSG_EMPTY_PASSWORD
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_LOGIN_CREDS = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_LOGIN_CREDS
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_FIRSTNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_NAME_FIRSTNAME
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_LASTNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_LASTNAME
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_OTHERNAMES = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_OTHERNAMES
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_PASSWORD = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_PASSWORD
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_USERNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_USERNAME
}), content_type="application/json", status=400)

# string constants for various responses
RESP_SUCCESS_INCIDENT_LIST_EMPTY = Response(json.dumps({
    "status": 400,
    "data": [],
    "error": RESP_SUCCESS_MSG_INCIDENT_LIST_EMPTY
}), content_type="application/json", status=400)


RESP_ERROR_INVALID_COMMENT_STRING_TYPE = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_EDIT_STRING_TYPE
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_EDIT_COMMENT = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_EDIT_COMMENT
}), content_type="application/json", status=400)

RESP_ERROR_ENTERED_NOTHING = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_ENTERED_NOTHING
}), content_type="application/json", status=400)

RESP_ERROR_FORBIDDEN_INCIDENT_UPDATE = Response(json.dumps({
    "status": 403,
    "error": RESP_ERROR_MSG_FORBIDDEN_INCIDENT_UPDATE
}), content_type="application/json", status=403)

RESP_ERROR_USER_NOT_FOUND = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_USER_NOT_FOUND
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_STRING_TYPE = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_STRING_TYPE
}), content_type="application/json", status=400)

# RESP_ERROR_INVALID_LIST_TYPE = Response(json.dumps({
#     "status": 400,
#     "error": RESP_ERROR_MSG_INVALID_LIST_TYPE
# }), content_type="application/json", status=400)

RESP_ERROR_INVALID_LOCATION = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_LOCATION
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_TITLE = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_TITLE
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_INCIDENT = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_INCIDENT
}), content_type="application/json", status=400)


RESP_ERROR_INVALID_EMAIL = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_EMAIL
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_PHONE = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_PHONE
}), content_type="application/json", status=400)

RESP_ERROR_UNACCEPTABLE_INPUT = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_UNACCEPTABLE_INPUT
}), content_type="application/json", status=400)

RESP_ERROR_POST_EMPTY_DATA = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_EMPTY_STRING
}), content_type="application/json", status=400)

RESP_ERROR_UPDATE_INCIDENT_WRONG_DATA = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_UDATE_WRONG_LOCATION
}), content_type="application/json", status=400)

RESP_ERROR_UPDATE_STATUS = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_UPDATE_STATUS
}), content_type="application/json", status=400)

RESP_ERROR_INCIDENT_NOT_FOUND = Response(json.dumps({
    "status": 404,
    "error": RESP_ERROR_MSG_INCIDENT_NOT_FOUND
}), content_type="application/json", status=404)

RESP_ERROR_POST_DUPLICATE = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INCIDENT_DUPLICATE
}), content_type="application/json", status=400)

RESP_ERROR_ADMIN_NO_RIGHTS = Response(json.dumps({
    "status": 401,
    "error": RESP_ERROR_MSG_ADMIN_NO_RIGHTS
}), content_type="application/json", status=401)

RESP_ERROR_SIGNUP_FAIL_USER_EXISTS = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_SIGNUP_FAIL_USER_EXISTS
}), content_type="application/json", status=400)

RESP_ERROR_BAD_REQUEST = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_BAD_REQUEST
}), content_type="application/json", status=400)

RESP_ERROR_PAGE_NOT = Response(json.dumps({
    "status": 404,
    "error": RESP_ERROR_MSG_PAGE_NOT
}), content_type="application/json", status=404)

RESP_ERROR_METHOD_NOT_ALLOWED = Response(json.dumps({
    "status": 405,
    "error": RESP_ERROR_MSG_METHOD_NOT_ALLOWED
}), content_type="application/json", status=405)

RESP_ERROR_INTERNAL_SERVER_ERROR = Response(json.dumps({
    "status": 500,
    "error": RESP_ERROR_MSG_INTERNAL_SERVER_ERROR
}), content_type="application/json", status=500)

RESP_ERROR_LOGIN_FAILED = Response(json.dumps({
    "status": 401,
    "error": RESP_ERROR_MSG_LOGIN_FAILED
}), content_type="application/json", status=401)

RESP_ERROR_UPDATE_ROLE_FAILED = Response(json.dumps({
    "status": 401,
    "error": RESP_ERROR_MSG_USER_STATUS_NORIGHTS
}), content_type="application/json", status=401)

RESP_ERROR_INVALID_ROLE = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_ROLE
}), content_type="application/json", status=400)

RESP_ERROR_USER_NOT_FOUND = Response(json.dumps({
    "status": 404,
    "error": RESP_ERROR_MSG_USER_NOT_FOUND
}), content_type="application/json", status=404)

RESP_ERROR_UNAUTHORIZED_VIEW = Response(json.dumps({
    "status": 401,
    "error": RESP_ERROR_MSG_UNAUTHORIZED_VIEW
}), content_type="application/json", status=401)

RESP_ERROR_ADMIN_ONLY = Response(json.dumps({
    "status": 401,
    "error": RESP_ERROR_MSG_UNAUTHORIZED_VIEW
}), content_type="application/json", status=401)

RESP_ERROR_INVALID_USER = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_USER
}), content_type="application/json", status=400)

RESP_ERROR_INVALID_OTHERNAME = Response(json.dumps({
    "status": 400,
    "error": RESP_ERROR_MSG_INVALID_OTHERNAMES
}), content_type="application/json", status=400)

# RESP_ERROR_INVALID_NAME = Response(json.dumps({
#     "status": 400,
#     "error": RESP_ERROR_MSG_INVALID_NAME
# }), content_type="application/json", status=400)