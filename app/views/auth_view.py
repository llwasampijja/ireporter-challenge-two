"""module includes auth views register and login"""
from flask import Blueprint, request

from app.models.user_model import User, UsersData

auth_blueprint = Blueprint("auth blueprint", __name__)
user_instance = User()

@auth_blueprint.route("/register", methods=["POST"])
def register():
    """method for registering or signing up a user"""
    request_info = request.get_json()
    return user_instance.create_user(request_info)

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login_user():
    """method for logging in a user"""
    request_info = request.get_json()
    return user_instance.login_user(request_info)
