import psycopg2
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase: Client = create_client(os.environ.get("SUPABASE_URL"),
                                 os.environ.get("SUPABASE_KEY"))

def db_get_users(app,user_id):
    try:
        # db_user = os.getenv("POSTGRESQL_DB_USER")
        # db_password = os.getenv("POSTGRESQL_DB_PASSWORD")
        # db_host = os.getenv("POSTGRESQL_DB_HOSTNAME")
        # db_port = os.getenv("POSTGRESQL_DB_PORT")
        # db_name = "twinkle" # Assuming database name is 'twinkle' based on previous conversation
        #
        # app.logger.info(f"Attempting to connect to PostgreSQL with:")
        # app.logger.info(f"  Host: {db_host}")
        # app.logger.info(f"  Port: {db_port}")
        # app.logger.info(f"  User: {db_user}")
        # app.logger.info(f"  DB Name: {db_name}")
        # app.logger.info(f"  Password: {'*' * len(db_password) if db_password else 'None'}") # Mask password in logs

        # conn = psycopg2.connect(host=db_host,
        #                         port=db_port,
        #                         user=db_user,
        #                         dbname=db_name,
        #                         password=db_password)

        response = supabase.table('users').select("*").eq('id', user_id).execute()
        todos = response.data
        app.logger.info(f"Connected to Database {todos}")
        return todos
    except Exception as e:
        app.logger.error(f"Error connecting to database: {e}")
        return None

def db_get_all_users(app):
    try:
        response = supabase.table('users').select("*").execute()
        users = response.data
        app.logger.info(f"Connected to Database {users}")
        return users
    except Exception as e:
        app.logger.error(f"Error connecting to database: {e}")
        return None

def db_create_user(app,username,email):
    try:
        user = supabase.table('users').insert({'username': username, 'email': email}).execute()
        app.logger.info(f"User created successfully {user}")
        return user
    except Exception as e:
        app.logger.error(f"Error connecting to database: {e}")
        return None
