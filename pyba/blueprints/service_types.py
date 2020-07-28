"""
Module for service types endpoint
"""
from __future__ import absolute_import

import logging
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import Api

import pyba.library as lib

SERVICE_TYPES = Blueprint('service_types', __name__)
API = Api(SERVICE_TYPES)



@API.route("/service_types")
class EndpointServiceTypes(Resource):
    """Ennumerate the known service types
    This service_types only have a GET method available, it will
    return the known service types.

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self):
        """GET on /service_types

        :return: Returns the known service types, probably just 3
        :rtype: dictionary (JSON)
        """

        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointServiceTypes",
                     client_ip)

        logging.debug("Filling variable service_types with function "
                      "endpoint_service_types_get")
        service_types_json = lib.api.endpoint_service_types_get()

        logging.info("Showing EndpointServiceTypes result as JSON "
                     "to %s", client_ip)
        return service_types_json



if __name__ == "__main__":
    pass
