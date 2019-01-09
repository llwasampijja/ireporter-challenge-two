"""module with routes or views for error handling"""

from app.utilitiez.static_strings import (
    RESP_ERROR_PAGE_NOT,
    RESP_ERROR_BAD_REQUEST,
    RESP_ERROR_METHOD_NOT_ALLOWED,
    RESP_ERROR_INTERNAL_SERVER_ERROR
)

def bad_request_error(error):
    """method for handling bad requests errors"""
    return RESP_ERROR_BAD_REQUEST

def page_not_found(error):
    """method for handling page not found errors"""
    return RESP_ERROR_PAGE_NOT

def method_not_allowed(error):
    """method for handling 'http method not allowed errors"""
    return RESP_ERROR_METHOD_NOT_ALLOWED

def internal_server_error(error):
    """method for handling internal server errors"""
    return RESP_ERROR_INTERNAL_SERVER_ERROR
