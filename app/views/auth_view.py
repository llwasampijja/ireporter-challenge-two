"""module includes auth views register and login"""
from flask import Blueprint, request

from app.controllers.users_controller import UsersController

auth_blueprint = Blueprint("auth blueprint", __name__)
users_controller = UsersController()

@auth_blueprint.route("/register", methods=["POST"])
def register():
    """method for registering or signing up a user"""
    request_info = request.get_json()
    return users_controller.adduser(request_info)

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login_user():
    """method for logging in a user"""
    request_info = request.get_json()
    return users_controller.signin(request_info)
