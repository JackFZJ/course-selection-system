# --*--coding: utf-8 --*--
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_nameko import FlaskPooledClusterRpcProxy
from flask_jwt_extended import JWTManager
db=SQLAlchemy()
ma=Marshmallow()
mg = Migrate()
cors=CORS()
rpc=FlaskPooledClusterRpcProxy()
jwt = JWTManager()