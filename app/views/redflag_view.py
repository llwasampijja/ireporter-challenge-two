from flask import Blueprint, request, Response, json
from app.controllers.incident_controller import IncidentController
from app.utilitiez.authenticator import Authenticator

redflag_bp = Blueprint("redflag_bp", __name__)
redflag_controller = IncidentController()
authenticator = Authenticator()

@redflag_bp.route("", methods=["POST"])
@authenticator.concerned_citzen
def create_redflag():
    request_data  = request.get_json()
    return redflag_controller.create_incident(request_data, "redflag")
    
@redflag_bp.route("", methods=["GET"])
@authenticator.authorized
def get_redflags():
    return redflag_controller.get_incidents("redflag")

@redflag_bp.route("/<int:redflag_id>", methods=["GET"])
@authenticator.authorized
def get_flag(redflag_id):
    return redflag_controller.get_incident(redflag_id, "redflag")

@redflag_bp.route("/<int:redflag_id>/location", methods=["PATCH"])
@authenticator.concerned_citzen
def update_redflag(redflag_id):
    request_data = request.get_json()
    username_cookie = request.cookies.get('username')
    
    return redflag_controller.update_incident(redflag_id, request_data, "redflag", username_cookie)
    
@redflag_bp.route("/<int:redflag_id>/status", methods=["PATCH"])
@authenticator.admin_only
def update_redflag_status(redflag_id):
    request_data = request.get_json()
    return redflag_controller.update_incident_status(redflag_id, request_data, "redflag")

@redflag_bp.route("/<int:redflag_id>", methods=["DELETE"])
@authenticator.concerned_citzen
def delete_redflag(redflag_id):
    username_cookie = request.cookies.get('username')
    return redflag_controller.delete_incident(redflag_id, "redflag", username_cookie)
    