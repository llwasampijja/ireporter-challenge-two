
import re


class UserValidator():

    def user_in_db(self, user_field, users_list, user_key):
        if any(user.get(user_key) == user_field for user in users_list):
            return True
        return False

    def username_in_db(self, username, users_list):
        return self.user_in_db(username, users_list, "username")

    def email_in_db(self, email, users_list):
        return self.user_in_db(email, users_list, "email")

    def validate_phone_numbers(self, phonenumber):
        if all(digit.isdigit() for digit in phonenumber) and len(phonenumber) <=10 and phonenumber.startswith("0"):
            return False 
        return True

    def valid_email(self, email):
        # email_pattern = re.compile("([a-z\d\-\.]+)@([a-z\d\-]+)\.([a-z\.](2.8))")
        email_pattern = re.compile("[^@]+@[^@]+\.[^@]+")
        if email_pattern.match(email):
            return False 
        return True

    # def invalid_admin_state(self, isadmin):
    #     if str(isadmin).lower()=="true" or str(isadmin).lower()=="false" or isinstance(isadmin, bool):
    #         return False
    #     return True

    def invalid_admin_state(self, isadmin):
        if isinstance(isadmin, bool):
            return False
        return True

    def valid_password(self, password):
        special_characters = ['$', '#', '@']
        password = password.replace(" ", "")
        test_conditions = [
            (len(password) >= 8 and len(password) <= 12),
            (any(x.isupper() for x in password) and any(x.islower() for x in password)),
            (any(y in password for y in special_characters) and any(y.isdigit() for y in password))
        ]
        if all( condition is True for condition in test_conditions):
            return True
        return False

        # if (len(password) >= 8 and len(password) <= 12) and (any(x.isupper() for x in password) and any(x.islower() for x in password))\
        #         and (any(y in password for y in special_characters) and any(y.isdigit() for y in password)):
        #         return True
        # return False

    def invalid_user(self, request_info):
        valid_user_properties = ["firstname","lastname","othernames","email","phonenumber","username","password"]
        if any((item not in valid_user_properties) for item in request_info) or len(request_info)!=7:
            return True
        return False 

    
