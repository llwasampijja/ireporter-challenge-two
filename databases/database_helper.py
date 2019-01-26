import datetime
import hashlib
from databases.ireporter_db import IreporterDb

class DatabaseHelper():
    ireporter_db = IreporterDb()

    def create_admin(self):
        """method for adding a user item in the users list"""
        admin_user = self.ireporter_db.fetch_data_user_byid(1)
        if not admin_user:
            self.ireporter_db.insert_data_users(
                "Edward",
                "Army",
                "Eddy",
                "edward",
                "edward@bolon.com",
                "0775961853",
                True,
                hashlib.sha224(
                        b"{}").hexdigest().format("i@mG8t##"),
                datetime.datetime.now()
            )

    def create_incident_types(self):
        incident_types = self.ireporter_db.fetch_data_incident_types()
        if not incident_types:
            self.ireporter_db.insert_data_incident_types("redflags")
            self.ireporter_db.insert_data_incident_types("interventions")
