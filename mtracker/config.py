import os
import dotenv

dotenv.load_dotenv()


class Config:

    DBMS = os.environ.get("DBMS")
    DB_DRIVER = os.environ.get("DB_DRIVER")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"{DBMS}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY")
