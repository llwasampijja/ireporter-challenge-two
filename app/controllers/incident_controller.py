"""This module contains code which connects the views/routes
of incidents to models"""
import datetime

from flask import request, Response, json
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.models.incident_model import Incident, IncidentData
from app.validators.general_validator import GeneralValidator
from app.utilitiez.static_strings import (
    RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE,
    RESP_SUCCESS_MSG_INCIDENT_DELETE,
    RESP_SUCCESS_MSG_CREATE_INCIDENT,
    RESP_SUCCESS_MSG_INCIDENT_UPDATE,
    RESP_SUCCESS_MSG_INCIDENT_LIST_EMPTY,

    RESP_EEROR_MSG_UNAUTHORIZED_DELETE,
    RESP_ERROR_MSG_UNAUTHORIZED_EDIT,
    
    RESP_ERROR_UNACCEPTABLE_INPUT,
    RESP_ERROR_POST_INCIDENT_WRONG_DATA,
    RESP_ERROR_POST_EMPTY_DATA,
    RESP_ERROR_UPDATE_INCIDENT_WRONG_DATA,
    RESP_ERROR_UPDATE_STATUS,
    RESP_ERROR_INCIDENT_NOT_FOUND,
    RESP_ERROR_POST_DUPLICATE,
    RESP_ERROR_ADMIN_NO_RIGHTS,
    RESP_ERROR_INVALID_STRING_TYPE,
    RESP_ERROR_INVALID_LIST_TYPE,
    RESP_ERROR_INVALID_LOCATION,
    RESP_ERROR_INVALID_INCIDENT
)


