"""module containing models and data methods for incidents"""
from app.models.user_model import UsersData
from databases.ireporter_db import IreporterDb

class Incident:
    """incident model"""
    def __init__(self, **kwargs):
        self.incident_id = kwargs.get("incident_id")
        self.incident_type = kwargs.get("incident_type")
        self.location = kwargs.get("location")
        self.title = kwargs.get("title")
        self.comment = kwargs.get("comment")
        self.images = kwargs.get("images")
        self.videos = kwargs.get("videos")
        self.created_on = kwargs.get("created_on")
        self.created_by = kwargs.get("created_by")
        self.status = kwargs.get("status")
        
    def incident_dict(self, keyword):
        """method to return a dictionary of an incident"""
        if keyword == "redflag":
            self.incident_type = "redflag"
        else:
            self.incident_type = "intervention"

        return {
            "incident_id": self.incident_id,
            "incident_type": self.incident_type,
            "location": self.location,
            "title": self.title,
            "comment": self.comment,
            "images": self.images,
            "videos": self.videos,
            "created_on": self.created_on,
            "created_by": self.created_by,
            "status": self.status
        }

class IncidentData:
    """class for managing data of incidents"""
    users_data = UsersData()
    ireporter_db = IreporterDb()
    def __init__(self):
        self.redflags_list = []
        self.interventions_list = []

    def create_incident(self, incident, keyword):
        """method for addind an incident to a list of incidents"""
        if keyword == "redflag":
            return self.ireporter_db.insert_data_redflags(
                1,
                incident.get("location"),
                incident.get("title"),
                incident.get("comment"),
                incident.get("images"),
                incident.get("videos"),
                incident.get("created_on"),
                incident.get("created_by"),
                incident.get("status")    
            )
        else:
            return self.ireporter_db.insert_data_interventions(
                2,
                incident.get("location"),
                incident.get("title"),
                incident.get("comment"),
                incident.get("images"),
                incident.get("videos"),
                incident.get("created_on"),
                incident.get("created_by"),
                incident.get("status")
            )

    def get_incidents(self, keyword, table_name):
        """method for reading the incidents list"""
        return self.get_all_dbincidents(keyword, table_name)

    def get_incidents_specific_user(self, user_id, table_name):
        """method for getting all incidents for a particular user"""
        return self.get_all_suer_dbincidents(user_id, table_name)

    def update_incident(self, incident_id, new_update, keyword, username, table_name):
        """method for updating the an incident in the incidents list"""
        return self.update(self.get_all_dbincidents(keyword, table_name), incident_id, new_update, username, table_name)
 
    def update(self, incidednts_list, incident_id, new_update, username, table_name):
        """method with logic to update an incident in the incidents list"""
        for incident in incidednts_list:
            # print("test this" + str(username) + incident.get("created_by"))
            if incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") == "pending investigation":
                self.ireporter_db.update_data_incident(incident_id, new_update, table_name)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") != "pending investigation":
                return "revoked"
            elif incident.get("incident_id") == incident_id and not username:
                self.ireporter_db.update_data_incident_status(incident_id, new_update.get("status"), table_name)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username != incident.get("created_by"):
                return "non_author"
        return None

    @staticmethod
    def my_get_incident(incidents_list, incident_id):
        """method for retrieving an incident from the incidents list"""
        for incident in incidents_list:
            if incident.get("incident_id") == incident_id:
                return incident
        return None

    def delete_incident(self, incident_id, keyword, username, table_name):
        """helper method for deleting or updaing incident"""
        return self.get_or_delete(incident_id, keyword, "delete", username, table_name)

    def get_incident(self, incident_id, keyword, table_name):
        """helper method for geing an incident"""
        return self.get_or_delete(incident_id, keyword, "get", None, table_name)

    def delete(self, incidednts_list, incident_id, username, table_name):
        """method with the logic to delete an incident in the incidents list"""
        for incident in incidednts_list:
            if incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") == "pending investigation":
                self.ireporter_db.delete_data_incident(incident_id, table_name)
                return incident
            elif incident.get("incident_id") == incident_id \
            and username == incident.get("created_by") \
            and incident.get("status") != "pending investigation":
                return "revoked"
            elif incident.get("incident_id") == incident_id \
            and username != incident.get("created_by"):
                return "non_author"
        return None

    def get_or_delete(self, incident_id, keyword, action_keyword, username, table_name):
        """helper method for getting or deleting an incident"""
        if keyword == "redflag" and action_keyword == "delete":
            # print("jy ruf dkag " + keyword)
            return self.delete(self.get_all_dbincidents("redflag", table_name), incident_id, username, table_name)
        elif keyword == "intervention" and action_keyword == "delete":
            return self.delete(self.get_all_dbincidents("intervention", table_name), incident_id, username, table_name)
        elif keyword == "redflag" and action_keyword == "get":
            return self.my_get_incident(self.get_all_dbincidents("redflag", table_name), incident_id)
        else:
            return self.my_get_incident(self.get_all_dbincidents("intervention", table_name), incident_id)

    def get_all_dbincidents(self, incident_type, table_name):
        data_from_db = None
        if incident_type == "redflag":
            table_name = "redflags"
        else:
            table_name = "interventions"
        data_from_db = self.ireporter_db.fetch_data_incidents(table_name)
        # print(data_from_db)
        dict_incident = {}
        list_incidents = []
        for incident in data_from_db:
            dict_incident = {
                "incident_id": incident[0],
                "incident_type": incident[11],
                "location": incident[2],
                "title": incident[3],
                "comment": incident[4],
                "images":incident[5],
                "videos": incident[6],
                "created_on": incident[7],
                "created_by": incident[16],
                "status": incident[9]   
            }

            list_incidents.append(dict_incident)
        return list_incidents


    def get_all_suer_dbincidents(self, user_id, table_name):
       
        data_from_db = self.ireporter_db.fetch_data_user_incidents(user_id, table_name)
        # print(data_from_db)
        dict_incident = {}
        list_incidents = []
        for incident in data_from_db:
            dict_incident = {
                "incident_id": incident[0],
                "incident_type": incident[11],
                "location": incident[2],
                "title": incident[3],
                "comment": incident[4],
                "images":incident[5],
                "videos": incident[6],
                "created_on": incident[7],
                "created_by": incident[16],
                "status": incident[9]   
            }

            list_incidents.append(dict_incident)
        return list_incidents