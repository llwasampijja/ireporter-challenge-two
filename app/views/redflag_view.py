from flask import Blueprint, request
from app.controllers.redflag_controller import RedflagController

redflag_bp = Blueprint("redflag_bp", __name__)
redflag_controller = RedflagController()

@redflag_bp.route("", methods=["POST"])
def create_redflag():
    request_data  = request.get_json()
    return redflag_controller.create_redflag(request_data)
    
@redflag_bp.route("", methods=["GET"])
def get_redflags():
    return redflag_controller.get_reflags()

@redflag_bp.route("/<int:redflag_id>", methods=["GET"])
def get_flag(redflag_id):
    return redflag_controller.get_redflag(redflag_id)

@redflag_bp.route("/<int:redflag_id>/location", methods=["PATCH"])
def update_redflag(redflag_id):
    request_data = request.get_json()
    return redflag_controller.update_redflag(redflag_id, request_data)
    

@redflag_bp.route("/<int:redflag_id>", methods=["DELETE"])
def delete_redflag(redflag_id):
    return redflag_controller.delete_redflag(redflag_id)