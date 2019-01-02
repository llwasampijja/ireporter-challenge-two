from flask import request


class Incident:
    def __init__(self, **kwargs):
        self.incident_id = kwargs.get("incident_id")
        self.incident_type = kwargs.get("incident_type")
        self.created_on = kwargs.get("created_on")
        self.created_by = kwargs.get("created_by")
        self.location = kwargs.get("location")
        self.status = kwargs.get("status")
        self.videos = kwargs.get("videos")
        self.images = kwargs.get("images")
        self.comment = kwargs.get("comment")

    def incident_dict(self, keyword):
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
            "comment": self.comment
        }


class IncidentData:
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
                "comment": "I saw him steal"
            }
        ]
        self.interventions_List = []

    def create_incident(self, incident, keyword):
        if keyword == "redflag":
            return self.redflags_list.append(incident)
        else:
            return self.interventions_List.append(incident)

    def get_incidents(self, keyword):
        if keyword == "redflag":
            return self.redflags_list
        else:
            return self.interventions_List

    def update_incident(self, incident_id, new_update, keyword, username):
        if keyword == "redflag":
            return self.update(self.redflags_list, incident_id, new_update, username)
        else:
            return self.update(self.interventions_List, incident_id, new_update, username)

    def update(self, incidednts_list, incident_id, new_update, username):
        for incident in incidednts_list:
            if incident.get("incident_id") == incident_id and username == incident.get("created_by"):
                incident.update(new_update)
                return incident
            elif incident.get("incident_id") == incident_id and not username:
                incident.update(new_update)
                return incident
            elif incident.get("incident_id") == incident_id and username != incident.get("created_by"):
                return "non_author"
        return None

    def delete(self, incidednts_list, incident_id, username):
        for incident in incidednts_list:
            if incident.get("incident_id") == incident_id and username == incident.get("created_by"):
                incidednts_list.remove(incident)
                return incident
            elif incident.get("incident_id") == incident_id and username != incident.get("created_by"):
                return "non_author"
        return None

    def my_get_incident(self, incidents_list, incident_id):
        for incident in incidents_list:
            if incident.get("incident_id") == incident_id:
                return incident
        return None

    def delete_incident(self, incident_id, keyword, username):
        return self.get_or_delete(incident_id, keyword, "delete", username)

    def get_incident(self, incident_id, keyword):
        return self.get_or_delete(incident_id, keyword, "get", None)

    def get_or_delete(self, incident_id, keyword, action_keyword, username):
        if keyword == "redflag" and action_keyword == "delete":
            return self.delete(self.redflags_list, incident_id, username)
        elif keyword == "intervention" and action_keyword == "delete":
            return self.delete(self.interventions_List, incident_id, username)
        elif keyword == "redflag" and action_keyword == "get":
            return self.my_get_incident(self.redflags_list, incident_id)
        else:
            return self.my_get_incident(self.interventions_List, incident_id)
