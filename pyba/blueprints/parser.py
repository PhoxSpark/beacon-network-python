"""
"""
from __future__ import absolute_import

import logging
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import Api

import pyba.library as lib

PARSER = Blueprint('parser', __name__)
API = Api(PARSER)

@API.route("/<endpoint>")
class EndpointCapturer(Resource):
    """Endpoint to redirect all the unidentified input.
    This endpoint will redirect every unidentified endpoint to all the
    known beacons to capture all their output.

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self, endpoint): # pylint: disable=no-self-use
        """GET on not recognised/registered/programmed endpoint.

        :return: It will return the API Rest result, if everything goes
                 well, it will be in JSON format.
        :rtype: dictionary (JSON)
        """
        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointCapturer",
                     client_ip)
        logging.debug("Getting list of known beacons from file "
                      "'services.conf', section 'beacons'")
        known_beacons = lib.config.read_external_configuration("beacons",
                                                               "beacons.conf")
        logging.debug("Checking number of beacons obtained")
        if known_beacons:
            logging.info("%s beacons found", len(known_beacons))
            logging.debug("Filling result_json with function "
                          "endpoint_capturer_get()")
            result_json = lib.api.endpoint_capturer_get(known_beacons,
                                                        endpoint)
        else:
            logging.error("No known beacons found!")
            result_json = {"ERROR" : "No known beacons found!"}
        logging.info("Showing captured responses as JSON to %s",
                     client_ip)
        return result_json

if __name__ == "__main__":
    pass
