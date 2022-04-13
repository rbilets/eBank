import os

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(DIR, "database.db")


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'you-will-never-know'