class IncidentController:
    "controller class"

    validator = GeneralValidator()
    incident_data = IncidentData()

    def create_incident(self, request_data, keyword):
        """method for creating red-flags"""
        verify_jwt_in_request()
        user_identity = get_jwt_identity()
        created_on = datetime.datetime.now()
        created_by = user_identity["username"]
        location = request_data.get("location")
        status = "pending investigation"
        videos = request_data.get("videos")
        images = request_data.get("images")
        title = request_data.get("title")
        comment = request_data.get("comment")

        strings_turple = (created_by, location, title, comment)
        media_turple = (videos, images)

        get_incidents_instance = self.incident_data.get_incidents(keyword)

        incident_id = self.validator.create_id(
            get_incidents_instance, "incident_id")

        
        if self.response_create_incident_failed(request_data, strings_turple, media_turple):
            return self.response_create_incident_failed(request_data, strings_turple, media_turple)
        elif self.response_invalid_location(location):
            return self.response_invalid_location(location)

        if self.validator.incident_duplicate(comment, get_incidents_instance):
            return RESP_ERROR_POST_DUPLICATE

        new_incident = Incident(
            incident_id=incident_id,
            created_on=created_on,
            created_by=created_by,
            location=location,
            status=status,
            videos=videos,
            images=images,
            title=title,
            comment=comment)
        self.incident_data.create_incident(
            new_incident.incident_dict(keyword), keyword)

        return Response(json.dumps({
            "status": 201,
            "data": [new_incident.incident_dict(keyword)],
            "message": RESP_SUCCESS_MSG_CREATE_INCIDENT
        }), content_type="application/json", status=201)

    def get_incidents(self, keyword):
        """method for getting all incidents"""
        get_incidents_instance = self.incident_data.get_incidents(keyword)
        if not get_incidents_instance:
            return Response(json.dumps({
                "status": 200,
                "data":[],
                "message": RESP_SUCCESS_MSG_INCIDENT_LIST_EMPTY
            }), content_type="application/json", status=200)
        else:
            return Response(json.dumps({
                "status": 200,
                "data": get_incidents_instance
            }), content_type="application/json", status=200)

    def get_incident(self, incident_id, keyword):
        """method for getting a single incident by id"""
        get_incident_instance = self.incident_data.get_incident(
            incident_id, keyword)
        if get_incident_instance is None:
            return RESP_ERROR_INCIDENT_NOT_FOUND
        else:
            return Response(json.dumps({
                "status": 200,
                "data": [get_incident_instance]
            }), content_type="application/json", status=200)

    def update_incident(self, incident_id, request_data, keyword, username):
        """method for editing the location of an incident"""
        location = request_data.get("location")

        for input_value in request_data:
            if input_value not in ["location"]:
                return RESP_ERROR_UNACCEPTABLE_INPUT

        if self.validator.empty_string(location):
            return RESP_ERROR_POST_EMPTY_DATA

        if self.validator.invalid_str_datatype(location) \
        or self.validator.invalid_coordinates(location):
            return RESP_ERROR_UPDATE_INCIDENT_WRONG_DATA
        

        update_incident_instance = self.incident_data.update_incident(
            incident_id, request_data, keyword, username)
        return self.delete_update(
            update_incident_instance,
            RESP_ERROR_MSG_UNAUTHORIZED_EDIT,
            self.response_submission_success(
                update_incident_instance,
                "update"))

    def update_incident_status(self, incident_id, request_data, keyword):
        """method for updating the status of an incident"""
        if "status" not in request_data or len(request_data) != 1:
            return RESP_ERROR_ADMIN_NO_RIGHTS

        if self.validator.invalid_status_value(request_data.get("status")):
            return RESP_ERROR_UPDATE_STATUS

        update_incident_instance = self.incident_data.update_incident(
            incident_id, request_data, keyword, None)
        if update_incident_instance is None:
            return RESP_ERROR_INCIDENT_NOT_FOUND
        else:
            return self.response_submission_success(update_incident_instance,
                                                    "incident_status")

    def delete_incident(self, incident_id, keyword, username):
        """method for deleing an incident basing on its id"""
        delete_incident_instance = self.incident_data.delete_incident(
            incident_id, keyword, username)
        return self.delete_update(
            delete_incident_instance,
            RESP_EEROR_MSG_UNAUTHORIZED_DELETE,
            self.response_submission_success(
                delete_incident_instance,
                "delete"))

    @staticmethod
    def delete_update(action_instance, message_fail, message_success):
        """refactored method for returning the right response for delete
        incident and update location"""
        if action_instance is None:
            return RESP_ERROR_INCIDENT_NOT_FOUND
        elif action_instance in ("non_author", "revoked"):
            return Response(json.dumps({
                "status": 401,
                "message": message_fail
            }), content_type="application/json", status=401)
        else:
            return message_success

    @staticmethod
    def response_submission_success(return_data, keyword):
        """refactored method for returning right response for successful delete and update"""
        if keyword == "delete":
            message = RESP_SUCCESS_MSG_INCIDENT_DELETE
        elif keyword == "incident_status":
            message = RESP_SUCCESS_MSG_INCIDENT_STATUS_UPDATE
        else:
            message = RESP_SUCCESS_MSG_INCIDENT_UPDATE
        return Response(json.dumps({
            "status": 201,
            "data": [return_data],
            "message": message
        }), content_type="application/json", status=201)

    @staticmethod
    def response_create_incident_failed(request_data, strings_turple, media_turple):
        valid_incidents = (
            "location",
            "videos",
            "images",
            "title",
            "comment")
        if GeneralValidator.invalid_item(request_data, valid_incidents, valid_incidents):
            return RESP_ERROR_INVALID_INCIDENT
        elif any(GeneralValidator.empty_string(item) for item in strings_turple):
            return RESP_ERROR_POST_EMPTY_DATA
        elif any(GeneralValidator.invalid_str_datatype(item) for item in strings_turple):
            return RESP_ERROR_INVALID_STRING_TYPE
        elif any(GeneralValidator.invalid_list_datatype(item) for item in media_turple):
            return RESP_ERROR_INVALID_LIST_TYPE

    def response_invalid_location(self, location):
        if self.validator.invalid_coordinates(location):
            return RESP_ERROR_INVALID_LOCATION

