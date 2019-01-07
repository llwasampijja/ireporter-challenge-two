"""this module includes all strings which are constant accross the app"""
# url string constants for users and authentication
URL_REGISTER = "/api/v1/auth/register"
URL_LOGIN = "/api/v1/auth/login"
URL_USERS = "/api/v1/users"

# url string constants for incidents
URL_REDFLAGS = "/api/v1/red-flags"
URL_INTERVENTIONS = "/api/v1/interventions"

# swagger url string constants
SWAGGER_UI_URL = "/api/v1/docs"
# remote API documenation url
API_URL = "https://llwasampijja.github.io/ireporter-challenge-two/ireporter_challenge_two.json"
# API_URL =
# "http://localhost/swagger-ui/dist/ireporter_challenge_two.json" #local
# API documentation url

# string constants for responses
RESP_EMPTY_STRING = "No empty fields are allowed"
RESP_INVALID_USER_INPUT = "An invalid user or Wrong datatype entered"
RESP_EMPTY_INVALID_EMAIL_PASSWORD_PHONE = "Entered an empty field or \
an invalid email address, phonenumber or password"
RESP_ALREADY_TAKEN = "Email address or username is already taken"
RESP_REGISTRATION_SUCCESS = "User account created successifully"
RESP_REGISTRATION_FAILED = "Failed to login, username or password is incorrect"
RESP_ADMIN_RIGHTS_SUCCESS = "The admin rights of the user have been updated successifully"
RESP_ROLE_INVALID = "The value can either be true (admin) or false (not admin)"
RESP_ROLE_NO_RIGHTS = "An administrator can only edit a user's role"
RESP_USER_NOT_FOUND = "That specified user wasn't found on the system"
RESP_USER_STATUS_NORIGHTS = "An admin can only edit the status of an incident, \
nothing more. The only accepted values include: 'pending investigation', 'resolved' and 'rejected'"
RESP_CREATE_INCIDENT_SUCCESS = "Incident created successifully"
RESP_INVALID_INCIDENT_INPUT = "Unaccepted datatype or Inavlid incident"
RESP_INCIDENT_NOT_FOUND = "No incident of that specific id found"
RESP_UNAUTHORIZED_VIEW = "You are not authorised to access this content"
RESP_UNAUTHORIZED_EDIT = "You are not authorised to edit this incident."
RESP_UNAUTHORIZED_DELETE = "You are not authorised to delete this incident"
RESP_INCIDENT_UPDATE_SUCCESS = "Updated incident record’s location"
RESP_INCIDENT_LIST_EMPTY = "incidents list is empty"
RESP_INCIDENT_STATUS_UPDATE_SUCCESS = "Updated incident record’s status"
RESP_INCIDENT_WROND_STATUS = "Wrong Status given"
RESP_ADMIN_ONLY = "This feature is only available to adminitrators"
RESP_INCIDENT_DELETE_SUCCESS = "Incident deleted successfully"
RESP_INCIDENT_DUPLICATE = "Creating a dupplicate incident isn't allowed"

# error response string constants
RESP_ERROR_BAD_REQUEST = "Bad request, check your input and try again"
RESP_ERRO_PAGE_NOT = "No such page on this site"
RESP_ERROR_METHOD_NOT_ALLOWED = "method not allowed"

RESP_AUTH_LOGIN_SUCCESS = "Logged in successifully"
RESP_AUTH_LOGIN_FAILED = "Failed to login, username or password is incorrect"
