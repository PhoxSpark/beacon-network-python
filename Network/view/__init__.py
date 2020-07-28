"""View package
"""

import os
import logging
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_bootstrap import Bootstrap

### Constants ###
VERSION = "v0.1.0"

### create flask object ###
APP = Flask(__name__)
CORS(APP)
Bootstrap(APP)

### logging specific ###
logging.basicConfig(level=logging.DEBUG)
### end logging specific ###
