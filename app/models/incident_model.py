"""module containing models and data methods for incidents"""
import datetime

from flask import json, Response

from app.models.user_model import UsersData
from app.utilities.authenticator import Authenticator
from databases.ireporter_db import IreporterDb

from app.utilities.static_strings import (
    RESP_SUCCESS_INCIDENT_LIST_EMPTY,
    RESP_ERROR_INCIDENT_NOT_FOUND,
    RESP_SUCCESS_MSG_INCIDENT_DELETE,
    RESP_ERROR_INVALID_COMMENT_STRING_TYPE,
    RESP_ERROR_POST_DUPLICATE,
    RESP_SUCCESS_MSG_INCIDENT_UPDATE_COMMENT,
    RESP_ERROR_INVALID_LOCATION,
    RESP_ERROR_UPDATE_STATUS,
    RESP_SUCCESS_MSG_INCIDENT_UPDATE_STATUS,
    RESP_SUCCESS_MSG_INCIDENT_UPDATE_LOCATION,
    RESP_SUCCESS_MSG_CREATE_INCIDENT,
    RESP_ERROR_MSG_NO_ACCESS,
    RESP_ERROR_INVALID_EMAIL,
    RESP_ERROR_INVALID_INCIDENT,
    RESP_ERROR_INVALID_TITLE,
    RESP_ERROR_INVALID_IMAGES,
    RESP_ERROR_INVALID_VIDEOS,
    RESP_ERROR_INVALID_COMMENT,
    RESP_ERROR_NO_ACCESS,
    RESP_ERROR_MSG_EMPTY_STRING
    
)

