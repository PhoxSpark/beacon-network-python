"""Initialize the API
Example command with flags to build configuration file:
python -m registry
    -c
    -i "org.inb.beacon"
    -n "inbBeacon"
    -u "http://example.org/"
    -d "Testing Beacon implemented in Python."
    -a "http://example.org/main"
    -o "True"
    -O "inbelixir"
    -N "INB-ELIXIR"
    -D "Instituto nacional de Bioinformática."
    -A "Carrer de Jordi Girona, 29, 31, 08034 Barcelona."
    -U "https://inb-elixir.es"
    -C "inb.hub@bsc.es"
    -L "https://inb-elixir.es/sites/default/files/inbelixir.png"
"""
import logging as log
import argparse
import os
from configparser import ConfigParser
from datetime import datetime
from .. import API
from .. import BEACON_CONFIG_FILE
from .. import API_VERSION
from .. import VERSION
from .. import SERVICE_TYPE
from .. import EXECUTION_DATE
from .blueprint.info    import INFO
from .blueprint.query   import QUERY

def start(debug=True):
    """Initialize the API
    It will preload the API and start it when everything is ready.

    :param debug: set if debug mode is enabled at start, defaults to True
    :type debug: bool, optional
    """
    args = parse_arguments()
    abort = build_config_file(args)

    if not os.path.isfile(BEACON_CONFIG_FILE):
        abort = True
        log.error("No configuration file, can't start the API.")

    if not abort:
        debug = args.debug
        port = args.port

        log.debug("Adding blueprints.")
        API.register_blueprint(INFO)
        API.register_blueprint(QUERY)

        log.debug("Starting API.")
        API.run(debug=debug, port=port, host='0.0.0.0')

def parse_arguments():
    """Parse arguments from command line.

    :return: arguments from argparse
    :rtype: argparse object
    """
    parser = argparse.ArgumentParser(
        description='Beacon to inform BeaconAggregators ' + \
        'about the available services.'
    )

    def flags_parser(parser):
        """Read the general flags

        :param parser: argparse object
        :type parser: argparse object
        :return: argparse object
        :rtype: argparse object
        """
        parser.add_argument(
            '-p',
            '--port',
            type=int,
            default=5000,
            help="Specify the port to use for the service. " + \
            "Defaults to 5000 for the beacon."
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            default=False,
            help="Enable or disable the debug mode."
        )
        return parser
    def service_build(parser):
        """Read the flags related to the service configuration

        :param parser: argparse object
        :type parser: argparse object
        :return: argparse object
        :rtype: argparse object
        """
        #Configuration builder
        parser.add_argument(
            '-c',
            '--build-config',
            action='store_true',
            default=False,
            help="When True it will look for arguments to build the " + \
            "configuration file. If some argument not mandatory is not " + \
            "specified it will use a default value.\n" + \
            "NOTE: THIS ACTION IS DESTRUCTIVE FOR THE OLD CONFIG FILE!"
        )
        parser.add_argument(
            '-i',
            '--id',
            default=None,
            help="Use with -c, set the ID to write in the configuration " + \
            "file. Can't repeat across the network!"
        )
        parser.add_argument(
            '-n',
            '--name',
            default="GA4GHBeacon",
            help="Use with -c, set the name for the service to write on " + \
            "the config file."
        )
        parser.add_argument(
            '-d',
            '--description',
            default="Description.",
            help="Use with -c, set the description for the service."
        )
        parser.add_argument(
            '-u',
            '-welcome-url',
            default=None,
            help="Use with -c, set the welcome URL."
        )
        parser.add_argument(
            '-a',
            '--alternative-url',
            default=None,
            help="Use with -c, set the alternative URL."
        )
        parser.add_argument(
            '-o',
            '--open',
            default=True,
            help="Use with -c, set if the service is open otside the " + \
            "network or not."
        )
        return parser
    def organization_build(parser):
        """Read the flags related to the organization

        :param parser: argparse object
        :type parser: argparse object
        :return: argparse object
        :rtype: argparse object
        """
        #Organization
        parser.add_argument(
            '-O',
            '--organization-id',
            default=None,
            help="Use with -c, it will require new arguments. Set the ID " + \
            "for the organization."
        )
        parser.add_argument(
            '-N',
            '--organization-name',
            default="Organization",
            help="Use with -O, specify the name of the organization."
        )
        parser.add_argument(
            '-D',
            '--organization-description',
            default="Description",
            help="Use with -O, specify the description for the organization."
        )
        parser.add_argument(
            '-A',
            '--organization-address',
            default="Address",
            help="Use with -O, specify the address of the organization."
        )
        parser.add_argument(
            '-U',
            '--organization-welcome-url',
            default=None,
            help="Use with -O, specify the welcome URL of the organization."
        )
        parser.add_argument(
            '-C',
            '--organization-contact',
            default=None,
            help="Use with -O, specify the contact email for the organization."
        )
        parser.add_argument(
            '-L',
            '--organization-logo',
            default=None,
            help="Use with -O, specify the logo URL for the organization."
        )

        return parser

    parser = flags_parser(parser)
    parser = service_build(parser)
    parser = organization_build(parser)
    args = parser.parse_args()

    return args

