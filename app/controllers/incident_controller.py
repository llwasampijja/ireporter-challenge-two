from flask import request, Response, json
import datetime
from app.models.incident_model import Incident, IncidentData
from app.validators.general_validator import GeneralValidator
incident_data = IncidentData()


class IncidentController:

    validator = GeneralValidator()

    def create_incident(self, request_data, keyword):
        """method for creating red-flags"""
        created_on = datetime.datetime.now()
        created_by = request.cookies.get('username')
        # created_by = request_data.get("created_by")
        location = request_data.get("location")
        status = request_data.get("status")
        videos = request_data.get("videos")
        images = request_data.get("images")
        comment = request_data.get("comment")

        args_strings = [created_by,
                        location, status, comment]
        args_list = [videos, images]


        get_incidents_instance = incident_data.get_incidents(keyword)
        
        incident_id = self.validator.create_id(get_incidents_instance, "incident_id")

        if any(self.validator.check_empty_string(item) for item in
               args_strings):
            return self.response_unaccepted("empty")

        if any(self.validator.check_str_datatype(item) for item in
               args_strings) or self.validator.invalid_incident(request_data) or \
               any(self.validator.check_list_datatype(item) for item in args_list):
            return self.response_unaccepted("datatype")

        if self.validator.check_status_value(status):
            return self.response_unaccepted("status")

        new_incident = Incident(incident_id=incident_id,
                              created_on=created_on, created_by=created_by,
                              location=location, status=status, videos=videos,
                              images=images, comment=comment)
        incident_data.create_incident(new_incident.incident_dict(keyword), keyword)

        return Response(json.dumps({
            "status": 201,
            "data": [new_incident.incident_dict(keyword)],
            "message": "Incident created successifully"
        }), content_type="application/json", status=201)

    def get_incidents(self, keyword):
        get_incidents_instance = incident_data.get_incidents(keyword)
        if not get_incidents_instance:
            return Response(json.dumps({
                "status": 404,
                "message": "incidents list is empty"
            }), content_type="application/json", status=404)
        else:
            return Response(json.dumps({
                "status": 200,
                "data": get_incidents_instance
            }), content_type="application/json", status=200)

    def get_incident(self, incident_id, keyword):
        get_incident_instance = incident_data.get_incident(incident_id, keyword)
        if get_incident_instance is None:
            return Response(json.dumps({
                "status": 404,
                "message": "No incident of that specific id found"
            }), content_type="application/json", status=404)
        else:
            return Response(json.dumps({
                "status": 200,
                "data": [get_incident_instance]
            }), content_type="application/json", status=200)
    def update_incident(self, incident_id, request_data, keyword, username):

        location = request_data.get("location")

        if self.validator.check_empty_string(location):
            return self.response_unaccepted("empty")

        if self.validator.check_str_datatype(location):
            return self.response_unaccepted("datatype")

        update_incident_instance = incident_data.update_incident(
            incident_id, request_data, keyword, username)
        if update_incident_instance is None:
            return self.response_unaccepted("none")
        elif update_incident_instance == "non_author":
            return Response(json.dumps({
                "status":401,
                "message": "You are not authorised to edit this incident."
            }), content_type="application/json", status=401)
        else:
            return self.response_sumission_success(update_incident_instance,
                                                   "update")

    def update_incident_status(self, incident_id, request_data, keyword):
        if "status" not in request_data or len(request_data) != 1 or self.validator.check_status_value(request_data.get("status")):
            return Response(json.dumps({
                "status": 401,
                "message": "An admin can only edit the status of an incident, nothing more. The only accepted values include: 'pending investigation', 'resolved' and 'rejected'"
            }), content_type="application/json", status=401)

        update_incident_instance = incident_data.update_incident(
            incident_id, request_data, keyword, None)
        if update_incident_instance is None:
            return self.response_unaccepted("none")
        else:
            return self.response_sumission_success(update_incident_instance,
                                                   "incident_status")
    
    def delete_incident(self, incident_id, keyword, username):
        delete_incident_instance = incident_data.delete_incident(incident_id, keyword, username)
        if delete_incident_instance is None:
            return self.response_unaccepted("none")
        else:
            return self.response_sumission_success(delete_incident_instance,
                                                   "delete")

    def response_unaccepted(self, word):
        if word == "none":
            status_code = 404
            message = "No incident of that specific id found"
        elif word == "status":
            status_code = 404
            message = "Wrong Status given"
        elif word == "empty":
            status_code = 400
            message = "No empty fields are allowed"
        else:
            status_code = 400
            message = "Unaccepted datatype or Inavlid incident"
        return Response(json.dumps({
            "status": status_code,
            "message": message
        }), content_type="application/json", status=status_code)

    def response_sumission_success(self, return_data, keyword):
        if keyword == "delete":
            message = "Incident deleted successfully"
        elif keyword == "incident_status":
            message = "Updated incident record’s status"
        else:
            message = "Updated incident record’s location"
        return Response(json.dumps({
            "status": 201,
            "data": [return_data],
            "message": message
        }), content_type="application/json", status=201)


            