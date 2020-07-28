"""API functions module
This module contains all the API related functions. The functions of
this module will be called only from the api module or from itself.

The use of nested functions will help on readability. Before this, the
functions were spreaded around this library. Now, with a quick look you
know what a function can do and what is it's pourpose.
"""

from __future__ import absolute_import

import logging
import json
import requests
from flask import request

import pyba.library as lib

#======================================================================#

def endpoint_capturer_get(known_beacons, endpoint):
    """Make the string for the query and send it to the known beacons.
    This function takes the string the user have input on the URL and
    resend it to the known beacons. If there's any, it will return an
    error in JSON format.

    The functions nested here are in order of execution.

    :param known_beacons: Dictionary with known beacons from the beacon
                          registry and files.
    :type_info known_beacons: dictionary
    :param endpoint: Endpoint parsed from the user input.
    :type_info endpoint: string
    :return: JSON file with all the output from the beacons.
    :rtype_info: dictionary
    """
    def capturer_get_sequence():
        """
        This function will load all the nested functions inside this
        encpoint capturer. It will read the param method to know which
        method will use.

        :return: JSON file with all the output from the beacons.
        """
        result_json = None
        full_query_string = endpoint_parser(str(request.query_string))
        logging.debug("Parsed endpoint: %s", full_query_string)

        result_json = endpoint_redirect(full_query_string)
        logging.debug("Endpoint redirect sequence finished.")

        return result_json

    def endpoint_parser(query_string):
        """Puts / + the endpoint writed + ? + the query writed on a string.
        This simple function will remove the unnecesary characters from the
        "request.query_string" function of Flask and will prepare the
        endpoint + querys to redirect it to it's known beacons.

        :param endpoint: It takes an endpoint without slash (/).
        :type_info endpoint: string
        :param query_string: It takes the query of an endpoint without
                             interrogation (?).
        :type_info query_string: string
        :return: It will return the full endpoint with querys to use it on a
                 request to the known beacons.
        :rtype_info: string
        """
        full_query_string = "/" + endpoint + "?" + query_string[2:]
        logging.debug("Endpoint parsed: %s", full_query_string)

        return full_query_string[:-1]

    def endpoint_redirect(full_query_string):
        """Redirect the user input to known beacons
        Takes the full query string and send it to the known beacons, it
        will try to handle not working beacons

        :param known_beacons: Dictionary of all the known beacons.
        :type_info known_beacons: dictionary
        :param full_query_string: endpoint + query writed by the user.
        :type_info full_query_string: string
        :return: JSON with the data returned by the beacons and classified
                 by their URL.
        :rtype_info: dictionary
        """
        json_load = None
        result_json = dict()
        errors_count = 0 # This int is for counting the errors to throw
                         # more information to the user.

        #This will ask in order to every beacon. It's ready to handle a
        #bad beacon or bar url or even an empty response, it will try to
        #recognise errors, but if the error is in JSON, it will show that
        #error.
        for beacon in known_beacons:
            error_this_lap = 0

            logging.info("Making query %s to beacon %s",
                         full_query_string, beacon)

            url = known_beacons[beacon]
            url_complete = url + full_query_string
            logging.debug("URL Created: %s", url_complete)

            try:
                json_tmp = requests.get(url_complete)
                logging.debug("Success requesting JSON to Beacon %s", beacon)

            except requests.exceptions.ConnectionError:
                error_this_lap = 1
                json_tmp = None
                logging.warning("Exception handled! Impossible to reach "
                                "beacon %s, ConnectionError", beacon)

            # If the service isn't working it can't get the JSON so it will
            # crash. We need to handle it.
            try:
                json_load = json_tmp.json()
                logging.debug("Success reading JSON data from query")

            except AttributeError:
                error_this_lap = 1
                json_load = {"error" : {"title" : "Empty Response", \
                            "content" : "The beacon didn't returned a "
                                        "JSON response or didn't returned "
                                        "a response at all. Maybe the "
                                        "beacon is unrechable, isn't "
                                        "online or the URL have a "
                                        "mispelling error."}}
                logging.warning("Exception handled! Data is empty JSON, "
                                "AttributeError. This warning will be thrown "
                                "if some beacon is not working and don't "
                                "return any answer or if the beacon is "
                                "impossible to reach. Probably above this log "
                                "will be another about it.\n"
                                "Also, json_load is filled with a dictionary "
                                "with information about this error.")

            # This exception also can try to find some text on the error
            # page to give a reason.
            except json.decoder.JSONDecodeError:
                error_this_lap = 1
                json_load = web_parser(json_tmp)
                logging.warning("Exception handled! Unexpected beacon "
                                "response from %s, JSONDecodeError.\n "
                                "Information about this error may be "
                                "parsed as a JSON result.",
                                beacon)

            # Add one to the error count in case there is any error, just
            # to get a control about them.
            errors_count += error_this_lap

            result_json[beacon] = json_load
            logging.debug("Result writed into result_json.")

        logging.info("Loop ended with %i errors from %i beacons.",
                     errors_count, len(known_beacons))

        return result_json

    def web_parser(content):
        """Try to take information from the error.
        Try to take the title and content of the error response from a
        Beacon. If there is nothing recogniseable, the error will be
        unknown. If the function recognise something wrong like a full <p>
        tag with a lot of information, it will limit the output saved on
        the json by the specified integer. This function is considered
        complete, but maybe this can be improved.

        :param content: It takes a binary object with the content of a
                        webpage requested with the module requests.
        :type_info content: binary
        :return: Returns a dictionary with the content it can parse (<h1>
                 and <p>). If it can't find title and content, it will
                 return a generic error message.
        :rtype_info: dictionary
        """
        max_length_parsed = 500 #This can be changed in case you need it.
        json_load = None

        web_content = str(content.content).replace("\\n", " ")
        web_content = web_content[:max_length_parsed]
        logging.debug("Web content taken, newlines were removed and "
                      "total string size was limited to %i characters",
                      max_length_parsed)

        #This will parse a posible result from a not working beacon.
        if "<h1>" and "</h1>" and "<p>" and "</p>" in web_content:
            title_error = web_content[web_content.find("<h1>")+4 \
                        : web_content.find("</h1>")]
            parag_error = web_content[web_content.find("<p>")+3 \
                        : web_content.find("</p>")]
            json_load = {"error" : {"title" : title_error, \
                        "content" : parag_error}}
            logging.debug("Parsed titles and paragraphs saved into "
                          "json_load.")
        else:
            json_load = {"error" : {"title" : "Unknown Error", \
                        "content" : "Error not recognised."}}
            logging.debug("Parseable content not found, json_load filled "
                          "with unknown error data.")

        return json_load

    return capturer_get_sequence()

