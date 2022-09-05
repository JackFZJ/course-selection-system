# name1="hello_flask"
# password1="123456"
# db1="courseSystem"
# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://"+name1+":"+password1+"@localhost:5432/"+db1+"?client_encoding=utf8"
# SQLALCHEMY_TRACK_MODIFICATIONS = False
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DEBUG = True
    # SECRET_KEY = 'SAFDAEF12E'
    JWT_SECRET_KEY='f(#4!@s5zMaf9+rw7j'
    # NAMEKO_AMQP_URI=os.getenv("NAMEKO_AMQP_URI", "amqp://localhost")
    # NAMEKO_AMQP_URI="amqp://localhost"
    NAMEKO_AMQP_URI="amqp://root:root@rabbitmq"
    # NAMEKO_AMQP_URI="amqp://guest:guest@localhost"
    # SESSION_COOKIE_SECURE=True
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=8)