class Incident:
    ireporter_db = IreporterDb()
    authenticator = Authenticator()

    def create_incident(self, request_info, keyword, table_name):
        user_identity = self.authenticator.get_identity(self.authenticator.get_token())
        if any(self.empty_string(user_input) for key_, user_input in request_info.items()):
            return RESP_ERROR_MSG_EMPTY_STRING

        if self.validate_incident(request_info):
            return RESP_ERROR_INVALID_INCIDENT

        if self.validate_images_videos(request_info.get("images")):
            return RESP_ERROR_INVALID_IMAGES

        if self.validate_images_videos(request_info.get("videos")):
            return RESP_ERROR_INVALID_VIDEOS

        if self.validate_comment(request_info.get("comment")):
            return RESP_ERROR_INVALID_COMMENT

        if self.validate_title(request_info.get("title")):
            return RESP_ERROR_INVALID_TITLE

        if self.validate_location(request_info.get("location")):
            return RESP_ERROR_INVALID_LOCATION

        if self.incident_duplicate(request_info.get("comment"), IncidentData.get_all_dbincidents(IncidentData, table_name)):
            return RESP_ERROR_POST_DUPLICATE
        # last_incidents = IncidentData.get_all_dbincidents(IncidentData, table_name)#[-1].get("incident_id")
        # last_incident_id = self.get_created_id(table_name)
        # incident_id = 0
        if table_name == "redflags":
            incident_type = 1
            incident_id = self.ireporter_db.insert_data_redflags(
                    1,
                    request_info.get("location"),
                    request_info.get("title"),
                    request_info.get("comment"),
                    request_info.get("images"),
                    request_info.get("videos"),
                    datetime.datetime.now(),
                    user_identity.get("user_id"),
                    request_info.get("status")    
                )

        if table_name == "interventions":
            incident_type = 2
            incident_id = self.ireporter_db.insert_data_interventions(
                    incident_type,
                    request_info.get("location"),
                    request_info.get("title"),
                    request_info.get("comment"),
                    request_info.get("images"),
                    request_info.get("videos"),
                    datetime.datetime.now(),
                    user_identity["user_id"],
                    request_info.get("status")    
                )
        created_incident = {
            "incident_id": incident_id[0][0],
            "incident_type": incident_type,
            "title": request_info.get("title"),
            "comment": request_info.get("comment"),
            "images": request_info.get("images"),
            "videos": request_info.get("videos"),
            "created_on": datetime.datetime.now(),
            "created_by": user_identity["user_id"],
            "status":"pending investigation"

        }

        return Response(json.dumps({
            "status": 201,
            "data": [created_incident],
            "message": RESP_SUCCESS_MSG_CREATE_INCIDENT
        }), content_type="application/json", status=201)

    # def get_created_id(self, table_name):
    #     if len(IncidentData.get_all_dbincidents(IncidentData, table_name)) > 0:
    #         return IncidentData.get_all_dbincidents(IncidentData, table_name)[-1].get("incident_id") + 1
    #     return 1

        # lastIncident_id = last_incident

    def edit_incident_comment(self, request_info, incident_id, incident_type, user_id, table_name):
        if "comment" not in request_info or len(request_info) != 1:
            return RESP_ERROR_INVALID_COMMENT_STRING_TYPE

        for incident in IncidentData.get_all_dbincidents(IncidentData, table_name):
            if incident.get("incident_id")==incident_id and incident.get("created_by")!=user_id:
                return RESP_ERROR_NO_ACCESS
            elif incident.get("comment")==request_info.get("comment"):
                return RESP_ERROR_POST_DUPLICATE
            else:
                self.ireporter_db.update_data_incident_comment(incident_id, request_info.get("comment"), table_name)
                return Response(json.dumps({
                    "status": 201,
                    "data": incident,
                    "message": RESP_SUCCESS_MSG_INCIDENT_UPDATE_COMMENT
                }), content_type="application/json", status=200)
        return RESP_ERROR_INCIDENT_NOT_FOUND


    def edit_incident_location(self, request_info, incident_id, incident_type, user_id, table_name):
        if "location" not in request_info or len(request_info) != 1:
            return RESP_ERROR_INVALID_COMMENT_STRING_TYPE

        if self.validate_location(request_info.get("location")):
            return RESP_ERROR_INVALID_LOCATION

        for incident in IncidentData.get_all_dbincidents(IncidentData, table_name):
            if incident.get("incident_id")==incident_id and incident.get("created_by")!=user_id:
                return RESP_ERROR_MSG_NO_ACCESS
            elif incident.get("location")==request_info.get("location"):
                return RESP_ERROR_POST_DUPLICATE
            else:
                self.ireporter_db.update_data_incident_comment(incident_id, request_info.get("location"), table_name)
                return Response(json.dumps({
                    "status": 201,
                    "data": incident,
                    "message": RESP_SUCCESS_MSG_INCIDENT_UPDATE_LOCATION
                }), content_type="application/json", status=201)
        return RESP_ERROR_INCIDENT_NOT_FOUND

    def edit_incident_status(self, request_info, incident_id, incident_type, user_id, table_name):
        if "status" not in request_info or len(request_info) != 1:
            return RESP_ERROR_INVALID_COMMENT_STRING_TYPE

        if self.validate_status (request_info.get("status")):
            return RESP_ERROR_UPDATE_STATUS

        for incident in IncidentData.get_all_dbincidents(IncidentData, table_name):
            if user_id != 1:
                return RESP_ERROR_MSG_NO_ACCESS
            else:
                self.ireporter_db.update_data_incident_status(incident_id, request_info.get("status"), table_name)
                return Response(json.dumps({
                    "status": 201,
                    "data": incident,
                    "message": RESP_SUCCESS_MSG_INCIDENT_UPDATE_STATUS
                }), content_type="application/json", status=200)
        return RESP_ERROR_INCIDENT_NOT_FOUND


    def get_incident(self, incident_id, keyword, action_keyword, username, table_name):
        for incident in IncidentData.get_all_dbincidents(IncidentData, table_name):
            if incident.get("incident_id") == incident_id and username == incident.get("created_by"):
                return Response( json.dumps({
                    "status": 200,
                    "data": incident
                }), content_type="application/json", status=200)
            elif incident.get("incident_id") == incident_id and username != incident.get("created_by"):
                return Response( json.dumps({
                    "status": 200,
                    "data": "incident",
                    "error": RESP_ERROR_MSG_NO_ACCESS
                }), content_type="application/json", status=200)

        return RESP_ERROR_INCIDENT_NOT_FOUND

    def delete_incident(self, incident_id, keyword, username, table_name):
        for incident in IncidentData.get_all_dbincidents(IncidentData, table_name):
            if incident.get("incident_id") == incident_id and username == incident.get("created_by")\
            and incident.get("status") == "pending investigation":
                self.ireporter_db.delete_data_incident(incident_id, table_name)
                return Response( json.dumps({
                    "status": 200,
                    "data": [{"incident_id": incident_id}],
                    "message": RESP_SUCCESS_MSG_INCIDENT_DELETE
                }), content_type="application/json", status=200)
            elif incident.get("incident_id") == incident_id and username != incident.get("created_by") or \
            incident.get("status") != "pending investigation":
                return Response( json.dumps({
                    "status": 200,
                    "data": "incident",
                    "error": RESP_ERROR_MSG_NO_ACCESS
                }), content_type="application/json", status=200)

        return RESP_ERROR_INCIDENT_NOT_FOUND

    def validate_incident(self, request_data):
        """this method checks if a request contains all and only required fields"""
        minimum_turple = (
            "location",
            "videos",
            "images",
            "title",
            "comment"
        )

        if any(item not in request_data for item in minimum_turple) \
        or any(item not in minimum_turple for item in request_data):
            return True
        return False

    def validate_status(self, status):
        if not status or status not in ("pending investigation", "under investigation", "resolved", "rejected"):
            return True
        return False 
    def incident_duplicate(self, comment, incidents_list):
        """method to check is an incident exists on the system"""
        if any((incident.get("comment")).lower() == comment.lower()
               for incident in incidents_list):
            return True
        return False
    
    def validate_location(self, geolocation):
        """method checks if a given string includes valid coordinates"""
        geolocation = geolocation.replace(" ", "")
        cordinates = geolocation.split(",")
        for cordinate in cordinates:
            try:
                float(cordinate)
            except ValueError:
                return True
        if len(cordinates) != 2 or self.geo_coordinate_not_inrange(float(cordinates[0]), 90) \
        or self.geo_coordinate_not_inrange(float(cordinates[1]), 180):
            return True
        return False

    def geo_coordinate_not_inrange(self, coordinate, bound):
        """method to determin whether a particular coordinate is within an acceptable range"""
        if bound >= coordinate >= 0:
            return False
        if -bound <= coordinate <= 0:
            return False
        return True

    def validate_title(self, title):
        if self.empty_string(title):
            return RESP_ERROR_INVALID_EMAIL

        if self.invalid_str_datatype(title):
            return RESP_ERROR_INVALID_EMAIL
        
        return False

    def validate_comment(self, comment):
        if self.empty_string(comment):
            return RESP_ERROR_INVALID_EMAIL

        if self.invalid_str_datatype(comment):
            return RESP_ERROR_INVALID_EMAIL
        
        return False

    def empty_string(self, user_input):
        """this method checks for empty incident and user fields"""
        if str(user_input).replace(" ", "") == "":
            return True
        return False

    def invalid_str_datatype(self, string_value):
        """this method checks if input is a string"""
        if isinstance(string_value, str):
            return False
        return True

    def validate_images_videos(self, list_value):
        """this method checks is field is a list of strings"""
        if not isinstance(list_value, list) \
        or any(not isinstance(item, str) for item in list_value) or not list_value:
            return True
        return False
    

