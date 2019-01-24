"""module containing models and data methods for incidents"""
import datetime

from flask import json, Response

from app.models.user_model import UsersData
from databases.ireporter_db import IreporterDb
from app.utilities.static_stringsnew import (
    RESP_SUCCESS_MSG_CREATE_INCIDENT,

    RESP_ERROR_INVALID_EMAIL
)

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

class Incident:
    ireporter_db = IreporterDb()

    def create_incident(self, request_info, keyword, table_name):
        verify_jwt_in_request()
        user_identity = get_jwt_identity()

        # if self.validate_incident(request_info):
        #     return RESP_ERROR_INVALID_EMAIL

        # if self.validate_images_videos(request_info.get("images")):
        #     return RESP_ERROR_INVALID_EMAIL

        # if self.validate_images_videos(request_info.get("videos")):
        #     return RESP_ERROR_INVALID_EMAIL

        # if self.validate_comment(request_info.get("comment")):
        #     return RESP_ERROR_INVALID_EMAIL

        # if self.validate_title(request_info.get("title")):
        #     return RESP_ERROR_INVALID_EMAIL

        # if self.validate_title(request_info.get("location")):
        #     return RESP_ERROR_INVALID_EMAIL

        # if self.incident_duplicate(request_info.get("comment"), IncidentData.get_all_dbincidents(IncidentData, keyword, table_name)):
        #     return RESP_ERROR_INVALID_EMAIL

        # self.ireporter_db.insert_data_redflags(
        #         1,
        #         request_info.get("location"),
        #         request_info.get("title"),
        #         request_info.get("comment"),
        #         request_info.get("images"),
        #         request_info.get("videos"),
        #         datetime.datetime.now(),
        #         user_identity["user_id"],
        #         request_info.get("status")    
        #     )

        # return Response(json.dumps({
        #     "status": 201,
        #     "data": [request_info],
        #     "message": RESP_SUCCESS_MSG_CREATE_INCIDENT
        # }), content_type="application/json", status=201)



    def edit_incident_location(self):
        pass

    def edit_incident_comment(self):
        pass

    def get_incident(self, incident_id, keyword, action_keyword, username, table_name):
        return IncidentData.get_or_delete(IncidentData, incident_id, keyword, action_keyword, username, table_name)

    def get_user_incidents(self):
        pass

    def delete_incident(self):
        pass

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
    users_data = UsersData()
    ireporter_db = IreporterDb()
    def __init__(self):
        self.redflags_list = []
        self.interventions_list = []

    def create_incident(self, incident, keyword):
        """method for addind an incident to a list of incidents"""
        if keyword == "redflag":
            return self.ireporter_db.insert_data_redflags(
                1,
                incident.get("location"),
                incident.get("title"),
                incident.get("comment"),
                incident.get("images"),
                incident.get("videos"),
                incident.get("created_on"),
                incident.get("created_by"),
                incident.get("status")    
            )
        else:
            return self.ireporter_db.insert_data_interventions(
                2,
                incident.get("location"),
                incident.get("title"),
                incident.get("comment"),
                incident.get("images"),
                incident.get("videos"),
                incident.get("created_on"),
                incident.get("created_by"),
                incident.get("status")
            )

    def get_incidents(self, keyword, table_name):
        """method for reading the incidents list"""
        return self.get_all_dbincidents(keyword, table_name)

    def get_incidents_specific_user(self, user_id, table_name):
        """method for getting all incidents for a particular user"""
        return self.get_all_suer_dbincidents(user_id, table_name)

    def update_incident(self, incident_id, new_update, keyword, username, table_name):
        """method for updating the an incident in the incidents list"""
        return self.update(self.get_all_dbincidents(keyword, table_name), incident_id, new_update, username, table_name)
 
    def update(self, incidednts_list, incident_id, new_update, username, table_name):
        """method with logic to update an incident in the incidents list"""
        for incident in incidednts_list:
            print("test this" + str(username) + incident.get("created_by"))
            if incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") == "pending investigation":
                self.ireporter_db.update_data_incident(incident_id, new_update, table_name)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") != "pending investigation":
                return "revoked"
            elif incident.get("incident_id") == incident_id and not username:
                self.ireporter_db.update_data_incident_status(incident_id, new_update.get("status"), table_name)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username != incident.get("created_by"):
                return "non_author"
        return None

    def my_get_incident(self, incidents_list, incident_id):
        """method for retrieving an incident from the incidents list"""
        for incident in incidents_list:
            if incident.get("incident_id") == incident_id:
                return incident
        return None

    def delete_incident(self, incident_id, keyword, username, table_name):
        """helper method for deleting or updaing incident"""
        return self.get_or_delete(incident_id, keyword, "delete", username, table_name)

    # def get_incident(self, incident_id, keyword, table_name):
    #     """helper method for geing an incident"""
    #     return self.get_or_delete(incident_id, keyword, "get", None, table_name)

    def delete(self, incidednts_list, incident_id, username, table_name):
        """method with the logic to delete an incident in the incidents list"""
        for incident in incidednts_list:
            if incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") == "pending investigation":
                self.ireporter_db.delete_data_incident(incident_id, table_name)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") != "pending investigation":
                return "revoked"
            elif incident.get("incident_id") == incident_id \
            and username != incident.get("created_by"):
                return "non_author"
        return None

    def get_or_delete(self, incident_id, keyword, action_keyword, username, table_name):
        """helper method for getting or deleting an incident"""
        if keyword == "redflag" and action_keyword == "delete":
            print("jy ruf dkag " + keyword)
            return self.delete(self.get_all_dbincidents("redflag", table_name), incident_id, username, table_name)
        elif keyword == "intervention" and action_keyword == "delete":
            return self.delete(self.get_all_dbincidents("intervention", table_name), incident_id, username, table_name)
        elif keyword == "redflag" and action_keyword == "get":
            return self.my_get_incident(self.get_all_dbincidents("redflag", table_name), incident_id)
        else:
            return self.my_get_incident(self.get_all_dbincidents("intervention", table_name), incident_id)

    def get_all_dbincidents(self, incident_type, table_name):
        data_from_db = None
        if incident_type == "redflag":
            table_name = "redflags"
        else:
            table_name = "interventions"
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


    def get_all_suer_dbincidents(self, user_id, table_name):
       
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