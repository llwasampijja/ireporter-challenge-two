import psycopg2
import os

from config import environment_config, runtime_mode
from app.utilities.static_strings import RESP_ERROR_MSG_DATABASE_CONNECTION

class IreporterDb():

    def __init__(self):
        """class initializing method"""
        try:
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
        except:
            print (RESP_ERROR_MSG_DATABASE_CONNECTION)

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
                incident_type_name varchar UNIQUE
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
        ) RETURNING user_id"""
        self.cursor_database.execute(sql_query)
        return self.cursor_database.fetchall()

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
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING incident_id;"""

        data = (incident_type, location, title, comment, images, videos, created_on, created_by,  status)
        self.cursor_database.execute(sql_query, data)
        return self.cursor_database.fetchall()

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
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING incident_id;"""
        

        data = (incident_type, location, title, comment, images, videos, created_on, created_by,  status)
        self.cursor_database.execute(sql_query, data)
        return self.cursor_database.fetchall()

    def fetch_data_users(self, app_users):
        sql_query = f"""SELECT * FROM {app_users}"""
        self.cursor_database.execute(sql_query)
        return self.cursor_database.fetchall()

    def fetch_data_incident_types(self):
        sql_query = f"""SELECT * FROM incident_types"""
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

    def fetch_data_user_byid(self, user_id):
        sql_query = f"""SELECT * FROM app_users WHERE user_id = '{user_id}'"""
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

    # def update_data_incident_video(self, incident_id, videos_string, table_name):
    #     old_video_string = f"""SELECT images FROM {table_name} WHERE incident_id = '{incident_id}'"""
    #     if old_video_string == "noimage":
    #         sql_query = f"""UPDATE {table_name} SET videos = '{videos_string}' WHERE incident_id = '{incident_id}'"""
    #         self.cursor_database.execute(sql_query)
    #     else:
    #         new_video_string = old_video_string + "," + videos_string
    #         sql_query = f"""UPDATE {table_name} SET videos = '{new_video_string}' WHERE incident_id = '{incident_id}'"""
    #         self.cursor_database.execute(sql_query)

    def fetch_data_incident_image(self, incident_id, images_string, table_name):
        sql_query_old_image_string = f"""SELECT images FROM {table_name} WHERE incident_id = '{incident_id}'"""
        self.cursor_database.execute(sql_query_old_image_string)
        return self.cursor_database.fetchall()

    def fetch_data_incident_video(self, incident_id, videos_string, table_name):
        sql_query_old_video_string = f"""SELECT videos FROM {table_name} WHERE incident_id = '{incident_id}'"""
        self.cursor_database.execute(sql_query_old_video_string)
        return self.cursor_database.fetchall()

    # def update_data_incident_image(self, incident_id, images_string, table_name):
    #     print(self.fetch_data_incident_image(incident_id, images_string, table_name))
    #     old_image_string = "this and athat"
    #     print(old_image_string)
    #     if old_image_string == "noimage":
    #         sql_query = f"""UPDATE {table_name} SET images = '{images_string}' WHERE incident_id = '{incident_id}'"""
    #         self.cursor_database.execute(sql_query)
    #     else:
    #         new_image_string = old_image_string + "," + images_string
    #         image_array = new_image_string.split(",")
    #         sql_query = f"""UPDATE {table_name} SET images = '{image_array}' WHERE incident_id = '{incident_id}'"""
    #         self.cursor_database.execute(sql_query)


    def update_data_incident_image(self, incident_id, images_string, table_name):

        new_urls_string = images_string.replace(" ", "") + ","
        old_urls = self.fetch_data_incident_image(incident_id, images_string, table_name)[0][0]
        old_urls_string = ",".join(old_urls).replace(" ", "") 
        sql_query = ""
        if old_urls_string == new_urls_string:
            print("old string equiates to new string")
            pass
        elif old_urls_string == "noimage":
            print(self.fetch_data_incident_image(incident_id, images_string, table_name)[0][0])
            while new_urls_string[-1] ==",":
                new_urls_string = new_urls_string[:-1]
            sql_query1 = f"""UPDATE {table_name} SET images = """
            sql_query2 = """'{""" + new_urls_string + """}' WHERE incident_id = """
            sql_query3 = f"""'{incident_id}'"""
            sql_query = sql_query1 + sql_query2 + sql_query3
            self.cursor_database.execute(sql_query)
        else:           
            new_images_string = new_urls_string + old_urls_string
            while new_images_string[-1] ==",":
                new_images_string = new_images_string[:-1]
            sql_query1 = f"""UPDATE {table_name} SET images = """
            sql_query2 = """'{""" + new_images_string + """}' WHERE incident_id = """
            sql_query3 = f"""'{incident_id}'"""
            sql_query = sql_query1 + sql_query2 + sql_query3
            self.cursor_database.execute(sql_query)

    def update_data_incident_video(self, incident_id, videos_string, table_name):
        new_urls_string = videos_string.replace(" ", "") + ","
        old_urls = self.fetch_data_incident_video(incident_id, videos_string, table_name)[0][0]
        old_urls_string = ",".join(old_urls).replace(" ", "") 
        sql_query = ""
        if old_urls_string == new_urls_string:
            print("old string equiates to new string")
            pass
        elif old_urls_string == "novideo":
            new_urls_string = videos_string.replace(" ", "")
            while new_urls_string[-1] ==",":
                new_urls_string = new_urls_string[:-1]
            sql_query1 = f"""UPDATE {table_name} SET videos = """
            sql_query2 = """'{""" + new_urls_string + """}' WHERE incident_id = """
            sql_query3 = f"""'{incident_id}'"""
            sql_query = sql_query1 + sql_query2 + sql_query3
            self.cursor_database.execute(sql_query)
        else:
            new_videos_string = new_urls_string + old_urls_string
            while new_videos_string[-1] ==",":
                new_videos_string = new_videos_string[:-1]
            sql_query1 = f"""UPDATE {table_name} SET videos = """
            sql_query2 = """'{""" + new_videos_string + """}' WHERE incident_id = """
            sql_query3 = f"""'{incident_id}'"""
            sql_query = sql_query1 + sql_query2 + sql_query3
            self.cursor_database.execute(sql_query)
        # self.cursor_database.execute(sql_query)



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
