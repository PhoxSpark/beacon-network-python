"""
Module for the registered beacons endpoint
"""
from __future__ import absolute_import

import logging
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import Api

import pyba.library as lib

REGISTERED_BEACONS = Blueprint('registered_beacons', __name__)
API = Api(REGISTERED_BEACONS)



@API.route("/registered_beacons")
class EndpointRegisteredBeacons(Resource):
    """[summary]

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def put(self):
        """PUT on /registered_beacons
        """

        client_ip = lib.api.get_client_ip()

        logging.info("PUT Requested from %s on "
                     "EndpointRegisteredBeacons", client_ip)



if __name__ == "__main__":
    pass
