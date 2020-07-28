from configparser import ConfigParser
from flask import Blueprint
import requests
import logging as log

from .info import get_aggregator_info
from ... import AGGREGATOR_CONFIG_FILE
from ... import SERVICES_KNOWN

REGISTERED_BEACONS = Blueprint('registered_beacons', __name__)

@REGISTERED_BEACONS.route('/registered_beacons', methods=["PUT"])
def registered_beacons():
    http_code = 200
    services = list()
    response = dict()
    services, http_code = ask_known_registries()
    if http_code == 200:
        self_information = get_aggregator_info(AGGREGATOR_CONFIG_FILE)
        response, http_code = build_known_services(services, str(self_information[0]["id"]))
    return response, http_code

def ask_known_registries():
    registries = list()
    networks = dict()
    services = dict()
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str
    http_code = 503

    config.read(SERVICES_KNOWN)

    for data in dict(config):
        try:
            if dict(config[data])["ServiceType"] == "GA4GHRegistry" \
            and data != "DEFAULT":
                registries.append(dict(config[data])["serviceURL"])
                http_code = 200
        except KeyError:
            pass

    for registry in registries:
        log.debug(registry)
        try:
            req1 = requests.get(registry + "/info")

            if req1.status_code == 200:
                req2 = requests.get(registry + "/networks")
                networks = req2.json()
        except requests.exceptions.ConnectionError:
            log.warning("Service %s unavailable.", registry)

    for network in networks:
        services[network] = networks[network]

    return services, http_code

def build_known_services(services, self_id):
    response = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str

    config.read(SERVICES_KNOWN)

    for network in services:
        for service in services[network]["services"]:
            try:
                req_id = requests.get(service["serviceURL"] + "/info")
                if req_id.json()["id"] != self_id:
                    config.add_section(req_id.json()["id"])
                    config.set(req_id.json()["id"], "ServiceType", service["ServiceType"])
                    config.set(req_id.json()["id"], "name", service["name"])
                    config.set(req_id.json()["id"], "serviceURL", service["serviceURL"])
            except requests.exceptions.ConnectionError:
                log.warning("The service %s from the registry didn't respond. It won't be added.", service["serviceURL"])
    with open(SERVICES_KNOWN, "w") as file:
        config.write(file)
    response = {"success" : "Operation successful."}    
    return response, http_code
