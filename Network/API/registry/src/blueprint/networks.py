"""Networks blueprint
"""
import logging as log
from configparser import ConfigParser
from flask import request
from flask import Blueprint

from ... import NETWORKS_CONFIG_FILE
from ... import SERVICES_CONFIG_FILE

NETWORKS = Blueprint('networks', __name__)

@NETWORKS.route('/networks', methods=["GET", "POST"])
def networks():
    """Show or add networks

    :return: dictionary with the response
    :rtype: dict()
    """
    result = dict()
    http_code = int()
    path = str()
    params = dict()

    if request.method == "GET":
        result, http_code = get_network(
            NETWORKS_CONFIG_FILE,
            SERVICES_CONFIG_FILE
        )

    elif request.method == "POST":
        path = request.path
        print(path)
        params = {
            "id"            : request.args.get('id'),
            "name"          : request.args.get('name'),
            "description"   : request.args.get('description'),
            "organization"  : request.args.get('organization')
        }
        result, http_code = post_network(
            params,
            NETWORKS_CONFIG_FILE
        )

    return result, http_code

@NETWORKS.route('/networks/<net_id>/services', methods=["POST"])
def networks_services(net_id):
    """Post new service on the network
    Add a new service from the network to this registry.

    :param net_id: ID of the network, it needs to exist on the registry.
    :type net_id: str()
    :return: dictionary with the response
    :rtype: dict()
    """
    result = dict()
    http_code = int()

    params = {
        "id"            : request.args.get('id'),
        "name"          : request.args.get('name'),
        "serviceURL"    : request.args.get('serviceURL'),
        "ServiceType"   : request.args.get('ServiceType'),
        "open"          : request.args.get('open'),
        "entryPoint"    : request.args.get('entryPoint')
    }
    result, http_code = post_network_service(
        net_id,
        params,
        SERVICES_CONFIG_FILE
    )

    return result, http_code

def get_network(networks_file, services_file):
    """Parse from configuration the network info

    :param networks_file: file where the network info is found
    :type networks_file: str()
    :param services_file: file where the services info is found
    :type services_file: str()
    :return: dictionary with the network data
    :rtype: dict()
    """
    network = dict()
    http_code = 200
    config_net = ConfigParser(delimiters=('=', ':'))
    config_net.optionxform = str
    config_serv = ConfigParser(delimiters=('=', ':'))
    config_serv.optionxform = str

    config_net.read(networks_file)
    config_serv.read(services_file)

    for net in dict(config_net):
        if net != "DEFAULT":
            network[net] = dict(config_net[net])
            network[net]["services"] = list()
            for serv in dict(config_serv):
                try:
                    dict_config_serv = dict(config_serv[serv])
                    if dict_config_serv["network"] == str(net):
                        network[net]["services"].append(dict(config_serv[serv]))
                except KeyError:
                    pass

    return network, http_code

def post_network(params, networks_file):
    """Add a network to the registry

    :param params: parameters dictionary
    :type params: dict()
    :param networks_file: file where the network information is stored
    :type networks_file: string
    :return: network information
    :rtype: dict()
    """
    network = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str
    abort = False

    config.read(networks_file)

    if params["id"] in dict(config):
        log.error("The ID alredy exists! This can cause a problem on \
the whole network so it won't be added.")
        abort = True
        http_code = 400
        network = {"error":"ID alredy exists."}

    if not abort:
        try:
            config.add_section(params["id"])
            config.set(params["id"], "name", params["name"])
            config.set(params["id"], "description", params["description"])
            config.set(params["id"], "organization", params["organization"])
            config.write(open(networks_file, "w"))
            network = {"success":"Operation successful."}
        except KeyError as error:
            log.error("Missing necessary params. Additional information: %s", error)
            network = {"error":"Missing necessary params. Additional information: %s" % error}
            http_code = 400

    return network, http_code

def post_network_service(net_id, params, services_file):
    """Add a new service to a network

    :param net_id: identification of the network
    :type net_id: str()
    :param params: dictionary of params
    :type params: dict()
    :param services_file: file where the services are stored
    :type services_file: str()
    :return: network dictionary with all the data
    :rtype: dict()
    """
    network = dict()
    http_code = 200
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str
    abort = False

    config.read(services_file)

    if params["id"] in dict(config):
        log.error("The ID alredy exists! This can cause a problem on \
the whole network so it won't be added.")
        abort = True
        http_code = 400
        network = {"error":"ID alredy exists."}

    if not abort:
        try:
            config.add_section(params["id"])
            config.set(params["id"], "name", params["name"])
            config.set(params["id"], "serviceURL", params["serviceURL"])
            config.set(params["id"], "ServiceType", params["ServiceType"])
            config.set(params["id"], "open", params["open"])
            config.set(params["id"], "entryPoint", params["entryPoint"])
            config.set(params["id"], "network", net_id)
            config.write(open(services_file, "w"))
            network = {"success":"Operation successful."}
        except KeyError as error:
            log.error("Missing necessary params. Additional information: %s", error)
            network = {"error":"Missing necessary params. Additional information: %s" % error}
            http_code = 400

    return network, http_code
