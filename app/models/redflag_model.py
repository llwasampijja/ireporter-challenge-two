class RedFlag():
    def __init__(self, **kwargs):
        self.redflag_id = kwargs.get("redflag_id")
        self.report_type = "red-flag"
        self.created_on = kwargs.get("created_on")
        self.created_by = kwargs.get("created_by")
        self.location = kwargs.get("location")
        self.status = kwargs.get("status")
        self.videos = kwargs.get("videos")
        self.images = kwargs.get("images")
        self.comment = kwargs.get("comment")


    def redflag_dict(self):
        return {
            "redflag_id": self.redflag_id,
            "type": self.report_type,
            "created_on": self.created_on,
            "created_by": self.created_by,
            "location": self.location,
            "status": self.status,
            "videos": self.videos,
            "images": self.images,
            "comment": self.comment
        }