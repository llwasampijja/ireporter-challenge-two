from flask import Blueprint, request, Response, json
from app.controllers.users_controller import UsersController
from app.authenticator import Authenticator

user_bp = Blueprint("user_bp", __name__)
users_controller = UsersController()
authenticator = Authenticator()

@user_bp.route("", methods=["GET"])
@authenticator.admin_only
def get_users():
    return users_controller.get_users()

@user_bp.route("/register", methods=["POST"])
def register():
    request_info = request.get_json()
    return users_controller.adduser(request_info)

@user_bp.route("/login", methods=["GET", "POST"])
def login_user():
    request_info = request.get_json()
    return users_controller.signin(request_info)

@user_bp.route("/<int:user_id>", methods=["PATCH"])
@authenticator.admin_only
def update_user(user_id):
    request_data = request.get_json()
    return users_controller.update_user_role(user_id, request_data)
