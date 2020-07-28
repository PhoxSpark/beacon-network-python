"""Info endpoint
Module to handle the blueprint for the info endpoint. It has the info
function which will handle the "GET" method and imports the necessary
modules for this to work.
"""
import logging as log
from configparser import ConfigParser
from flask import request
from flask import Blueprint

from ... import DATABASE_CONFIG_FILE
from ... import BEACON_CONFIG_FILE
from ..controller.dao import AccesDataBase

INFO = Blueprint('info', __name__)

@INFO.route('/', methods=["GET"])
@INFO.route('/info', methods=["GET"])
def info():
    """Show information about the Beacon service.
    This endpoint will return a JSON with the information of this Beacon
    Aggregator. It only handles "GET" methods and has two endpoints: "/"
    and "/info", both of them call this function.
    """
    result = dict()
    http_code = int()
    if request.method == 'GET':
        result, http_code = get_beacon_info(
            conf_file=BEACON_CONFIG_FILE
        )

    return result, http_code

def get_beacon_info(conf_file, include_datasets=True):
    """Get the configuration related to the service.
    Parse the configuration file searching for the beacon data.

    :param conf_file: file to take the configuration
    :type conf_file: str()
    :param include_datasets: set if datasets will be included defaults to True
    :type include_datasets: bool, optional
    :return: dictionary with the configuration of the beacon and the hhtp code
    :rtype: dict(), int()
    """

    beacon_conf = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str

    try:
        # Read configuration file
        log.debug("Reading configuration file '%s'.", conf_file)
        config.read(conf_file)

        #Take beacon and organization data
        log.debug("Parsing configuration file.")
        beacon_conf = dict(config["beacon"])
        beacon_conf["info"] = dict(config["beaconInfo"])
        beacon_conf["organization"] = dict(config["organization"])
        beacon_conf["organization"]["info"] = dict(config["organizationInfo"])

        #Datasets
        if include_datasets:
            beacon_conf["datasets"] = take_datasets()
        else:
            beacon_conf["datasets"] = None

        #sampleAlleleRequests
        beacon_conf["sampleAlleleRequests"] = [{"error" : "NOT IMPLEMENTED"}]

    except KeyError:
        log.error("Configuration file not found or bad writed.")
        http_code = 503

    return beacon_conf, http_code

def get_database_access(db_conf_file):
    """Get the information necessary to access the database.
    Parse the database configuration file in look for the database access
    data.

    :param dbConfFile: configuration file for the database
    :type dbConfFile: str()
    :return: dictionary with database configuration
    :rtype: dict()
    """

    db_conf = dict()
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str

    #Read configuration file
    log.debug("Reading configuration file '%s'.", db_conf_file)
    config.read(db_conf_file)

    #Take database data
    log.debug("Parsing database configuration file.")
    db_conf = dict(config["database"])

    return db_conf

def take_datasets():
    """Access database and take datasets

    :return: list of datasets
    :rtype: list()
    """
    tmp_dao = AccesDataBase()
    tmp_return = list()

    tmp_dao.connect(get_database_access(DATABASE_CONFIG_FILE))
    tmp_dao.simple_select_data("beacon_dataset_table")
    if tmp_dao.response is None:
        tmp_return = ["ERROR CONNECTING DATABASE"]
    else:
        tmp_return = tmp_dao.response

    tmp_dao.disconnect()

    return tmp_return
