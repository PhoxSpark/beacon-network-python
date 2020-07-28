"""
Module for all related to services endpoint.
"""
from __future__ import absolute_import

import logging
from flask import Blueprint
from flask_restplus import Resource
from flask_restplus import Api

import pyba.library as lib

SERVICES = Blueprint('services', __name__)
API = Api(SERVICES)



@API.route("/services")
class EndpointServices(Resource):
    """This endpoint can filter and show data from known beacons.
    When a GET method is maded to this endpoint, the return will be a
    JSON with all the serviceInfo from the known services, this can be
    Registry, Beacon or Beacon Aggregator, depending on which services
    has the network.

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self):
        """GET on /services
        This GET method will accept some querys: servuceType, model,
        listFormat, apiVersion. Those methods will be filters for the
        /services endpoint.

        :return: serviceInfo from the known beacons
        :rtype: dictionary (JSON)
        """

        client_ip = lib.api.get_client_ip()
        #querys = {"serviceType" : request.args.get("serviceType"),
        #          "model" : request.args.get("model"),
        #          "listFormat" : request.args.get("listFormat"),
        #          "apiVersion" : request.args.get("apiVersion")}

        logging.info("GET Requested from %s on EndpointServices",
                     client_ip)

    def post(self):
        """[summary]
        """

        client_ip = lib.api.get_client_ip()

        logging.info("POST Requested from %s on EndpointServices",
                     client_ip)


@API.route("/services/<ids>")
class EndpointServicesId(Resource):
    """List the service details
    This endpoint will list all the details of a specific service.

    :param Resource: Represent the abstract RESTPlus Resource.
    :type Resource: RESTPlus
    """

    def get(self, ids):
        """GET on /services/<ids>

        :param ids: [description]
        :type ids: [type]
        """

        client_ip = lib.api.get_client_ip()

        logging.info("GET Requested from %s on EndpointServicesId",
                     client_ip)
        logging.info("ID specified: %s", ids)
        #servicesid_dict = api_lib.endpoint_services

    def put(self, ids):
        """/PUT on /services/<ids>

        :param ids: [description]
        :type ids: [type]
        """
        client_ip = lib.api.get_client_ip()

        logging.info("PUT Requested from %s on EndpointServicesId",
                     client_ip)
        logging.info("ID specified: %s", ids)

    def delete(self, ids):
        """DELETE on /services/<ids>

        :param ids: [description]
        :type ids: [type]
        """

        client_ip = lib.api.get_client_ip()

        logging.info("DELETE Requested from %s on EndpointServicesId",
                     client_ip)
        logging.info("ID specified: %s", ids)



if __name__ == "__main__":
    pass
