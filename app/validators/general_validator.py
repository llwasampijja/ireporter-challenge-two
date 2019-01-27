"""this module includes validations for incidents and users"""
class GeneralValidator():
    """this class includes methods used to validate incident fields and users"""

    @staticmethod
    def empty_string(user_input):
        """this method checks for empty incident and user fields"""
        if str(user_input).replace(" ", "") == "":
            return True
        return False

    @staticmethod
    def invalid_str_datatype(string_value):
        """this method checks if input is a string"""
        if isinstance(string_value, str):
            return False
        return True

    @staticmethod
    def invalid_list_datatype(list_value):
        """this method checks is field is a list of strings"""
        if not isinstance(list_value, list) \
        or any(not isinstance(item, str) for item in list_value) or not list_value:
            return True
        return False

    @staticmethod
    def invalid_status_value(status):
        """this methods checks is incidents status is among the given values"""
        status = str(status).lower()
        if status in ("resolved", "pending investigation", "rejected", "under investigation"):
            return False
        return True

    @staticmethod
    def invalid_item(request_data, minimum_turple, maximum_turple):
        """this method checks if a request contains all and only required fields"""
        if any(item not in request_data for item in minimum_turple) \
        or any(item not in maximum_turple for item in request_data):
            return True
        return False

    @staticmethod
    def incident_duplicate(comment, incidents_list):
        """method to check is an incident exists on the system"""
        if any((incident.get("comment")).lower() == comment.lower()
               for incident in incidents_list):
            return True
        return False

    # @staticmethod
    # def create_id(get_incidents_instance, key_id):
    #     """method for creating an id for every new item created"""
    #     if not get_incidents_instance:
    #         return 1
    #     return 1 + get_incidents_instance[-1].get(key_id)

    def invalid_coordinates(self, geolocation):
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

    @staticmethod
    def geo_coordinate_not_inrange(coordinate, bound):
        """method to determin whether a particular coordinate is within an acceptable range"""
        if bound >= coordinate >= 0:
            return False
        if -bound <= coordinate <= 0:
            return False
        return True
