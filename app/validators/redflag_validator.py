class RedflagValidator():
    def check_empty_string(self, user_input):
        if str(user_input).replace(" ", "") == "":
            return True
        return False

    # def check_empty_string(self, *args):
    #     if any(str(user_input).replace(" ", "") == "" for user_input in args):
    #         return True
    #     return False

    def check_str_datatype(self, string_value):
        if isinstance(string_value, str):
            return False
        return True

    def check_int_datatype(self, int_value):
        if isinstance(int_value, int):
            return True
        return False

    def check_status_value(self, status):
        status = status.lower()
        if status=="resolved" or status=="pending investigation" or status=="rejected":
            return False
        return True

    def invalid_redflag(self, request_data):
        valid_redflags = ["created_on", "created_by", "location", "status", "videos", "images", "comment"]
        if any((item not in valid_redflags) for item in request_data):
            return True
        return False 