"""
Module for all related to registries endpoint.
"""
from __future__ import absolute_import

import logging
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import Api

import pyba.library as lib

REGISTRIES = Blueprint('registries', __name__)
API = Api(REGISTRIES)



@API.route("/registries")
class EndpointRegistries(Resource):
    """This is equivalent to GET /services?serviceType=GA4GHRegistry

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self):
        """GET on /registries
        """

        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointRegistries",
                     client_ip)


@API.route("/registries/<ids>")
class EndpointRegistriesId(Resource):
    """This is equivalent to GET /services/{id}

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self, ids):
        """GET on /registries/<ids>
        """

        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointRegistriesId",
                     client_ip)
        logging.info("ID specified: %s", ids)



if __name__ == "__main__":
    pass
