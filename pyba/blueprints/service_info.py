"""
Module for service info endpoint
"""
from __future__ import absolute_import

import logging
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import Api

import pyba.library as lib

SERVICE_INFO = Blueprint('service-info', __name__)
API = Api(SERVICE_INFO)



@API.route("/service-info")
class EndpointServiceInfo(Resource):
    """Endpoint that will return the service info.

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self):
        """GET on /service-info

        :return: Return the service info
        :rtype: dictionary (JSON)
        """

        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointServiceInfo",
                     client_ip)

        logging.debug("Filling variable service_info_json with "
                      "function end endpoint_service_info")
        service_info_json = lib.api.endpoint_service_info_get()

        logging.info("Showing EndpointServiceInfo as JSON to %s",
                     client_ip)
        return service_info_json



if __name__ == "__main__":
    pass
