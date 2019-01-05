from flask import Blueprint, Response, json

from app.utilitiez.static_strings import RESP_ERRO_PAGE_NOT, RESP_ERROR_BAD_REQUEST, RESP_ERROR_METHOD_NOT_ALLOWED

def bad_request_error(error):
    return Response(json.dumps({
        "status": 400,
        "message": RESP_ERROR_BAD_REQUEST
    }), content_type="application/json", status=400)
    
def page_not_found(error):
    return Response(json.dumps({
        "status": 404,
        "message": RESP_ERRO_PAGE_NOT
    }), content_type="application/json", status=404)

def method_not_allowed(error):
    return Response(json.dumps({
        "status": 405,
        "message": RESP_ERROR_METHOD_NOT_ALLOWED
    }), content_type="application/json", status=405)
