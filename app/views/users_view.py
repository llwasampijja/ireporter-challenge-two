"""module with methods and routes for users"""
from flask import Blueprint, request

from app.controllers.users_controller import UsersController
from app.utilitiez.authenticator import Authenticator

user_blueprint = Blueprint("user blueprint", __name__)
users_controller = UsersController()
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
