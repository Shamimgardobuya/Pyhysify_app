import os
from datetime import timedelta
class Config:
    SECRET_KEY = os.getenv("FLASK_APP_KEY") or "34738748374"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or "sqlite:///app.db"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "frfrfrf"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    PROPAGATE_EXCEPTIONS = True
    JWT_TOKEN_LOCATION = ['headers']
    