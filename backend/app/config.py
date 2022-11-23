from re import T
from flask import Config
import os

class Config(Config):
    """
    Flask configuration class and MONGODB.
    """
    enable_utc = True
    APP_NAME = "Flask-App"
    MONGODB_DB = os.getenv("MONGODB_DB", "api")
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "root")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "root")
    MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
    MONGODB_PORT = 27017
    JWT_SECRET_KEY = "secret"
    ERROR_404_HELP = False
    AWS_BUCKET_NAME = "kpi-spa-demo-dft"