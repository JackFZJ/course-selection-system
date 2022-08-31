# name1="hello_flask"
# password1="123456"
# db1="courseSystem"
# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://"+name1+":"+password1+"@localhost:5432/"+db1+"?client_encoding=utf8"
# SQLALCHEMY_TRACK_MODIFICATIONS = False
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DEBUG = True
    SECRET_KEY = 'SAFDAEF12E'
    SESSION_COOKIE_SAMESITE=None
    SESSION_COOKIE_SECURE=True