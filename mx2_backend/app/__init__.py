from calendar import c
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask import Blueprint
import logging
import os
from app.config import Config

api_bp = Blueprint('api', __name__, url_prefix='/api/v1') 
api = Api(api_bp)


# import apis from other modules
from app.campus.controller import campus_api
from app.user.controller import auth_api, user_api, student_api, admin_api, teacher_api
from app.course.controller import course_api
from app.order.controller import order_api
from app.user import register_user_lookup

api.add_namespace(campus_api)
api.add_namespace(auth_api)
api.add_namespace(user_api)
api.add_namespace(student_api)
api.add_namespace(admin_api)
api.add_namespace(teacher_api)
api.add_namespace(course_api)
api.add_namespace(order_api)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #Logger (app.root_path is the application root path)
    log_path = os.path.join(app.root_path, 'logs')
    
    # check if log directory exists, if not create it
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    # create a file handler --> logging module generation need satisfying some rules
    # where you want to store the logs
    file_handler = logging.FileHandler(f"{log_path}/default.log")
    
    # set the logging level
    file_handler.setFormatter(
        # timestamp, module name, level, message
        logging.Formatter("%(asctime)s:%(levelname)s:%(module)s:%(message)s")
    )

    # add the handler to the app (default logger in terminal)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)



    # DB
    MongoEngine(app)



    # CORS (api allows cross-origin requests from any origin)
    # Headers: cross-origin-resource-policy is set to allow cross-origin requests
    CORS(app)



    # JWT
    jwt = JWTManager(app)
    register_user_lookup(jwt)



    # API register
    app.register_blueprint(api_bp)

    return app