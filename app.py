from flask import Flask
from flask_sock import Sock
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_restful import  Api
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
import logging
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_redis import FlaskRedis
import redis
from dotenv import load_dotenv
from flask_rest_paginate import Pagination

load_dotenv()

REDIS_URL = "redis://localhost:6379/0"


db = SQLAlchemy()
migrate = Migrate()
api = Api()
bcrypt = Bcrypt()
jwt = JWTManager()
redis_client = FlaskRedis()
sock = Sock()
pagination = Pagination()


def create_app():
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///app.db"
    
    app.config['SECRET_KEY'] = os.getenv("FLASK_APP_KEY") or "34738748374"
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "frfrfrf"
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    

    db.init_app(app)
    migrate.init_app(app)
    api.init_app(app) 
    bcrypt.init_app(app)
    jwt.init_app(app)
    sock.init_app(app)
    redis_client.init_app(app, decode_responses = True)
    pagination.init_app(app, db=db)
    CORS(app, origins="http://localhost:3000")
    app.logger.setLevel(logging.DEBUG)
    
    with app.app_context():
        import models
        db.create_all()
        
    return app
    
