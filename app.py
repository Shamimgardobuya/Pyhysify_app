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
from config import Config

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')


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
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app) 
    api.handle_error = app.handle_exception
    bcrypt.init_app(app)
    jwt.init_app(app)
    sock.init_app(app)
    redis_client.init_app(app, decode_responses = True)
    pagination.init_app(app, db=db)
    CORS(app, origins=os.getenv("FRONTEND_URL"))
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
    
    
    