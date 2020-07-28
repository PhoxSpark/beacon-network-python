"""Initialization of the app
This __init__ will initialize the Flask API and the loggings. As this
is in the main module, the constants will share through all the
submodules.
"""

from __future__ import absolute_import

#package imports:
import logging
from datetime import datetime
from flask import Flask
from flask_restplus import Api as BaseApi
from flask_cors import CORS

# REMEMBER TO UPDATE THE VERSION ON EACH COMMIT!!!
APP_NAME = "PyBA"
APP_VERSION = "0.2.5" #Date: 17/12/2019
API_VERSION = "1.1.0"
EXECUTION_TIME = str(datetime.now())[:18]

CONFIGURATIONS = {
    "PORT" : None,
    "IP" : None,
    "LOGS_FOLDER" : None,
    "CONFIG_BEACONS" : None,
    "CONFIG_REGISTRIES" : None
    }


class ModifiedApi(BaseApi):
    """Workaround to make the root route to work
    Workaround found on GitHub issues
    (https://github.com/noirbizarre/flask-restplus/issues/247) to allow
    the root route to reender when Swagger is in another route.
    Aparently, RESTPlus isn't too good with some things and we have to
    modify some functions of the object. IMPORTANT: This have to been
    loaded BEFORE the API constant is created because the API constant
    will use the ModifiedApi class created here instead of the Api
    module.

    :param BaseApi: The Api module from flask_restplus library.
    :type BaseApi: object
    """

    def _register_doc(self, app_or_blueprint):
        """Modification of an actual piece of code on the Api module.

        :param app_or_blueprint: [description]
        :type app_or_blueprint: [type]
        """
        # This is just a copy of the original implementation with the
        # last line commented out.
        if self._add_specs and self._doc:
            # Register documentation before root if enabled
            app_or_blueprint.add_url_rule(self._doc,
                                          'doc',
                                          self.render_doc)
        # app_or_blueprint.add_url_rule(self._doc, 'root',
        # self.render_root)

    @property
    def base_path(self):
        return ''


# Flask initialization
APP = Flask(__name__)

# Flask CORS Initialization (before API to import properly)
CORS(APP)

# Flask RESTPlus Initialization
API = ModifiedApi(APP, doc='/swagger')

# Logs initialization
HANDLER = logging.StreamHandler()

LOGGFLASK = logging.getLogger('werkzeug')
LOGGLIB = logging.getLogger('urllib3.connectionpool')
LOGGROOT = logging.getLogger()
LOGGROOT.addHandler(HANDLER)

# Disable/enable some loggers for get a smaller console output. Debug
# mode will reenable some.
APP.logger.disabled = True
LOGGFLASK.disabled = False
LOGGLIB.disabled = False
LOGGROOT.disabled = False

#This put the loggs into INFO level, even the disabled ones.
LOGGROOT.setLevel(logging.INFO)
LOGGLIB.setLevel(logging.INFO)
LOGGFLASK.setLevel(logging.INFO)
