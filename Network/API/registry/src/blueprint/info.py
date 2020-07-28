"""Information blueprint
"""
import logging as log
from configparser import ConfigParser
from flask import request
from flask import Blueprint

from ... import REGISTRY_CONFIG_FILE

INFO = Blueprint('info', __name__)

@INFO.route('/', methods=["GET"])
@INFO.route('/info', methods=["GET"])
def info():
    """Information about the Registry service
    Endpoint to show information of the Registry service. It will
    take all the information from the configuration file.
    """
    result = dict()
    http_code = 200
    if request.method == "GET":
        result, http_code = get_registry_info(
            conf_file=REGISTRY_CONFIG_FILE
        )

    return result, http_code

def get_registry_info(conf_file):
    """Get the configuration related to the service.
    Parse the configuration file searching for the registry data.

    Not implemented:
    Should build a configuration file from flags!

    :param confFile: [description]
    :type confFile: [type]
    :return: [description]
    :rtype: [type]
    """

    reg_conf = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str

    try:
        # Read configuration file
        log.debug("Reading configuration file '%s'.", conf_file)
        config.read(conf_file)

        #Take beacon and organization data
        log.debug("Parsing configuration file.")
        reg_conf = dict(config["registry"])
        reg_conf["info"] = dict(config["registryInfo"])
        reg_conf["organization"] = dict(config["organization"])
        reg_conf["organization"]["info"] = dict(config["organizationInfo"])

    except KeyError as error:
        log.error("Configuration file not found or bad writed. Additional information: %s", error)
        http_code = 503

    return reg_conf, http_code
