"""
"""
from __future__ import absolute_import

import logging
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import Api

import pyba.library as lib

NETWORKS = Blueprint('networks', __name__)
API = Api(NETWORKS)



@API.route("/networks")
class EnpointNetworks(Resource):
    """Endpoint to show the current network info where this service is
    registered in.

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self):
        """GET on /networks
        """

        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointNetworks",
                     client_ip)

        logging.debug("Filling networks_dict with function "
                      "endpoint_networks_get result")
        networks_dict = lib.api.endpoint_networks_get()

        logging.info("Showing EndpointNetwork as JSON to %s",
                     client_ip)
        return networks_dict


@API.route("/networks/<ids>")
class EndpointNetworksId(Resource):
    """Endpoint to show the info of a specific network where this
    service is registered in.

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self, ids):
        """GET on /networks/<ids>

        :param ids: The ID of the specific network to show
        :type ids: string
        """

        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointNetworksId",
                     client_ip)
        logging.info("ID specified: %s", ids)



if __name__ == "__main__":
    pass
