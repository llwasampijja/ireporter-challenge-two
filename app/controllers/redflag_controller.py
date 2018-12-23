from flask import request, Response, json
import datetime
from app.models.redflag_model import RedFlag
from app.data.redflag_data import RedflagData
from app.validators.redflag_validator import RedflagValidator
redflag_data = RedflagData()


class RedflagController:

    redflag_validator = RedflagValidator()

    def create_redflag(self, request_data):
        """method for creating red-flags"""
        created_on = datetime.datetime.now()
        created_by = request_data.get("created_by")
        location = request_data.get("location")
        status = request_data.get("status")
        videos = request_data.get("videos")
        images = request_data.get("images")
        comment = request_data.get("comment")

        args_strings = [created_by,
                        location, status, comment]
        args_list = [videos, images]


        get_redflags_instance = redflag_data.get_redflags()
        
        redflag_id = self.create_id(get_redflags_instance)

        if any(self.redflag_validator.check_empty_string(item) for item in
               args_strings):
            return self.response_emptystring()

        if any(self.redflag_validator.check_str_datatype(item) for item in
               args_strings) or self.redflag_validator.invalid_redflag(request_data):
            return self.response_unaccepted("datatype")

        if self.redflag_validator.check_status_value(status):
            return self.response_unaccepted("status")

        if any(self.redflag_validator.check_list_datatype(item) for item in
               args_list):
            return Response(json.dumps({
                "status": 404,
                "message": "Images or videos not a list"
            }), content_type="application/json", status=404)

        new_redflag = RedFlag(redflag_id=redflag_id, 
                              created_on=created_on, created_by=created_by,
                              location=location, status=status, videos=videos,
                              images=images, comment=comment)
        redflag_data.create_redflag(new_redflag.redflag_dict())

        return Response(json.dumps({
            "status": 202,
            "data": [new_redflag.redflag_dict()],
            "message": "Red-Flag created successifully"
        }), content_type="application/json", status=202)

    def get_reflags(self):
        get_redflags_instance = redflag_data.get_redflags()
        if not get_redflags_instance:
            return Response(json.dumps({
                "status": 411,
                "message": "Redflags list is empty"
            }), content_type="application/json", status=411)
        else:
            return Response(json.dumps({
                "status": 200,
                "data": get_redflags_instance
            }), content_type="application/json", status=200)

    def get_redflag(self, redflag_id):
        get_redflag_instance = redflag_data.get_redflag(redflag_id)
        if get_redflag_instance is None:
            return Response(json.dumps({
                "status": 404,
                "message": "No redflag of that specific id found"
            }), content_type="application/json", status=404)
        else:
            return Response(json.dumps({
                "status": 200,
                "data": [get_redflag_instance]
            }), content_type="application/json", status=200)

    def update_redflag(self, redflag_id, request_data):

        comment = request_data.get("comment")

        if self.redflag_validator.check_empty_string(comment):
            return self.response_emptystring()

        if self.redflag_validator.check_str_datatype(comment):
            return self.response_unaccepted("datatype")

        update_redflag_instance = redflag_data.update_redflag(
            redflag_id, request_data)
        if update_redflag_instance is None:
            return self.response_unaccepted("none")
        else:
            return self.response_sumission_success(update_redflag_instance,
                                                   "update")

    def delete_redflag(self, redflag_id):
        delete_redflag_instance = redflag_data.delete_redflag(redflag_id)
        if delete_redflag_instance is None:
            return self.response_unaccepted("none")
        else:
            return self.response_sumission_success(delete_redflag_instance,
                                                   "delete")

    def response_emptystring(self):
        return Response(json.dumps({
            "status": 406,
            "message": "No empty fields are allowed"
        }), content_type="application/json", status=406)

    def response_unaccepted(self, word):
        if word == "none":
            status_code = 404
            message = "No redflag of that specific id found"
        elif word == "status":
            status_code = 404
            message = "Wrong Status given"
        elif word == "empty":
            status_code = 406
            message = "No empty fields are allowed"
        else:
            status_code = 406
            message = "Unaccepted datatype or Inavlid Redflag"
        return Response(json.dumps({
            "status": status_code,
            "message": message
        }), content_type="application/json", status=status_code)

    def response_sumission_success(self, return_data, keyword):
        if keyword == "delete":
            message = "Red-flag deleted successfully"
        else:
            message = "Updated red-flag record’s location"
        return Response(json.dumps({
            "status": 202,
            "data": [return_data],
            "message": message
        }), content_type="application/json", status=202)

    def create_id(self, get_redflags_instance):
        if not get_redflags_instance:
            return 1
        else:
            return 1 + get_redflags_instance[-1].get("redflag_id")
