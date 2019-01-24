"""module including routes for the red-flags incidents"""
from flask import Blueprint, request, Response, json
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.utilities.authenticator import Authenticator
from app.models.incident_model import Incident, IncidentData
from app.utilities.static_strings import (
    RESP_SUCCESS_INCIDENT_LIST_EMPTY
)


redflag_blueprint = Blueprint("redflag blueprint", __name__)
authenticator = Authenticator()
incident_data = IncidentData()
incident_instance = Incident()


@redflag_blueprint.route("", methods=["POST"])
@authenticator.concerned_citzen
def create_redflag():
    """method and route for creating an red-flag incident"""
    request_data = request.get_json()
    return incident_instance.create_incident(request_data, "redflag", "redflags")


@redflag_blueprint.route("", methods=["GET"])
@authenticator.authorized
def get_redflags():
    """method and route for getting all red-flag incidents"""
    return incident_data.get_incidents("redflags")

@redflag_blueprint.route("/<int:redflag_id>", methods=["GET"])
@authenticator.authorized
def get_flag(redflag_id):
    """method and route for getting a red-flag inciden by id"""
    return incident_instance.get_incident(redflag_id, "redflag", "get", "edward", "redflags")


@redflag_blueprint.route("/<int:redflag_id>/location", methods=["PATCH"])
@authenticator.concerned_citzen
def update_redflag_location(redflag_id):
    """method for updating location of red-flag incident by id"""
    request_data = request.get_json()
    verify_jwt_in_request()
    return incident_instance.edit_incident_location(request_data, redflag_id, "redflag", 2, "redflags")

@redflag_blueprint.route("<int:redflag_id>/comment", methods=["PATCH"])
@authenticator.concerned_citzen
def update_redflag_comment(redflag_id):
    """method for updating the comment of a redflag"""
    request_info = request.get_json()
    verify_jwt_in_request()
    return incident_instance.edit_incident_comment(request_info, redflag_id, "redflag", 2, "redflags")

@redflag_blueprint.route("/<int:redflag_id>/status", methods=["PATCH"])
@authenticator.admin_only
def update_redflag_status(redflag_id):
    """method and route for updating the status a red-flag incident by id"""
    request_data = request.get_json()
    return incident_instance.edit_incident_status(request_data, redflag_id, "redflag", 2, "redflags")


@redflag_blueprint.route("/<int:redflag_id>", methods=["DELETE"])
@authenticator.concerned_citzen
def delete_redflag(redflag_id):
    """method and route for deleting a red-flag incident by id"""
    verify_jwt_in_request()
    user_identity = get_jwt_identity()
    return incident_instance.delete_incident( redflag_id, "redflag", 2, "redflags")