#======================================================================#

# GET for networks endpoint
def endpoint_networks_get():
    """Make a dictionary with the content of network info in params
    This imple function takes the data on params.conf refeering to the
    networksInfo and adds it in a dictionary.

    :return: current network info
    :rtype: dictionary
    """

    logging.debug("Filling dictionary with params.conf data, section "
                  "networkInfo")
    networks_dict = lib.config.read_external_configuration("networkInfo")

    return networks_dict

# GET for service_info endpoint
def endpoint_service_info_get():
    """Simple function to take the serviceInfoGA4GH data from params
    Uses the read_external_configuration function to read the data of
    the service GA4GH from params.conf file. This function works but
    it's too simple and probably will need improvements.

    :return: service info GA4GH
    :rtype: dictionary
    """
    logging.debug("Filling dictionary with params.conf data, section "
                  "serviceInfoGA4GH")
    service_info_dict = lib.config.read_external_configuration(
        "serviceInfoGA4GH")

    return service_info_dict

# GET for service_info endpoint
def endpoint_service_types_get():
    """Simple function that will take the serviceTypes on the params
    Uses the read_external_configuration function to read the list (or
    tuple) of the params.conf file related to the types of service
    known. Probably we will only have three known types, registry,
    beacon and beacon aggregator. This function it's working but
    probably will be improved.

    :return: known serviceTypes
    :rtype: dictionary
    """
    logging.debug("Filling dictionary with params.conf data, section "
                  "serviceTypes")
    service_types_dict = lib.config.read_external_configuration(
        "serviceTypes")

    logging.debug("Spliting taken results into a list")
    service_types_list = service_types_dict["types"].split(" ")

    logging.debug("Returning dictionary with serviceTypes")
    return {"serviceTypes" : service_types_list}

# GET for info endpoint
def endpoint_info_get():
    """Take and check the service info data from the params.conf file.
    This function will read the serviceInfo data from the params.conf
    file and check if the mandatory data is correct. Principally, every
    camp is a string, except for the ones that are booleans, these ones
    have to ve checked. This function is working but can be improved.

    :return: Return a dictionary with all the parsed data from the
             configuration file.
    :rtype_info: dictionary
    """
    logging.debug("Filling dictionary with params.conf data, section "
                  "serviceInfo")
    info_dict = lib.config.read_external_configuration("serviceInfo")

    logging.debug("Checking sintax of boolean 'entrypoint'")
    if info_dict["entrypoint"][0].lower() == "t":
        info_dict["entrypoint"] = True
    else:
        info_dict["entrypoint"] = False

    logging.debug("Checking sintax of boolean 'open'")
    if info_dict["open"][0].lower() == "t":
        info_dict["open"] = True
    else:
        info_dict["open"] = False

    logging.debug("Returning dictionary filled with params.conf data")
    return info_dict

#---------------------------PUT Endpoints------------------------------#


#-------------------------General Functions----------------------------#

def get_client_ip():
    """Function to take client IP
    This function takes the client IP and return it as string. It's
    fully working and by it's simplicity probably don't need future
    tweaks.

    :return: the IP of the client who made the query, if there is no IP
             recognised, it will be considered "localhost"
    :rtype: string
    """
    logging.debug("Trying to get the client IP")

    #Important to try to take the clien IP, because when flask initialize,
    #apparently test every function. When Flask tests a function with
    #request.remote_addr, this will not have any IP and cause an exception.
    try:
        client_ip = request.remote_addr
        logging.debug("Client IP: %s", client_ip)

    except RuntimeError:
        logging.debug("Silent exception handled! RuntimeError, "
                      "probably was Flask initializing.")
        client_ip = "localhost"

    logging.debug("Returning client_ip")
    return client_ip



if __name__ == "__main__":
    pass
else:
    logging.debug("Current: %s", __name__)
