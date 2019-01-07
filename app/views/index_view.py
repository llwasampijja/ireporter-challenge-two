
"""module with route for the index page"""
from flask import Blueprint, Response, json
from app.utilitiez.static_strings import RESP_INDEX_MESSAGE, WELCOME_MSG

index_blueprint = Blueprint("index blueprint", __name__)

@index_blueprint.route("")
def index_page():
    """method and route to the index page endpoint"""
    return Response(json.dumps({
        "status": 200,
        "message": WELCOME_MSG,
        "data": [RESP_INDEX_MESSAGE]
    }), content_type="application/json", status=200)