def build_config_file(args):
    """Create configuration file

    :param args: Arguments to build the configuration files.
    :type args: argparse object
    :return: information about the process
    :rtype: bool()
    """
    config = ConfigParser(delimiters=('=', ':'))
    config.optionxform = str
    abort = False

    config.add_section('beacon')
    config.add_section('organization')
    config.add_section('beaconInfo')
    config.add_section('organizationInfo')

    if args.build_config:
        ### ---------------- Beacon Config build ----------------- ###
        #Handling None types
        try:
            config.set('beacon', 'id', args.id)
        except TypeError:
            log.error("ID necessary to run the API.")
            abort = True
        try:
            config.set('beacon', 'welcomeUrl', args.u)
        except TypeError:
            log.warning("WelcomeURL not specified!")
            config.set('beacon', 'welcomeUrl', "")
        try:
            config.set('beacon', 'alternativeUrl', args.alternative_url)
        except TypeError:
            config.set('beacon', 'alternativeUrl', "")

        config.set('beacon', 'apiVersion', API_VERSION)
        config.set('beacon', 'version', VERSION)
        config.set('beacon', 'serviceType', SERVICE_TYPE)
        config.set('beacon', 'name', args.name)
        config.set('beacon', 'description', args.description)
        config.set('beacon', 'open', str(args.open))
        config.set('beacon', 'entryPoint', "False")
        config.set('beacon', 'createDateTime', datetime.today().strftime('%Y-%m-%d'))
        config.set('beacon', 'updateDateTime', EXECUTION_DATE)
        ### -------------------------------------------------------- ###
        ### -------------- Organization Config Build --------------- ###
        if args.organization_id is not None:
            log.info("Specified organization ID, now expecting necessary organization params.")
            config.set('organization', 'id', args.organization_id)
            config.set('organization', 'name', args.organization_name)
            config.set('organization', 'description', args.organization_description)
            config.set('organization', 'address', args.organization_address)

            try:
                config.set('organization', 'welcomeUrl', args.organization_welcome_url)
            except TypeError:
                config.set('organization', 'welcomeUrl', "")
            try:
                config.set('organization', 'contactUrl', args.organization_contact)
            except TypeError:
                config.set('organization', 'contactUrl', "")
            try:
                config.set('organization', 'logoUrl', args.organization_logo)
            except TypeError:
                config.set('organization', 'logoUrl', "")
        ### -------------------------------------------------------- ###
        if not abort:
            with open(BEACON_CONFIG_FILE, "w") as file:
                config.write(file)
            log.info("Configuration file created, you don't need to use the -c flag anymore.")
    return abort

if __name__ == "__main__":
    pass
