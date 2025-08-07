from flask import Flask, jsonify, request
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
from datetime import timedelta
from dotenv import load_dotenv
from flask_rest_paginate import Pagination
from jwt.exceptions import ExpiredSignatureError, InvalidIssuerError, InvalidAudienceError, InvalidTokenError
from werkzeug.exceptions import HTTPException

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
    app.config["SQLALCHEMY_DATABASE_URI"] =  os.getenv('DATABASE_URI') or "sqlite:///app.db"
    
    app.config['SECRET_KEY'] = os.getenv("FLASK_APP_KEY") or "34738748374"
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "frfrfrf"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app) 
    api.handle_error = app.handle_exception
    bcrypt.init_app(app)
    jwt.init_app(app)
    sock.init_app(app)
    redis_client.init_app(app, decode_responses = True)
    pagination.init_app(app, db=db)
    CORS(app, origins="http://localhost:3000")
    app.logger.setLevel(logging.DEBUG)
    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header, jwt_payload):
            return jsonify(code="token_expired", message="Your session has expired. Please log in again."), 401
    
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = redis_client.get(jti)
        return token_in_redis is not None
    
    @jwt.invalid_token_loader
    def check_token_invalid(e):
        return jsonify(code="invalid_token", message="Your token is invalid. Please log in to use the correct one."), 401
    
    
    with app.app_context():
        import models
        db.create_all()
        
    return app
    
