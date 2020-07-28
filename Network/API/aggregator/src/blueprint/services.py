import logging as log
from flask import request
from flask import Blueprint
from configparser import ConfigParser
from ... import SERVICES_KNOWN

SERVICES = Blueprint('services', __name__)

@SERVICES.route('/services', methods=["GET", "POST"])
def services():
    services = list()
    http_code = 200
    params = {
        "ServiceType"   : request.args.get('ServiceType'),
        "listFormat"    : request.args.get('listFormat'),
        "apiVersion"    : request.args.get('apiVersion')
    }
    services, http_code = get_services(params)
    return services, http_code

@SERVICES.route('/services/<service_id>', methods=["GET", "POST", "DELETE"])
def services_id(service_id):
    response = dict()
    http_code = 200
    if request.method == 'GET':
        response, http_code = get_services_id(service_id)
    elif request.method == 'POST': #Shouldn't be there, but it's useful for debuging.
        params = {
            "name"          : request.args.get("name"),
            "ServiceType"   : request.args.get('ServiceType'),
            "serviceUrl"    : request.args.get('serviceURL')
        }
        response, http_code = post_services_id(params, service_id)
    elif request.method == 'DELETE':
        response, http_code = delete_services_id(service_id)
    
    return response, http_code

def get_services(params):
    services = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str
    abort = False

    config.read(SERVICES_KNOWN)

    for data in dict(config):
        try:
            if dict(config[data])["ServiceType"] == params["ServiceType"] \
            and params["ServiceType"] is not None:
                config.remove_section(data)
        except KeyError:
            pass
        try:
            if dict(config[data])["listFormat"] == params["listFormat"] \
            and params["listFormat"] is not None:
                config.remove_section(data)
        except KeyError:
            pass
        try:
            if dict(config[data])["apiVersion"] == params["apiVersion"] \
            and params["apiVersion"] is not None:
                config.remove_section(data)
        except KeyError:
            pass

    tmp_services = dict(config)
    for data in tmp_services:
        if data != "DEFAULT":
            services[data] = dict(tmp_services[data])

    return services, http_code

def get_services_id(service_id):
    services = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str
    abort = False

    config.read(SERVICES_KNOWN)

    if service_id not in dict(config):
        log.error("ID Not found.")
        http_code = 400
        abort = True
        services = {"error":"ID not found."}

    if not abort:
        for data in dict(config):
            if data == service_id:
                services = dict(config[data])

    return services, http_code

def delete_services_id(service_id):
    services = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str
    abort = False

    config.read(SERVICES_KNOWN)

    if service_id not in dict(config):
        log.error("ID Not found.")
        http_code = 400
        abort = True
        services = {"error":"ID not found."}

    if not abort:
        config.remove_section(service_id)
        config.write(open(SERVICES_KNOWN, "w"))
        services = {"success":"Operation successful."}

    return services, http_code

def post_services_id(params, service_id):
    services = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str
    abort = False

    config.read(SERVICES_KNOWN)

    if service_id in dict(config):
        log.error("The ID alredy exists!")
        abort = True
        http_code = 400
        services = {"error":"ID alredy exists."}

    if not abort:
        try:
            config.add_section(service_id)
            config.set(service_id, "name", params["name"])
            config.set(service_id, "ServiceType", params["ServiceType"])
            config.set(service_id, "serviceURL", params["serviceUrl"])
            config.write(open(SERVICES_KNOWN, "w"))
            services = {"success":"Operation successful."}
        except KeyError as error:
            log.error("Missing necessary params. Additional information: %s", error)
            services = {"error":"Missing necessary params. Additional information: %s" % error}
            http_code = 400

    return services, http_code