"""This module contains code which connects the views/routes
of incidents to models"""
import datetime

from flask import request, Response, json

from app.models.incident_model import Incident, IncidentData
from app.validators.general_validator import GeneralValidator
from app.utilitiez.static_strings import (
    RESP_USER_STATUS_NORIGHTS,
    RESP_INCIDENT_DUPLICATE,
    RESP_INCIDENT_STATUS_UPDATE_SUCCESS,
    RESP_INCIDENT_DELETE_SUCCESS,
    RESP_INVALID_INCIDENT_INPUT,
    RESP_EMPTY_STRING,
    RESP_INCIDENT_WROND_STATUS,
    RESP_UNAUTHORIZED_DELETE,
    RESP_UNAUTHORIZED_EDIT,
    RESP_CREATE_INCIDENT_SUCCESS,
    RESP_INCIDENT_UPDATE_SUCCESS,
    RESP_INCIDENT_LIST_EMPTY,
    RESP_INCIDENT_NOT_FOUND)


class IncidentController:
    "controller class"

    validator = GeneralValidator()
    incident_data = IncidentData()

    def create_incident(self, request_data, keyword):
        """method for creating red-flags"""
        created_on = datetime.datetime.now()
        created_by = request.cookies.get('username')
        location = request_data.get("location")
        status = "pending investigation"
        videos = request_data.get("videos")
        images = request_data.get("images")
        title = request_data.get("title")
        comment = request_data.get("comment")

        args_strings = [created_by, location, title, comment]
        args_list = [videos, images]

        get_incidents_instance = self.incident_data.get_incidents(keyword)

        incident_id = self.validator.create_id(
            get_incidents_instance, "incident_id")

        if any(self.validator.check_empty_string(item) for item in
               args_strings):
            return self.response_unaccepted("empty")

        if any(self.validator.check_str_datatype(item) for item in args_strings)\
                or self.validator.invalid_incident(request_data)\
                or any(self.validator.check_list_datatype(item) for item in args_list)\
                or self.validator.invalid_coordinates(location):
            return self.response_unaccepted("datatype")

        if self.validator.incident_duplicate(comment, get_incidents_instance):
            return Response(json.dumps({
                "status": 400,
                "message": RESP_INCIDENT_DUPLICATE
            }), content_type="application/json", status=400)

        # if self.validator.check_status_value(status):
        #     return self.response_unaccepted("status")

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
            "message": RESP_CREATE_INCIDENT_SUCCESS
        }), content_type="application/json", status=201)

    def get_incidents(self, keyword):
        """method for getting all incidents"""
        get_incidents_instance = self.incident_data.get_incidents(keyword)
        if not get_incidents_instance:
            return Response(json.dumps({
                "status": 200,
                "message": RESP_INCIDENT_LIST_EMPTY
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
            return Response(json.dumps({
                "status": 404,
                "message": RESP_INCIDENT_NOT_FOUND
            }), content_type="application/json", status=404)
        else:
            return Response(json.dumps({
                "status": 200,
                "data": [get_incident_instance]
            }), content_type="application/json", status=200)

    def update_incident(self, incident_id, request_data, keyword, username):
        """method for editing the location of an incident"""
        location = request_data.get("location")

        if self.validator.check_empty_string(location):
            return self.response_unaccepted("empty")

        if self.validator.check_str_datatype(location):
            return self.response_unaccepted("datatype")

        update_incident_instance = self.incident_data.update_incident(
            incident_id, request_data, keyword, username)
        return self.delete_update(
            update_incident_instance,
            RESP_UNAUTHORIZED_EDIT,
            self.response_sumission_success(
                update_incident_instance,
                "update"))

    def update_incident_status(self, incident_id, request_data, keyword):
        """method for updating the status of an incident"""
        # if "status" not in request_data or len(request_data) != 1 or
        # self.validator.check_status_value(request_data.get("status")):
        if "status" not in request_data or len(request_data) != 1:
            return Response(json.dumps({
                "status": 401,
                "message": RESP_USER_STATUS_NORIGHTS
            }), content_type="application/json", status=401)

        if self.validator.check_status_value(request_data.get("status")):
            return self.response_unaccepted("status")

        update_incident_instance = self.incident_data.update_incident(
            incident_id, request_data, keyword, None)
        if update_incident_instance is None:
            return self.response_unaccepted("none")
        else:
            return self.response_sumission_success(update_incident_instance,
                                                   "incident_status")

    def delete_incident(self, incident_id, keyword, username):
        """method for deleing an incident basing on its id"""
        delete_incident_instance = self.incident_data.delete_incident(
            incident_id, keyword, username)
        return self.delete_update(
            delete_incident_instance,
            RESP_UNAUTHORIZED_DELETE,
            self.response_sumission_success(
                delete_incident_instance,
                "delete"))

    def delete_update(self, action_instance, message_fail, message_success):
        """refactored method for returning the right response for delete
        incident and update location"""
        if action_instance is None:
            return self.response_unaccepted("none")
        elif action_instance == "non_author":
            return Response(json.dumps({
                "status": 401,
                "message": message_fail
            }), content_type="application/json", status=401)
        else:
            return message_success

    @staticmethod
    def response_unaccepted(word):
        """refactored method for returning right status codes and messages"""
        if word == "none":
            status_code = 404
            message = RESP_INCIDENT_NOT_FOUND
        elif word == "status":
            status_code = 400
            message = RESP_INCIDENT_WROND_STATUS
        elif word == "empty":
            status_code = 400
            message = RESP_EMPTY_STRING
        else:
            status_code = 400
            message = RESP_INVALID_INCIDENT_INPUT
        return Response(json.dumps({
            "status": status_code,
            "message": message
        }), content_type="application/json", status=status_code)

    @staticmethod
    def response_sumission_success(return_data, keyword):
        """refactored method for returning right response for successful delete and update"""
        if keyword == "delete":
            message = RESP_INCIDENT_DELETE_SUCCESS
        elif keyword == "incident_status":
            message = RESP_INCIDENT_STATUS_UPDATE_SUCCESS
        else:
            message = RESP_INCIDENT_UPDATE_SUCCESS
        return Response(json.dumps({
            "status": 201,
            "data": [return_data],
            "message": message
        }), content_type="application/json", status=201)
