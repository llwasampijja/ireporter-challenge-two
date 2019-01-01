from flask import Blueprint, request, Response, json
from app.controllers.incident_controller import IncidentController

redflag_bp = Blueprint("redflag_bp", __name__)
redflag_controller = IncidentController()

@redflag_bp.route("", methods=["POST"])
def create_redflag():
    request_data  = request.get_json()
    return redflag_controller.create_incident(request_data, "redflag")
    
@redflag_bp.route("", methods=["GET"])
def get_redflags():
    return redflag_controller.get_incidents("redflag")

@redflag_bp.route("/<int:redflag_id>", methods=["GET"])
def get_flag(redflag_id):
    return redflag_controller.get_incident(redflag_id, "redflag")

@redflag_bp.route("/<int:redflag_id>/location", methods=["PATCH"])
def update_redflag(redflag_id):
    request_data = request.get_json()
    username_cookie = request.cookies.get('username')
    
    return redflag_controller.update_incident(redflag_id, request_data, "redflag", username_cookie)
    
@redflag_bp.route("/<int:redflag_id>/status", methods=["PATCH"])
def update_redflag_status(redflag_id):
    # if not request.headers.get("Authorization"):
    #     return Response(json.dumps({
    #         "message":"must supply authorization header"
    #     }))
    request_data = request.get_json()
    return redflag_controller.update_incident_status(redflag_id, request_data, "redflag")

@redflag_bp.route("/<int:redflag_id>", methods=["DELETE"])
def delete_redflag(redflag_id):
    username_cookie = request.cookies.get('username')
    return redflag_controller.delete_incident(redflag_id, "redflag", username_cookie)
    