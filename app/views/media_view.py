from flask import Blueprint, Response, json, render_template, send_from_directory, request
from app.controllers.media_controller import MediaController

from app.utilities.authenticator import Authenticator
import os.path
from app.utilities.static_strings import BASE_IMAGES_URL

authenticator = Authenticator()
media_blueprint = Blueprint("fileupload_blueprint", __name__)
media_edit_blueprint = Blueprint("fileupload_blueprint", __name__)
media_controller = MediaController()

@media_blueprint.route("images/<string:incident_type>/<int:incident_id>", methods=["PATCH"])
@authenticator.concerned_citzen
def image_upload(incident_type, incident_id):
    if incident_type == "red-flags":
        incident_type = "redflags"
    return media_controller.upload_file(incident_type, incident_id)

@media_blueprint.route("videos/<string:incident_type>/<int:incident_id>", methods=["PATCH"])
@authenticator.concerned_citzen
def video_upload(incident_type, incident_id):
    if incident_type == "red-flags":
        incident_type = "redflags"
    return media_controller.upload_video(incident_type, incident_id)

@media_blueprint.route("/images/<string:image_name>")
def image_view(image_name):
    return send_from_directory('../uploads/images/', image_name), 200


@media_blueprint.route("/videos/<string:video_name>")
def video_view(video_name):
    return send_from_directory('../uploads/videos/', video_name), 200
