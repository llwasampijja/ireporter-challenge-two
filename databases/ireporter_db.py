import psycopg2
import os

from config import runtime_mode

class IreporterDb():

    def __init__(self):
        """class initializing method"""
        self.database_name = ""
        self.database_connect = None

        if runtime_mode == "development":
            self.database_connect = self.database_connection("ireporter_db")

        if runtime_mode == "testing":
            self.database_connect = self.database_connection("testing_db")

        if runtime_mode == "production":
            DATABASE_URL = os.environ['DATABASE_URL']
            self.database_connect = psycopg2.connect(DATABASE_URL, sslmode='require')

        self.database_connect.autocommit = True
        self.cursor_database = self.database_connect.cursor()

    def database_connection(self, database_name):
        """method to connect to appropriate database basing on the database name"""
        return psycopg2.connect(dbname=database_name, user='andela', host='localhost', password='bootcamp')

    def create_tables(self):
        """method for creating all the tables required for the application"""
        # create user tables
        self.cursor_database.execute(
            """CREATE TABLE IF NOT EXISTS app_users (
                user_id serial PRIMARY KEY, 
                firstname varchar, 
                lastname varchar, 
                othernames varchar, 
                username varchar UNIQUE, 
                email varchar UNIQUE, 
                phonenumber varchar UNIQUE, 
                is_admin BOOLEAN, 
                password varchar,
                registered_on TIMESTAMP)"""
        )

        # create incident type tables
        self.cursor_database.execute(
            """CREATE TABLE IF NOT EXISTS incident_types (
                incident_type_id serial PRIMARY KEY,
                incident_type_name varchar
            )"""
        )

        # create interventions tables
        self.cursor_database.execute(
            """CREATE TABLE IF NOT EXISTS interventions(
                incident_id serial PRIMARY KEY,
                incident_type int REFERENCES incident_types(incident_type_id) ON DELETE RESTRICT,
                location varchar,
                title varchar,
                comment varchar UNIQUE,
                images varchar [],
                videos varchar [],
                created_on TIMESTAMP,
                created_by int REFERENCES app_users(user_id) ON DELETE RESTRICT, 
                status varchar
            )"""
        )

        # create red-flags tables
        self.cursor_database.execute(
            """CREATE TABLE IF NOT EXISTS redflags(
                incident_id serial PRIMARY KEY,
                incident_type int REFERENCES incident_types(incident_type_id) ON DELETE RESTRICT,
                location varchar,
                title varchar,
                comment varchar UNIQUE,
                images varchar [],
                videos varchar [],
                created_on TIMESTAMP,
                created_by int REFERENCES app_users(user_id) ON DELETE RESTRICT, 
                status varchar
            )"""
        )

    def insert_data_incident_types(self, incident_type_name):
        sql_query = f"""INSERT INTO incident_types (
            incident_type_name
        ) VALUES (
            '{incident_type_name}'
        )"""
        self.cursor_database.execute(sql_query)

    def insert_data_users(self, firstname, lastname, othernames, username, email, phonenumber, is_admin, password, registered_on):
        sql_query = f"""INSERT INTO app_users(
            firstname,
            lastname,
            othernames,
            username,
            email,
            phonenumber,
            is_admin,
            password,
            registered_on
        ) VALUES (
            '{firstname}',
            '{lastname}',
            '{othernames}',
            '{username}',
            '{email}',
            '{phonenumber}',
            '{is_admin}',
            '{password}',
            '{registered_on}'
        )"""
        self.cursor_database.execute(sql_query)

    def insert_data_interventions(self, incident_type, location, title, comment, images, videos, created_on, created_by,  status):
        sql_query = """INSERT INTO interventions(
            incident_type,
            location,
            title,
            comment,
            images,
            videos,
            created_on,
            created_by,
            status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        data = (incident_type, location, title, comment, images, videos, created_on, created_by,  status)
        self.cursor_database.execute(sql_query, data)

    def insert_data_redflags(self, incident_type, location, title, comment, images, videos, created_on, created_by,  status):
        sql_query = """INSERT INTO redflags(
            incident_type,
            location,
            title,
            comment,
            images,
            videos,
            created_on,
            created_by,
            status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        data = (incident_type, location, title, comment, images, videos, created_on, created_by,  status)
        self.cursor_database.execute(sql_query, data)

    def fetch_data_users(self, app_users):
        sql_query = f"""SELECT * FROM {app_users}"""
        self.cursor_database.execute(sql_query)
        return self.cursor_database.fetchall()

    def fetch_data_incidents(self, table_name):
        sql_query = f"""SELECT * FROM {table_name} 
        JOIN incident_types ON {table_name}.incident_type = incident_types.incident_type_id
        JOIN app_users ON {table_name}.created_by = app_users.user_id"""
        self.cursor_database.execute(sql_query)
        return self.cursor_database.fetchall()

    def fetch_data_user_incidents(self, user_id, table_name):
        sql_query = f"""SELECT * FROM {table_name} 
        JOIN incident_types ON {table_name}.incident_type = incident_types.incident_type_id 
        JOIN app_users ON {table_name}.created_by = app_users.user_id WHERE created_by = '{user_id}'"""
        self.cursor_database.execute(sql_query)
        return self.cursor_database.fetchall()

    def update_data_incident_location(self, incident_id, location, table_name):
        sql_query = f"""UPDATE {table_name} SET location = '{location}' WHERE incident_id = '{incident_id}'"""
        self.cursor_database.execute(sql_query)

    def update_data_incident_comment(self, incident_id, comment, table_name):
        sql_query = f"""UPDATE {table_name} SET comment = '{comment}' WHERE incident_id = '{incident_id}'"""
        self.cursor_database.execute(sql_query)

    def update_data_incident(self, incident_id, new_update, table_name):
        if "location" in new_update:
            self.update_data_incident_location(incident_id, new_update.get("location"), table_name)
        
        if "comment" in new_update:
            self.update_data_incident_comment(incident_id, new_update.get("comment"), table_name)

    def update_data_incident_status(self, incident_id, status, table_name):
        sql_query = f"""UPDATE {table_name} SET status = '{status}' WHERE incident_id = '{incident_id}'"""
        self.cursor_database.execute(sql_query)

    def update_data_user_role(self, user_id, is_admin):
        sql_query = f"""UPDATE app_users SET is_admin = '{is_admin}' WHERE user_id = '{user_id}'"""
        self.cursor_database.execute(sql_query)

    def delete_data_incident(self, incident_id, table_name):
        sql_query = f"""DELETE FROM {table_name} WHERE incident_id = '{incident_id}'"""
        self.cursor_database.execute(sql_query)

    def drop_tables(self):
        sql_query0 = """DROP TABLE IF EXISTS redflags;"""
        sql_query1 = """DROP TABLE IF EXISTS interventions;"""
        sql_query2 = """DROP TABLE IF EXISTS app_users;"""
        sql_query3 = """DROP TABLE IF EXISTS incident_types;"""
        self.cursor_database.execute(sql_query0)
        self.cursor_database.execute(sql_query1)
        self.cursor_database.execute(sql_query2)
        self.cursor_database.execute(sql_query3)


if __name__=="__main__":
    ireporter_db = IreporterDb()
    ireporter_db.create_tables()