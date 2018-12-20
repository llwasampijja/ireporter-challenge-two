from flask import request, Response, json
import datetime
from app.models.redflag_model import RedFlag
from app.data.redflag_data import RedflagData
from app.validators.redflag_validator import RedflagValidator
redflagData = RedflagData()

class RedflagController:
    
    redflagValidator = RedflagValidator()
    
    def create_redflag(self):
        """method for creating red-flags"""
        request_data = request.get_json()
        redflag_id = request_data.get("redflag_id")
        report_type = request_data.get("report_type")
        created_on = datetime.datetime.now()
        created_by = request_data.get("created_by")
        location = request_data.get("location")
        status = request_data.get("status")
        videos = request_data.get("videos")
        images = request_data.get("images")
        comment = request_data.get("comment")

        args_strings = [report_type,created_by,location,status,videos,images,comment]

        

        if self.redflagValidator.check_empty_string(report_type,created_by,location,status,\
            videos,images,comment):
            response_data = {
                "status": 406,
                "message": "No empty fields are allowed"
            }
            return Response(json.dumps(response_data), content_type="application/json", status=406)

        if any(self.redflagValidator.check_str_datatype(item) for item in args_strings):
            response_data = {
                "status": 422,
                "message": "Wrong data type entered"
            }
            return Response(json.dumps(response_data), content_type="application/json", status=422)

        if self.redflagValidator.check_status_value(status):
            response_data = {
                "status": 412,
                "message": "Wrong Status given"
            }
            return Response(json.dumps(response_data), content_type="application/json", status=412)
            

        new_redflag = RedFlag(redflag_id=redflag_id,report_type=report_type,created_on=created_on,\
        created_by=created_by,location=location,status=status,videos=videos,images=images,comment=comment)
        redflagData.create_redflag(new_redflag.redflag_dict())

        response_data = {
            "status": 202,
            "data": [new_redflag.redflag_dict()],
            "message": "Red-Flag created successifully"
        }
        return Response(json.dumps(response_data), content_type="application/json", status=202)
        
    def get_reflags(self):
        get_redflags_instance = redflagData.get_redflags() 
        if len(get_redflags_instance) <= 0:
            return Response(json.dumps({
                "status": 411,
                "message": "No redflags found"
            }),content_type="application/json", status=411)
        else:
            return Response(json.dumps ({
                "status": 200,
                "data": get_redflags_instance
                }), content_type="application/json", status=200)
    
    def get_redflag(self, redflag_id):
        get_redflag_instance = redflagData.get_redflag(redflag_id) 
        if get_redflag_instance == None:
            return Response(json.dumps({
                "status": 404,
                "message": "No redflag of that specific id found"
            }), content_type="application/json", status=404)
        else:
            return Response(json.dumps({
                "status": 200,
                "data": [get_redflag_instance]
            }), content_type="application/json", status=200)

    def update_redflag(self, redflag_id):
        request_data = request.get_json()
        comment = request_data.get("comment")

        if self.redflagValidator.check_empty_string(comment):
            response_data = {
                "status": 406,
                "message": "No empty fields are allowed"
            }
            return Response(json.dumps(response_data), content_type="application/json", status=406)

        if self.redflagValidator.check_str_datatype(comment):
            return Response(json.dumps({
                "status": 406,
                "message": "Wrong data type entered"
            }), content_type="application/json", status=406)

        update_redflag_instance = redflagData.update_redflag(redflag_id, request_data)
        if update_redflag_instance == None:
            return Response(json.dumps({
                "status": 404,
                "message": "No redflag of that specific id found"
            }), content_type="application/json", status=404)
        else:
            return Response(json.dumps({
                "status": 202,
                "data": [update_redflag_instance],
                "message": "Updated red-flag record’s location"
            }), content_type="application/json", status=202)

    def delete_redflag(self, redflag_id):
        delete_redflag_instance = redflagData.delete_redflag(redflag_id)
        if delete_redflag_instance == None:
            return Response(json.dumps({
                "status": 404,
                "message": "No redflag of that specific id found"
            }), content_type="application/json", status=404)
        else:
            return Response(json.dumps({
                "status": 202,
                "data": [delete_redflag_instance],
                "message": "Red-flag deleted successfully"
            }), content_type="application/json", status=202)