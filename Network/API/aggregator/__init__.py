"""Beacon Aggregator package
"""

import os
import logging
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

### Constants ###
AGGREGATOR_CONFIG_FILE = "aggregator/configuration.ini"
SERVICES_KNOWN = "aggregator/services.ini"
API_VERSION = "v1.1.0"
VERSION = "v0.1.0"
SERVICE_TYPE = "GA4GHBeaconAggregator"
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
