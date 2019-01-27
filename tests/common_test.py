from flask import Response, json
from app import create_app
from app.utilities.static_strings import (
    URL_LOGIN,
    URL_REGISTER,
    # URL_USERS
)
class CommonTest():
    
    app = create_app()
    client = app.test_client()

    def response_post_incident(self, URL_INCIDENTS, data_post, jwt_token):
        return self.client.post(
            URL_INCIDENTS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(data_post),
            content_type="application/json"
        )

    def response_patch_incident(self, URL_INCIDENTS, incident_index, incident_attr, data_patch, jwt_token):
        return self.client.patch(
            URL_INCIDENTS + f"/{incident_index}/{incident_attr}",
            headers=dict(Authorization='Bearer ' + jwt_token),
            data=json.dumps(data_patch),
            content_type="application/json"
        )

    def response_delete_incident(self, URL_INCIDENTS, incident_index, jwt_token):
        return self.client.delete(
            URL_INCIDENTS + f"/{incident_index}",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )
    
    def response_get_incident(self, URL_INCIDENTS, incident_index, jwt_token):
        return self.client.get(
            URL_INCIDENTS + f"/{incident_index}",
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )

    def response_get_incidents(self, URL_INCIDENTS, jwt_token):
        return self.client.get(
            URL_INCIDENTS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )

    def response_get_users(self, URL_USERS, jwt_token):
        return self.client.get(
            URL_USERS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            content_type="application/json"
        )

    def response_patch_user(self, URL_USERS, user_data, jwt_token):
        return self.client.patch(
            URL_USERS,
            headers=dict(Authorization='Bearer ' + jwt_token),
            data = json.dumps(user_data),
            content_type="application/json"
        )

    def admin_jwt_token(self):
        admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "edward",
            "password": "i@mG8t##"
        }), content_type="application/json")
        return json.loads(admin_login_response.data)["access_token"]

    def nonadmin_jwt_token(self):
        admin_login_response = self.client.post(URL_LOGIN, data=json.dumps({
            "username": "annsmith",
            "password": "ABd1234@1"
        }), content_type="application/json")
        return json.loads(admin_login_response.data)["access_token"]

    def nonadmin_author_token(self):
        # test_user = {
        #     "firstname": "Dall",
        #     "lastname": "Kased",
        #     "othernames": "eddy",
        #     "email": "dall@bolon.com",
        #     "phonenumber": "0775961753",
        #     "username": "dallkased",
        #     "password": "ABd1234@1"
        # }
        # self.client.post(URL_REGISTER, data=json.dumps(test_user),
        #                  content_type="application/json")
        # login_response = self.client.post(URL_LOGIN, data=json.dumps({
        #     "username": "dallkased",
        #     "password": "ABd1234@1"
        # }), content_type="application/json")
        login_response = self.response_login_user()
        return json.loads(login_response.data)["access_token"]

    def response_login_user(self):
        test_user = {
            "firstname": "Dall",
            "lastname": "Kased",
            "othernames": "eddy",
            "email": "dall@bolon.com",
            "phonenumber": "0775961753",
            "username": "dallkased",
            "password": "ABd1234@1"
        }
        # self.client.post(URL_REGISTER, data=json.dumps(test_user),
        #                  content_type="application/json")
        self.response_register_user(test_user)
        return self.client.post(URL_LOGIN, data=json.dumps({
            "username": "dallkased",
            "password": "ABd1234@1"
        }), content_type="application/json")

    def response_register_user(self, test_user_data):
        return self.client.post(URL_REGISTER, data=json.dumps(test_user_data),
                         content_type="application/json")
        # return self.client.post(URL_LOGIN, data=json.dumps({
        #     "username": "dallkased",
        #     "password": "ABd1234@1"
        # }), content_type="application/json")
