from flask import Blueprint
from app.controllers.redflag_controller import RedflagController

redflag_bp = Blueprint("redflag_bp", __name__)
redflagController = RedflagController()

@redflag_bp.route("", methods=["POST"])
def create_redflag():
    return redflagController.create_redflag()
    
@redflag_bp.route("", methods=["GET"])
def get_redflags():
    return redflagController.get_reflags()