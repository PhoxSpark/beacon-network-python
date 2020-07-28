"""
Module for /info and / (root)
"""

from __future__ import absolute_import

import logging
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import Api

import pyba.library as lib

INFO_ROOT = Blueprint('info_root', __name__)
API = Api(INFO_ROOT)



@API.route('/')
@API.route('/info')
class EndpointInfo(Resource):
    """This endpoint will give all the information specified.
    When called the endpoint /info or /, returns a JSON with the
    information of the Beacon Aggregator.

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self):
        """GET on root or /info endpoints

        :return: It returns the service info object model from the
                 specification with the concrete BA information.
        :rtype: dictionary (JSON)
        """

        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointInfo",
                     client_ip)

        logging.debug("Filling variable info_json with function "
                      "endpoint_info_get()")
        info_json = lib.api.endpoint_info_get()

        logging.info("Showing EndpointInfo result as JSON to %s",
                     client_ip)
        return info_json



if __name__ == "__main__":
    pass
