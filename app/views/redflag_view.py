"""module including routes for the red-flags incidents"""
from flask import Blueprint, request, Response, json
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.controllers.incident_controller import IncidentController
from app.utilities.authenticator import Authenticator
from app.models.incident_model import Incident, IncidentData

redflag_blueprint = Blueprint("redflag blueprint", __name__)
redflag_controller = IncidentController()
authenticator = Authenticator()
incident_data = IncidentData()
incident_instance = Incident()


@redflag_blueprint.route("", methods=["POST"])
@authenticator.concerned_citzen
def create_redflag():
    """method and route for creating an red-flag incident"""
    request_data = request.get_json()
    return redflag_controller.create_incident(request_data, "redflag", "redflags")
    # return incident_instance.create_incident(request_data, "redflag", "redflags")


@redflag_blueprint.route("", methods=["GET"])
@authenticator.authorized
def get_redflags():
    """method and route for getting all red-flag incidents"""
    # return redflag_controller.get_incidents("redflag", "redflags")
    return Response(json.dumps({
        "status": 200,
        "data": incident_data.get_all_dbincidents("redflag", "redflags")
    }), content_type="application/json", status=200)
    # return 

@redflag_blueprint.route("/<int:redflag_id>", methods=["GET"])
@authenticator.authorized
def get_flag(redflag_id):
    """method and route for getting a red-flag inciden by id"""
    # return redflag_controller.get_incident(redflag_id, "redflag", "redflags")
    return incident_instance.get_incident(redflag_id, "redflag", "redflags")


@redflag_blueprint.route("/<int:redflag_id>/location", methods=["PATCH"])
@authenticator.concerned_citzen
def update_redflag_location(redflag_id):
    """method for updating location of red-flag incident by id"""
    request_data = request.get_json()
    verify_jwt_in_request()
    return redflag_controller.update_incident(
        redflag_id, request_data, "redflag", get_jwt_identity()["username"],
        "edit_location", "redflags"
    )

@redflag_blueprint.route("<int:redflag_id>/comment", methods=["PATCH"])
@authenticator.concerned_citzen
def update_redflag_comment(redflag_id):
    """method for updating the comment of a redflag"""
    request_data = request.get_json()
    verify_jwt_in_request()
    return redflag_controller.update_incident(
        redflag_id, request_data, "redflag", get_jwt_identity()["username"],
        "edit_comment", "redflags"
    )

@redflag_blueprint.route("/<int:redflag_id>/status", methods=["PATCH"])
@authenticator.admin_only
def update_redflag_status(redflag_id):
    """method and route for updating the status a red-flag incident by id"""
    request_data = request.get_json()
    return redflag_controller.update_incident_status(
        redflag_id, request_data, "redflag", "redflags"
    )


@redflag_blueprint.route("/<int:redflag_id>", methods=["DELETE"])
@authenticator.concerned_citzen
def delete_redflag(redflag_id):
    """method and route for deleting a red-flag incident by id"""
    verify_jwt_in_request()
    return redflag_controller.delete_incident(
        redflag_id, "redflag", get_jwt_identity()["username"], "redflags"
    )
