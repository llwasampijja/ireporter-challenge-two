"""module includes routes for the intervention incidents"""
from flask import Blueprint, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.utilities.authenticator import Authenticator
from app.models.incident_model import Incident, IncidentData

intervention_blueprint = Blueprint("intervention_blueprint", __name__)

authenticator = Authenticator()
incident_data = IncidentData()
incident_instance = Incident()


@intervention_blueprint.route("", methods=["POST"])
@authenticator.concerned_citzen
def create_intervention():
    """method with route for creating an intervention incident"""
    request_data = request.get_json()
    return incident_instance.create_incident(request_data, "intervention", "interventions")


@intervention_blueprint.route("", methods=["GET"])
@authenticator.authorized
def get_interventions():
    """method with route for getting all the intervention incidents"""
    return incident_data.get_incidents("interventions")

@intervention_blueprint.route("/<int:intervention_id>", methods=["GET"])
@authenticator.authorized
def get_intervention(intervention_id):
    """method with route for getting an intervention incident by id"""
    verify_jwt_in_request()
    user_identity = get_jwt_identity()
    return incident_instance.get_incident(intervention_id, "intervention", "get", user_identity["user_id"], "interventions")


@intervention_blueprint.route("/<int:intervention_id>/location", methods=["PATCH"])
@authenticator.concerned_citzen
def update_intervention_location(intervention_id):
    """method with route for updating the location of an intervention incident"""
    request_data = request.get_json()
    verify_jwt_in_request()
    user_identity = get_jwt_identity()
    return incident_instance.edit_incident_location(request_data, intervention_id, "intervention", user_identity["user_id"], "interventions")


@intervention_blueprint.route("/<int:intervention_id>/comment", methods=["PATCH"])
@authenticator.concerned_citzen
def update_intervention_comment(intervention_id):
    request_data = request.get_json()
    verify_jwt_in_request()
    user_identity = get_jwt_identity()
    return incident_instance.edit_incident_comment(request_data, intervention_id, "intervention",user_identity["user_id"], "interventions")



@intervention_blueprint.route("/<int:intervention_id>/status", methods=["PATCH"])
@authenticator.admin_only
def update_intervention_status(intervention_id):
    """method with route for updting status of an intervention incident"""
    request_data = request.get_json()
    verify_jwt_in_request()
    user_identity = get_jwt_identity()
    return incident_instance.edit_incident_status(request_data, intervention_id, "intervention", user_identity["user_id"], "interventions")



@intervention_blueprint.route("/<int:intervention_id>", methods=["DELETE"])
@authenticator.concerned_citzen
def delete_intervention(intervention_id):
    """method with route for deleting an intervention incident"""
    verify_jwt_in_request()
    user_identity = get_jwt_identity()
    return incident_instance.delete_incident( intervention_id, "intervention", user_identity["user_id"], "interventions")
