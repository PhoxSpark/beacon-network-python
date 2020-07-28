import logging as log
import requests
from configparser import ConfigParser
from flask import request
from flask import Blueprint
from .info import get_aggregator_info
from ... import SERVICES_KNOWN
from ... import AGGREGATOR_CONFIG_FILE

QUERY = Blueprint('query', __name__)

@QUERY.route('/query', methods=["GET", "POST"])
def query():
    http_code = 200
    services = dict()
    response = list()
    params = {
        "referenceName"           : request.args.get('referenceName'),
        "start"                   : request.args.get('start'),
        "startMin"                : request.args.get('startMin'),
        "startMax"                : request.args.get('startMax'),
        "end"                     : request.args.get('end'),
        "endMin"                  : request.args.get('endMin'),
        "endMax"                  : request.args.get('endMax'),
        "referenceBases"          : request.args.get('referenceBases'),
        "alternateBases"          : request.args.get('alternateBases'),
        "variantType"             : request.args.get('variantType'),
        "assemblyId"              : request.args.get('assemblyId'),
        "mateName"                : request.args.get('mateName'),
        "datasetIds"              : request.args.get('datasetIds'),
        "includeDatasetResponses" : request.args.get('includeDatasetResponses')
    }
    self_information = get_aggregator_info(AGGREGATOR_CONFIG_FILE)
    services = get_services()
    if (len(services["GA4GHBeacon"]) + len(services["GA4GHBeaconAggregator"]) < 1):
        log.error("No services to query.")
        response = {"error" : "No services to query."}
        http_code = 503
    elif http_code == 200:
        response = {str(self_information[0]["id"]) : query_beacons(
            params,
            services["GA4GHBeacon"],
            services["GA4GHBeaconAggregator"]
        )}
    return response, http_code

def query_beacons(params, beacons, aggregators):
    """[summary]

    :param params: [description]
    :type params: [type]
    :param beacons: [description]
    :type beacons: [type]
    :param aggregators: [description]
    :type aggregators: [type]
    :param method: [description]
    :type method: [type]
    :return: [description]
    :rtype: [type]
    """
    response = list()
    working_services_url = list()
    queries = list()

    #Check if services are working
    for beacon in beacons:
        req = requests.get(beacon["serviceURL"] + "/info")
        if req.status_code == 200:
            working_services_url.append(beacon["serviceURL"])
        else:
            log.warning(
                "Beacon %s answered %s code, not quering it.",
                beacon["name"], req.status_code
            )
    for aggregator in aggregators:
        req = requests.get(aggregator["serviceURL"] + "/info")
        if req.status_code == 200:
            working_services_url.append(aggregator["serviceURL"])
        else:
            log.warning(
                "Beacon Aggregator %s answered %s code, not quering it.",
                aggregator["name"], req.status_code
                )

    #Build the url to every service working
    for service in working_services_url:
        query_string = service + "?"
        for param in params:
            if param is not None:
                try:
                    query_string = query_string + param + "=" + params[param] + "&"
                except TypeError:
                    pass
        queries.append(query_string)

    #Make a query to every url
    for query in queries:
        req = requests.get(query)
        aggregator = False

        #Check if the response is from an aggregator or from a beacon.
        for dic in req.json():
            if type(req.json()[dic]) == list():
                for item in req.json()[dic]:
                    response.append(item)
        response.append(req.json())

    return response

def get_services():
    """[summary]

    :return: [description]
    :rtype: [type]
    """
    services = dict()
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str

    config.read(SERVICES_KNOWN)

    services["GA4GHRegistry"] = list()
    services["GA4GHBeacon"] = list()
    services["GA4GHBeaconAggregator"] = list()

    for data in dict(config):
        try:
            if dict(config[data])["ServiceType"] == "GA4GHRegistry" \
            and data != "DEFAULT":
                services["GA4GHRegistry"].append(dict(config[data]))
            if dict(config[data])["ServiceType"] == "GA4GHBeacon" \
            and data != "DEFAULT":
                services["GA4GHBeacon"].append(dict(config[data]))
            if dict(config[data])["ServiceType"] == "GA4GHBeaconAggregator" \
            and data != "DEFAULT":
                services["GA4GHBeaconAggregator"].append(dict(config[data]))
        except KeyError:
            pass

    return services