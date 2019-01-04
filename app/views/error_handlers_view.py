from flask import Blueprint, Response, json

def bad_request_error(error):
    return Response(json.dumps({
        "status": 400,
        "message": "Bad request, check your input and try again"
    }), content_type="application/json", status=400)
    
def page_not_found(error):
    return Response(json.dumps({
        "status": 404,
        "message":"No such page on this site"
    }), content_type="application/json", status=404)

def method_not_allowed(error):
    return Response(json.dumps({
        "status": 405,
        "message": "method not allowed"
    }), content_type="application/json", status=405)
