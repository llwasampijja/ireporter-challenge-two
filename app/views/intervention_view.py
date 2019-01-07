"""module includes routes for the intervention incidents"""
from flask import Blueprint, request

from app.controllers.incident_controller import IncidentController
from app.utilitiez.authenticator import Authenticator

interventionController = IncidentController()
intervention_blueprint = Blueprint("intervention_blueprint", __name__)

authenticator = Authenticator()


@intervention_blueprint.route("", methods=["POST"])
@authenticator.concerned_citzen
def create_intervention():
    """method with route for creating an intervention incident"""
    request_data = request.get_json()
    return interventionController.create_incident(request_data, "intervention")


@intervention_blueprint.route("", methods=["GET"])
@authenticator.authorized
def get_interventions():
    """method with route for getting all the intervention incidents"""
    return interventionController.get_incidents("intervention")


@intervention_blueprint.route("/<int:intervention_id>", methods=["GET"])
@authenticator.authorized
def get_intervention(intervention_id):
    """method with route for getting an intervention incident by id"""
    return interventionController.get_incident(
        intervention_id, "intervention"
    )


@intervention_blueprint.route("/<int:intervention_id>/location", methods=["PATCH"])
@authenticator.concerned_citzen
def update_intervention(intervention_id):
    """method with route for updating the location of an intervention incident"""
    request_data = request.get_json()
    username_cookie = request.cookies.get('username')
    return interventionController.update_incident(
        intervention_id, request_data, "intervention", username_cookie
    )


@intervention_blueprint.route("/<int:intervention_id>/status", methods=["PATCH"])
@authenticator.admin_only
def update_intervention_status(intervention_id):
    """method with route for updating status of an intervention incident"""
    request_data = request.get_json()
    return interventionController.update_incident_status(
        intervention_id, request_data, "intervention"
    )


@intervention_blueprint.route("/<int:intervention_id>", methods=["DELETE"])
@authenticator.concerned_citzen
def delete_intervention(intervention_id):
    """method with route for deleting an intervention incident"""
    username_cookie = request.cookies.get('username')
    return interventionController.delete_incident(
        intervention_id, "intervention", username_cookie
    )
