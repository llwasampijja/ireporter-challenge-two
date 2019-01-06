class GeneralValidator():
    def check_empty_string(self, user_input):
        if str(user_input).replace(" ", "") == "":
            return True
        return False

    def check_str_datatype(self, string_value):
        if isinstance(string_value, str):
            return False
        return True

    def check_list_datatype(self, list_value):
        if not isinstance(list_value, list) or any(not isinstance(item, str) for item in list_value) or not list_value:
            return True
        return False

    def check_status_value(self, status):
        status = str(status).lower()
        if status == "resolved" or status == "pending investigation" or status == "rejected" or status == "under investigation":
            return False
        return True

    def invalid_incident(self, request_data):
        # valid_incidents = ["created_on", "created_by", "location", "status", "videos", "images", "comment"]
        valid_incidents = ["location", "videos", "images", "title", "comment"]
        if any((item not in valid_incidents) for item in request_data):
            return True
        return False

    def incident_duplicate(self, comment, incidents_list):
        if any((incident.get("comment")).lower() == comment.lower() for incident in incidents_list):
            return True
        return False

    def create_id(self, get_incidents_instance, key_id):
        if not get_incidents_instance:
            return 1
        else:
            return 1 + get_incidents_instance[-1].get(key_id)

    def invalid_coordinates(self, geolocation):
        geolocation = geolocation.replace(" ", "")
        cordinates = geolocation.split(",")
        # if len(cordinates) != 2:
        #     return True
        for cordinate in cordinates:
            try:
                float(cordinate)
            except ValueError:
                return True

        if len(cordinates) != 2 or self.geo_coordinate_not_inrange(float(cordinates[0]), 90) or \
                self.geo_coordinate_not_inrange(float(cordinates[1]), 180):
            return True

        return False

    def geo_coordinate_not_inrange(self, coordinate, bound):
        if 0 <= coordinate and coordinate <= bound:
            return False
        if -bound <= coordinate and coordinate <= 0:
            return False
        return True
