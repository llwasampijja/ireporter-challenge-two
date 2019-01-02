from flask import Blueprint, json, Response, request
from app.controllers.incident_controller import IncidentController
from app.authenticator import Authenticator

interventionController = IncidentController()
intervention_bp = Blueprint("intervention_bp", __name__)

authenticator = Authenticator()

@intervention_bp.route("", methods=["POST"])
@authenticator.concerned_citzen
def create_intervention():
    request_data = request.get_json()
    return interventionController.create_incident(request_data, "intervention")

@intervention_bp.route("", methods=["GET"])
@authenticator.authorized
def get_interventions():
    return interventionController.get_incidents("intervention")

@intervention_bp.route("/<int:intervention_id>", methods=["GET"])
@authenticator.authorized
def get_intervention(intervention_id):
    return interventionController.get_incident(intervention_id, "intervention")

@intervention_bp.route("/<int:intervention_id>/location", methods=["PATCH"])
@authenticator.concerned_citzen
def update_intervention(intervention_id):
    request_data = request.get_json()
    username_cookie = request.cookies.get('username')
    return interventionController.update_incident(intervention_id, request_data, "intervention", username_cookie)