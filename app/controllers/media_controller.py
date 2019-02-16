"""This module contains code which connects the views/routes
of incidents to models"""
import datetime

import os

from flask import request, Response, json, redirect, url_for
from werkzeug.utils import secure_filename

from app.utilities.authenticator import Authenticator
from app.models.incident_model import Incident, IncidentData
from app.controllers.users_controller import UsersController
from app.validators.general_validator import GeneralValidator
from databases.ireporter_db import IreporterDb
from app.utilities.static_strings import (
    BASE_IMAGES_URL,
    BASE_VIDEOS_URL,
    RESP_ERROR_NO_FILE_UPLOADED,
    RESP_ERROR_FILE_UPLOAD_ERROR
)

class MediaController:
    "controller class"

    validator = GeneralValidator()
    incident_data = IncidentData()
    users_controller = UsersController()
    authenticator = Authenticator()
    ireporter_db = IreporterDb()

    def upload_file(self, incident_type, incident_id):
        if request.method == 'PATCH':
            myTemp = request.files
            if 'images' not in myTemp:
                return RESP_ERROR_NO_FILE_UPLOADED
            file = request.files['images']
            if file.filename == '':
                return RESP_ERROR_FILE_UPLOAD_ERROR
            if file and self.validator.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join("./uploads/images/", filename))
                image_url = BASE_IMAGES_URL + filename
                self.ireporter_db.update_data_incident_image(incident_id, image_url, incident_type)
                return Response(json.dumps({
                    "status": 201,
                    "data": [filename],
                    "message": "Image uploaded Successfully"
                }))

    def upload_video(self, incident_type, incident_id):
        if request.method == 'PATCH':
            myTemp = request.files
            if 'videos' not in myTemp:
                return RESP_ERROR_NO_FILE_UPLOADED
            file = request.files['videos']
            if file.filename == '':
                return RESP_ERROR_FILE_UPLOAD_ERROR
            if file and self.validator.allowed_video_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join("./uploads/videos/", filename))
                video_url = BASE_VIDEOS_URL + filename
                self.ireporter_db.update_data_incident_video(incident_id, video_url, incident_type)
                return Response(json.dumps({
                    "status": 201,
                    "data": [filename],
                    "message": "Video uploaded Successfully"
                }))