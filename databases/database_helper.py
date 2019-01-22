import datetime
import hashlib
from databases.ireporter_db import IreporterDb

class DatabaseHelper():
    ireporter_db = IreporterDb()

    def create_admin(self):
        """method for adding a user item in the users list"""
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
        self.ireporter_db.insert_data_incident_types("redflags")
        self.ireporter_db.insert_data_incident_types("interventions")
