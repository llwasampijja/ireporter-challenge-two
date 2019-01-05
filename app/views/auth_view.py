from flask import Blueprint, request

from app.controllers.users_controller import UsersController

auth_bp = Blueprint("auth bp", __name__)
users_controller = UsersController()

@auth_bp.route("/register", methods=["POST"])
def register():
    request_info = request.get_json()
    return users_controller.adduser(request_info)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_user():
    request_info = request.get_json()
    return users_controller.signin(request_info)