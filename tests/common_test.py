from flask import Response, json
from app import create_app
from app.utilities.static_strings import (
    URL_LOGIN
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
