
"""This module includes validations for sthe rest of the user fields that
are not covered in the general_validator module"""
import re


class UserValidator():
    """class with a collection of validation methods for user''s fields"""

    @staticmethod
    def user_in_db(user_field, users_list, user_key):
        """refactored method to check if a user is already in the system"""
        if any(user.get(user_key) == user_field for user in users_list):
            return True
        return False

    def username_in_db(self, username, users_list):
        """method checks if a username is already in the system"""
        return self.user_in_db(username, users_list, "username")

    def email_in_db(self, email, users_list):
        """method checks if email already in the system"""
        return self.user_in_db(email, users_list, "email")

    def phonenumber_in_db(self, phonenumber, users_list):
        """method checks if phonenumber already in the system"""
        return self.user_in_db(phonenumber, users_list, "phonenumber")

    @staticmethod
    def validate_phone_numbers(phonenumber):
        """check if phonenumber has the correct number of digits for uganda"""
        if all(digit.isdigit() for digit in phonenumber) \
                and len(phonenumber) <= 10 and phonenumber.startswith("0"):
            return False
        return True

    @staticmethod
    def valid_email(email):
        """method checks if the email is in the correct format"""
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if email_pattern.match(email):
            return False
        return True

    @staticmethod
    def invalid_admin_state(isadmin):
        """method checks is is_admin as a valid value"""
        if isinstance(isadmin, bool):
            return False
        return True

    @staticmethod
    def valid_password(password):
        """method checks for an unacceptable password"""
        special_characters = ['$', '#', '@']
        password = password.replace(" ", "")
        test_conditions = [
            (len(password) >= 8 and len(password) <= 12),
            (any(x.isupper() for x in password) and any(x.islower()
                                                        for x in password)),
            (any(y in password for y in special_characters)
             and any(y.isdigit() for y in password))
        ]
        if all(condition is True for condition in test_conditions):
            return True
        return False

    @staticmethod
    def invalid_user(request_info):
        """method checks if a user has all and only the acceptable fields"""
        minimum_user_properties = (
            "firstname",
            "lastname",
            "email",
            "phonenumber",
            "username",
            "password"
        )
        all_user_fields = (
            "firstname",
            "lastname",
            "othernames",
            "email",
            "phonenumber",
            "username",
            "password"
            )

        if any(item not in request_info for item in minimum_user_properties)\
        or any(item not in all_user_fields for item in request_info):#\
            return True
        return False

    def invalid_othername(self, request_info):
        """method checks if othernames is provided by the user and if \
        provided it checks if it is a valid name"""
        if "othernames" in request_info \
        and self.invalid_name(request_info.get("othernames")):
            return True
        return False

    @staticmethod
    def invalid_username(username):
        """method checks if a provided username is valid"""
        word_letters = re.sub('[^a-zA-Z-0-9]+', '', str(username))
        if any(item.isalpha() for item in word_letters):
            return False
        return True

    @staticmethod
    def invalid_name(name):
        """method checks if a provided name is valid"""
        if any(not item.isalpha() for item in str(name)):
            return True
        return False
