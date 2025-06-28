import os

from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_community.utilities import SQLDatabase

def init_db():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")

    uri = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    try:
        db = SQLDatabase.from_uri(uri)
        return db
    except Exception as e:
        return f"Failed to initialize database\nError: {e}"