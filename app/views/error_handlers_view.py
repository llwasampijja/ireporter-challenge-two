"""module with routes or views for error handling"""
from flask import Response, json

from app.utilitiez.static_strings import (
    RESP_ERRO_PAGE_NOT,
    RESP_ERROR_BAD_REQUEST,
    RESP_ERROR_METHOD_NOT_ALLOWED,
    RESP_INTERNAL_SERVER_ERROR
)

def bad_request_error(error):
    """method for handling bad requests errors"""
    return Response(json.dumps({
        "status": 400,
        "message": RESP_ERROR_BAD_REQUEST
    }), content_type="application/json", status=400)

def page_not_found(error):
    """method for handling page not found errors"""
    return Response(json.dumps({
        "status": 404,
        "message": RESP_ERRO_PAGE_NOT
    }), content_type="application/json", status=404)

def method_not_allowed(error):
    """method for handling 'http method not allowed errors"""
    return Response(json.dumps({
        "status": 405,
        "message": RESP_ERROR_METHOD_NOT_ALLOWED
    }), content_type="application/json", status=405)

def internal_server_error(error):
    """method for handling internal server errors"""
    return Response(json.dumps({
        "status": 500,
        "message": RESP_INTERNAL_SERVER_ERROR
    }), content_type="application/json", status=500)
