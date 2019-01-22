"""this module launches the entire application"""
from app import create_app
from databases.database_helper import DatabaseHelper
from databases.ireporter_db import IreporterDb

app = create_app()
ireporter_db = IreporterDb()
database_helper = DatabaseHelper()

if __name__ == "__main__":
    ireporter_db.drop_tables()
    ireporter_db.create_tables()
    database_helper.create_admin()
    database_helper.create_incident_types()
    app.run(debug=True)
