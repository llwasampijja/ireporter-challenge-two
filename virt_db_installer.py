import psycopg2

db_connect = psycopg2.connect(\
"dbname='ireporter_db' \
user='andela' \
host='localhost' \
password='bootcamp'")
db_connect.autocommit = True

cursor_database = db_connect.cursor()
    
def create_tables():
        """method for creating all the tables required for the application"""
        # create user tables
        cursor_database.execute(
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
        cursor_database.execute(
            """CREATE TABLE IF NOT EXISTS incident_types (
                incident_type_id serial PRIMARY KEY,
                incident_type_name varchar
            )"""
        )

        # create interventions tables
        cursor_database.execute(
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
        cursor_database.execute(
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



if __name__ == "__main__":
    create_tables()