class IncidentData:
    """class for managing data of incidents"""
    ireporter_db = IreporterDb()
    def get_incidents(self, table_name):
        incidents = self.get_all_dbincidents(table_name)
        if not incidents:
            return RESP_SUCCESS_INCIDENT_LIST_EMPTY
        return Response(
            json.dumps({
                "status": 200,
                "data": incidents
            }), content_type="application/json", status=200
        )

    def get_user_incidents(self, user_id, table_name):
        incidents = self.get_incidents_specific_user(user_id, table_name)
        if not incidents:
            return RESP_SUCCESS_INCIDENT_LIST_EMPTY
        return Response(
            json.dumps({
                "status": 200,
                "data": incidents
            }), content_type="application/json", status=200
        )

    def get_all_dbincidents(self, table_name):
        data_from_db = self.ireporter_db.fetch_data_incidents(table_name)
        print(data_from_db)
        dict_incident = {}
        list_incidents = []
        for incident in data_from_db:
            dict_incident = {
                "incident_id": incident[0],
                "incident_type": incident[11],
                "location": incident[2],
                "title": incident[3],
                "comment": incident[4],
                "images":incident[5],
                "videos": incident[6],
                "created_on": incident[7],
                "created_by": incident[16],
                "status": incident[9]   
            }

            list_incidents.append(dict_incident)
        return list_incidents

    def get_incidents_specific_user(self, user_id, table_name):
        """method for getting all incidents for a particular user"""
        data_from_db = self.ireporter_db.fetch_data_user_incidents(user_id, table_name)
        print(data_from_db)
        dict_incident = {}
        list_incidents = []
        for incident in data_from_db:
            dict_incident = {
                "incident_id": incident[0],
                "incident_type": incident[11],
                "location": incident[2],
                "title": incident[3],
                "comment": incident[4],
                "images":incident[5],
                "videos": incident[6],
                "created_on": incident[7],
                "created_by": incident[16],
                "status": incident[9]   
            }

            list_incidents.append(dict_incident)
        return list_incidents