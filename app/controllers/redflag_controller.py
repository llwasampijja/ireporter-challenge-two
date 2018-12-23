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
        report_type = request_data.get("report_type")
        created_on = datetime.datetime.now()
        created_by = request_data.get("created_by")
        location = request_data.get("location")
        status = request_data.get("status")
        videos = request_data.get("videos")
        images = request_data.get("images")
        comment = request_data.get("comment")

        args_strings = [report_type, created_by,
                        location, status, videos, images, comment]


        get_redflags_instance = redflag_data.get_redflags()
        if not get_redflags_instance:
            redflag_id = 1
        else:
            redflag_id = 1 + get_redflags_instance[-1].get("redflag_id")

        if any(self.redflag_validator.check_empty_string(item) for item in
               args_strings):
            return self.responses("empty", None)

        if any(self.redflag_validator.check_str_datatype(item) for item in
               args_strings):
            return self.responses("datatype", None)

        if self.redflag_validator.check_status_value(status):
            return self.responses("status", None)

        new_redflag = RedFlag(redflag_id=redflag_id, report_type=report_type,
                              created_on=created_on, created_by=created_by,
                              location=location, status=status, videos=videos,
                              images=images, comment=comment)
        redflag_data.create_redflag(new_redflag.redflag_dict())

        return self.responses("create_success", new_redflag.redflag_dict())

    def get_reflags(self):
        get_redflags_instance = redflag_data.get_redflags()
        if not get_redflags_instance:
            return self.responses("empty_list", None)
            # return Response(json.dumps({
            #     "status": 411,
            #     "message": "Redflags list is empty"
            # }), content_type="application/json", status=411)
        else:
            return self.responses("non_empty_list", get_redflags_instance)
            # return Response(json.dumps({
            #     "status": 200,
            #     "data": get_redflags_instance
            # }), content_type="application/json", status=200)

    def get_redflag(self, redflag_id):
        get_redflag_instance = redflag_data.get_redflag(redflag_id)
        if get_redflag_instance is None:
            return self.responses("none", None)
        else:
            return self.responses("non_empty_list", get_redflag_instance)

        # if get_redflag_instance is None:
        #     return Response(json.dumps({
        #         "status": 404,
        #         "message": "No redflag of that specific id found"
        #     }), content_type="application/json", status=404)
        # else:
        #     return Response(json.dumps({
        #         "status": 200,
        #         "data": [get_redflag_instance]
        #     }), content_type="application/json", status=200)

    def update_redflag(self, redflag_id, request_data):

        comment = request_data.get("comment")

        if self.redflag_validator.check_empty_string(comment):
            # return self.response_emptystring()
            return self.responses("empty", None)

        if self.redflag_validator.check_str_datatype(comment):
            return self.responses("datatype", None)

        update_redflag_instance = redflag_data.update_redflag(
            redflag_id, request_data)
        if update_redflag_instance is None:
            return self.responses("none", None)
        else:
            # return self.response_sumission_success(update_redflag_instance, "update")
            return self.responses("update_success", update_redflag_instance)

    def delete_redflag(self, redflag_id):
        delete_redflag_instance = redflag_data.delete_redflag(redflag_id)
        if delete_redflag_instance is None:
            return self.responses("none", None)
        else:
            return self.responses("delete_success", delete_redflag_instance)
            # return self.response_sumission_success(delete_redflag_instance, "delete")

    # def response_emptystring(self):
    #     return Response(json.dumps({
    #         "status": 406,
    #         "message": "No empty fields are allowed"
    #     }), content_type="application/json", status=406)

    def responses(self, word, data):
        if word == "none":
            status_code = 404
            message = "No redflag of that specific id found"
        if word == "status":
            status_code = 404
            message = "Wrong Status given"
        if word == "empty":
            status_code = 406
            message = "No empty fields are allowed"
        if word == "create_success":
            status_code = 202
            message = "Red-Flag created successifully"
        if word == "update_success":
            status_code = 202
            message = "Red-flag updated successfully" 
        elif word == "delete_success":
            status_code = 202
            message = "Red-flag deleted successfully"  
        elif word == "empty_list":
            status_code = 411
            message = "Redflags list is empty"
        elif word == "non_empty_list":
            status_code = 200
            message = None
        else:
            status_code = 406
            message = "Unaccepted datatype"
        if data is None:
            return Response(json.dumps({
                "status": status_code,
                "message": message
            }), content_type="application/json", status=status_code)
        elif message is None:
            return Response(json.dumps({
                "status": status_code,
                "data": [data],
            }), content_type="application/json", status=status_code)
        else:
            return Response(json.dumps({
                "status": status_code,
                "data": [data],
                "message": message
            }), content_type="application/json", status=status_code)

    # def response_sumission_success(self, return_data, keyword):
    #     if keyword == "delete":
    #         message = "Red-flag deleted successfully"
    #     else:
    #         message = "Updated red-flag record’s location"
    #     return Response(json.dumps({
    #         "status": 202,
    #         "data": [return_data],
    #         "message": message
    #     }), content_type="application/json", status=202)
