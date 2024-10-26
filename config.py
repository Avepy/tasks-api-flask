import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'tasks.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "please_change_me"
    APISPEC_TITLE = "Task Management API"
    APISPEC_VERSION = "1.0.0"
    SERVER_NAME = "localhost:5000"
