"""Info endpoint
Module to handle the blueprint for the info endpoint. It has the info
function which will handle the "GET" method and imports the necessary
modules for this to work.
"""
import logging as log
from configparser import ConfigParser
from flask import request
from flask import Blueprint

from ... import AGGREGATOR_CONFIG_FILE

INFO = Blueprint('info', __name__)

@INFO.route('/', methods=["GET"])
@INFO.route('/info', methods=["GET"])
def info():
    """Show information about the Aggregator service.
    This endpoint will return a JSON with the information of this Aggregator
    Aggregator. It only handles "GET" methods and has two endpoints: "/"
    and "/info", both of them call this function.
    """
    result = dict()
    http_code = int()
    if request.method == 'GET':
        result, http_code = get_aggregator_info(
            conf_file=AGGREGATOR_CONFIG_FILE
        )

    return result, http_code

def get_aggregator_info(conf_file, include_datasets=True):
    """Get the configuration related to the service.
    Parse the configuration file searching for the aggregator data.

    Not implemented:
    Should build a configuration file from flags!

    :param confFile: [description]
    :type confFile: [type]
    :return: [description]
    :rtype: [type]
    """

    aggregator_conf = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str

    try:
        # Read configuration file
        log.debug("Reading configuration file '%s'.", conf_file)
        config.read(conf_file)

        #Take aggregator and organization data
        log.debug("Parsing configuration file.")
        aggregator_conf = dict(config["aggregator"])
        aggregator_conf["info"] = dict(config["aggregatorInfo"])
        aggregator_conf["organization"] = dict(config["organization"])
        aggregator_conf["organization"]["info"] = dict(config["organizationInfo"])

    except KeyError:
        log.error("Configuration file not found or bad writed.")
        http_code = 503

    return aggregator_conf, http_code
