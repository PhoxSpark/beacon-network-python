"""Beacon package
"""

import os
import logging
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

### Constants ###
DATABASE_CONFIG_FILE = "beacon/database.ini"
BEACON_CONFIG_FILE = "beacon/configuration.ini"
API_VERSION = "v1.1.0"
VERSION = "v0.4.0"
SERVICE_TYPE = "GA4GHBeacon"
EXECUTION_DATE = datetime.today().strftime('%Y-%m-%d')

### create flask object ###
API = Flask(__name__)
CORS(API)

### swagger specific ###
SWAGGER_URL = '/spec'
API_URL = '/static/spec.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
API.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

### logging specific ###
logging.basicConfig(level=logging.DEBUG)
### end logging specific ###
