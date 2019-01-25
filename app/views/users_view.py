"""module with methods and routes for users"""
from flask import Blueprint, request

from app.controllers.users_controller import UsersController
from app.controllers.incident_controller import IncidentController
from app.utilities.authenticator import Authenticator
from app.utilities.static_strings import RESP_ERROR_UNAUTHORIZED_VIEW


user_blueprint = Blueprint("user blueprint", __name__)
users_controller = UsersController()
incident_controller = IncidentController()
authenticator = Authenticator()

@user_blueprint.route("", methods=["GET"])
@authenticator.admin_only
def get_users():
    """method and route for getting all users"""
    return users_controller.get_users()

@user_blueprint.route("/<int:user_id>", methods=["PATCH"])
@authenticator.admin_only
def update_user(user_id):
    """method and route for updating the role of a user"""
    request_data = request.get_json()
    return users_controller.update_user_role(user_id, request_data)

@user_blueprint.route("/<int:user_id>/interventions", methods=["GET"])
@authenticator.authorized
def get_interventions_for_user(user_id):
    """method and route for getting all intervention incidents for a particular user"""
    return incident_controller.get_incidents_specific_user(user_id, "interventions")

@user_blueprint.route("<int:user_id>/red-flags", methods=["GET"])
@authenticator.authorized
def get_redflags_user(user_id):
    """method and route for getting all red-flag incidents for a particular user"""
    return incident_controller.get_incidents_specific_user(user_id, "redflags")