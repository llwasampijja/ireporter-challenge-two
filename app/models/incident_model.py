"""module containing models and data methods for incidents"""
from app.models.user_model import UsersData

class Incident:
    """incident model"""
    def __init__(self, **kwargs):
        self.incident_id = kwargs.get("incident_id")
        self.incident_type = kwargs.get("incident_type")
        self.created_on = kwargs.get("created_on")
        self.created_by = kwargs.get("created_by")
        self.location = kwargs.get("location")
        self.status = kwargs.get("status")
        self.videos = kwargs.get("videos")
        self.images = kwargs.get("images")
        self.title = kwargs.get("title")
        self.comment = kwargs.get("comment")

    def incident_dict(self, keyword):
        """method to return a dictionary of an incident"""
        if keyword == "redflag":
            self.incident_type = "redflag"
        else:
            self.incident_type = "intervention"

        return {
            "incident_id": self.incident_id,
            "incident_type": self.incident_type,
            "created_on": self.created_on,
            "created_by": self.created_by,
            "location": self.location,
            "status": self.status,
            "videos": self.videos,
            "images": self.images,
            "title": self.title,
            "comment": self.comment
        }


class IncidentData:
    """class for managing data of incidents"""
    users_data = UsersData()
    def __init__(self):
        self.redflags_list = [
            {
                "incident_id": 1,
                "incident_type": "red-flag",
                "created_on": "10/10/2018",
                "created_by": "annsmith",
                "location": "2.0000, 0.3019",
                "status": "pending investigation",
                "videos": ['stole.mp4', 'corrupe.mp4'],
                "images": ['stole.jpg', 'corrupt.jpg'],
                "title": "cop thief",
                "comment": "I saw him steal"
            },
            {
                "incident_id": 2,
                "incident_type": "red-flag",
                "created_on": "30/10/2018",
                "created_by": "dallkased",
                "location": "2.0000, 90.3019",
                "status": "resolved",
                "videos": ['stole.mp4', 'corrupe.mp4'],
                "images": ['stole.jpg', 'corrupt.jpg'],
                "title": "cop thief",
                "comment": "Every one saw him stealing money"
            }
        ]
        self.interventions_list = []

    def create_incident(self, incident, keyword):
        """method for addind an incident to a list of incidents"""
        if keyword == "redflag":
            return self.redflags_list.append(incident)
        else:
            return self.interventions_list.append(incident)

    def get_incidents(self, keyword):
        """method for reading the incidents list"""
        if keyword == "redflag":
            return self.redflags_list
        else:
            return self.interventions_list

    def get_incidents_specific_user(self, user_id, incidents_list, users_list):
        """method for getting all incidents for a particular user"""
        incidents_specific_user = []
        username = None
        for user in users_list:
            if user_id == user.get("user_id"):
                username = user.get("username")
        for incident in incidents_list:
            if username == incident.get("created_by"):
                incidents_specific_user.append(incident)
        return (username, incidents_specific_user)

    def update_incident(self, incident_id, new_update, keyword, username):
        """method for updating the an incident in the incidents list"""
        if keyword == "redflag":
            return self.update(self.redflags_list, incident_id, new_update, username)
        else:
            return self.update(self.interventions_list, incident_id, new_update, username)

    @staticmethod
    def update(incidednts_list, incident_id, new_update, username):
        """method with logic to update an incident in the incidents list"""
        for incident in incidednts_list:
            if incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") == "pending investigation":
                incident.update(new_update)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") != "pending investigation":
                return "revoked"
            elif incident.get("incident_id") == incident_id and not username:
                incident.update(new_update)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username != incident.get("created_by"):
                return "non_author"
        return None

    @staticmethod
    def delete(incidednts_list, incident_id, username):
        """method with the logic to delete an incident in the incidents list"""
        for incident in incidednts_list:
            if incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") == "pending investigation":
                incidednts_list.remove(incident)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") != "pending investigation":
                return "revoked"
            elif incident.get("incident_id") == incident_id \
            and username != incident.get("created_by"):
                return "non_author"
        return None

    @staticmethod
    def my_get_incident(incidents_list, incident_id):
        """method for retrieving an incident from the incidents list"""
        print("Unknown cause of error: " + str(incidents_list))
        for incident in incidents_list:
            if incident.get("incident_id") == incident_id:
                return incident
        return None

    def delete_incident(self, incident_id, keyword, username):
        """helper method for deleting or updaing incident"""
        return self.get_or_delete(incident_id, keyword, "delete", username)

    def get_incident(self, incident_id, keyword):
        """helper method for geing an incident"""
        return self.get_or_delete(incident_id, keyword, "get", None)

    def get_or_delete(self, incident_id, keyword, action_keyword, username):
        """helper method for getting or deleting an incident"""
        if keyword == "redflag" and action_keyword == "delete":
            return self.delete(self.redflags_list, incident_id, username)
        elif keyword == "intervention" and action_keyword == "delete":
            return self.delete(self.interventions_list, incident_id, username)
        elif keyword == "redflag" and action_keyword == "get":
            return self.my_get_incident(self.redflags_list, incident_id)
        else:
            return self.my_get_incident(self.interventions_list, incident_id)
