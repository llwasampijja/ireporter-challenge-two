
from flask import request, Response, json
import datetime
from app.models.redflag_model import RedFlag
from app.data.redflag_data import RedflagData
from app.validators.redflag_validator import RedflagValidator
redflagData = RedflagData()

class RedflagController:
    
    redflagValidator = RedflagValidator()
    
    def create_redflag(self):
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

        

        if self.redflagValidator.check_empty_string(report_type,created_by,location,status,\
            videos,images,comment):
            response_data = {
                "status": 201,
                "message": "No empty fields are allowed"
            }
            return Response(json.dumps(response_data), content_type="application/json", status=200)

        if self.redflagValidator.check_str_datatype(report_type) or self.redflagValidator.check_str_datatype(created_by) or \
            self.redflagValidator.check_str_datatype(location) or self.redflagValidator.check_str_datatype(status) or \
            self.redflagValidator.check_str_datatype(videos) or self.redflagValidator.check_str_datatype(images) or \
            self.redflagValidator.check_str_datatype(comment):
            response_data = {
                "status": 201,
                "message": "Wrong data type entered"
            }
            return Response(json.dumps(response_data), content_type="application/json", status=200)

        if self.redflagValidator.check_status_value(status):
            response_data = {
                "status": 201,
                "message": "Wrong Status given"
            }
            return Response(json.dumps(response_data), content_type="application/json", status=200)
            

        new_redflag = RedFlag(redflag_id=redflag_id,report_type=report_type,created_on=created_on,\
        created_by=created_by,location=location,status=status,videos=videos,images=images,comment=comment)
        redflagData.create_redflag(new_redflag.redflag_dict())

        response_data = {
            "status": 201,
            "data": [new_redflag.redflag_dict()],
            "message": "Red-Flag created successifully"
        }
        return Response(json.dumps(response_data), content_type="application/json", status=201)
        