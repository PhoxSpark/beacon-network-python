"""API Service
This module contains the service classes for the endpoints of
FlaskRESTPlus. It can be started calling the function start(),
by default, the function will start without debug mode.
"""

from __future__ import absolute_import

import logging

import pyba.blueprints as bp

from pyba import APP

def start(debug=False):
    """Function to start Flask service.
    This function will start flask service with REST capabilities. If
    there is specified a true boolean when called, it will extend the
    logging information and relaunch the server every time Flask
    detects it changed something on the script.

    :param options: Dictionary with all the flags necessary for Flask.
    :type debug_enabled: dictionary
    """

    logging.info("Initializing Flask service. Debug=%s", debug)

    #Load all the blueprints, they have to be imported before!
    logging.info("Loading blueprints")
    logging.debug("Loading INFO_ROOT blueprint")
    APP.register_blueprint(bp.i.INFO_ROOT)
    logging.debug("Loading NETWORKS blueprint")
    APP.register_blueprint(bp.n.NETWORKS)
    logging.debug("Loading PARSER blueprint")
    APP.register_blueprint(bp.p.PARSER)
    logging.debug("Loading REGISTERED_BEACONS blueprint")
    APP.register_blueprint(bp.rb.REGISTERED_BEACONS)
    logging.debug("Loading REGISTRIES blueprint")
    APP.register_blueprint(bp.r.REGISTRIES)
    logging.debug("Loading SERVICE_INFO blueprint")
    APP.register_blueprint(bp.si.SERVICE_INFO)
    logging.debug("Loading SERVICE_TYPES blueprint")
    APP.register_blueprint(bp.st.SERVICE_TYPES)
    logging.debug("Loading SERVICES blueprint")
    APP.register_blueprint(bp.s.SERVICES)

    #Start the service depending if debug was specified or not.
    if debug:
        logging.info("Starting Flask")
        APP.run(host='0.0.0.0', port='5000', debug=True)
    else:
        logging.info("Starting Flask")
        APP.run(host='0.0.0.0', port='5000')



if __name__ == "__main__":
    pass
