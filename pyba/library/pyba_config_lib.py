"""Contains all the config related functions
This module have all the functions with something related to the config
files. To edit them or read them, this module has to be able to perform
a lot of the common and specific actions with config files.
"""

from __future__ import absolute_import
import logging
import json
import configparser

from pyba import API_VERSION, APP_VERSION



CONFIG = configparser.ConfigParser()



def parse_from_config(dictionary_string):
    """This function will parse dictionaries and lists
    This function will be able to take a dictionary or a list of
    dictionaries from a string. It will parse the information inside
    into a JSON object, with that, the json library will transform the
    string into a dictionary, being able to fill another dictionary
    with the information parsed by the json library. It's able to parse
    data from lists only too.

    :param string: A dictionary, list of dictionaries or a single list
    :type string: string
    :return: A list of dictionaries, even if it's only one it will
             be a list
    :rtype: list
    """

    logging.debug("Initializating dictionary to save the results")
    list_parsed = list()

    #Remove double quotes if exists from config
    logging.debug("Checking if there is double quotes on the string")
    if dictionary_string.startswith('"') and dictionary_string.endswith('"'):
        logging.debug("Removing double quotes")
        dictionary_string = dictionary_string[1:-1]

    #Remove single quotes if exists from config
    logging.debug("Checking if there is single quotes on the string")
    if dictionary_string.startswith("'") and dictionary_string.endswith("'"):
        logging.debug("Removing single quotes")
        dictionary_string = dictionary_string[1:-1]

    #Check if the string introduced it's a dictionary to add it like that
    #and not like a string.
    logging.debug("Checking if string %s is a dictionary",
                  dictionary_string)
    if dictionary_string.startswith("{"):
        logging.debug("String is a dictionary, inserting it into a "
                      "list...")
        dictionary_string = "[" + dictionary_string + "]"

    #JSONIFYING data to convert strings into dictionaries and lists
    logging.debug("JSONyfing string:\n%s", dictionary_string)
    jdata = json.loads(dictionary_string)

    #Append the list of parsed data from json data.
    logging.debug("Iterating trough JSON data")
    for data in jdata:
        list_parsed.append(data)

    logging.debug("Returning dictionary")
    return list_parsed


def read_external_configuration(section, file="params.conf",
                                path_file="pyba/config/"):
    """Request dictionary from sections on configuration files
    This function will go to the specified configuration file and put
    the specified section into a dictionary. It should work with any
    configuration file.

    :param section: Section of the config file to parse.
    :type section: string
    :param file: File to parse, defaults to "configuration.ini"
    :type file: str, optional
    :param path_file: Location of the file to parse, defaults to
                      "pyba/config/"
    :type path_file: str, optional
    :return: Dictionary with all the section parsed.
    :rtype: dictionary
    """

    logging.debug("Initializing dictionary_return as an empty "
                  "dictionary")
    dictionary_return = dict()

    logging.debug("Reading %s on %s", file, path_file)
    CONFIG.read(path_file + file)

    #Look to every config data, remove line breaks from data, check if
    #data starts with { or [ to determine if it's a dictionary or a list
    #and adding all into a dictionary.
    logging.debug("Iterating through all config data")
    for key in CONFIG[section]:
        logging.debug("Saving string and removing residual values")
        getted_section = CONFIG[section].get(key)\
                                        .replace("\n", "")\
                                        .replace("\n\\", "")\
                                        .replace("\\", "")

        logging.debug("Checking if string is a dictionary or a list")
        try:
            if(getted_section[1] == "{" or getted_section[1] == "["\
                                        or getted_section[0] == "{"\
                                        or getted_section[0] == "["):
                logging.info("Dictionary found on key %s, section %s! "
                             "Calling parsing string function.",
                             key, section)
                getted_section = parse_from_config(getted_section)

        except IndexError:
            logging.warning("Exception IndexError handled! The string "
                            "introduced on params.conf it's very short "
                            "(one character or less)! Nothing to worry "
                            "about, check if the value '%s' is correct, "
                            "and if it is, ignore this warning.",
                            getted_section)

        logging.debug("Saving %s from section %s on dictionary_return",
                      getted_section, section)
        dictionary_return[key] = getted_section

    logging.debug("Returning dictionary_return")
    return dictionary_return


def write_to_external_configuration(section,
                                    parameter,
                                    value=str(),
                                    file="params.conf",
                                    path_file="pyba/config/"):
    """Function to write something on a specified config file.
    This function will write a parameter onto a config file, it's
    designed to be flexible, so it can be used on every necessary
    section of service.

    :param section: Section of the config file that we want to edit,
                    marked with [] on the file.
    :type section: string
    :param parameter: Specific parameter that we want to edit on the
                      file.
    :type parameter: string or dictionary
    :param value: Value to write on the parameter. If the parameter is
                  a dictionary and actually have the values on it, this
                  value will not be necessary.
    :type value: string
    :param file: File to find all the data to modify, defaults to
                 "params.conf"
    :type file: str, optional
    :param path_file: Path of the config files to edit, default to
                      "pyba/config/"
    """

    logging.debug("Reading %s from %s", file, path_file)
    CONFIG.read(path_file + file)

    logging.debug("Writing %s on section %s, parameter %s",
                  value, section, parameter)
    CONFIG[section][parameter] = value

    logging.debug("Opening %s on write mode", file)
    with open(path_file + file, 'w') as configfile:
        logging.debug("Writing all readed config file with applied "
                      "changes")
        CONFIG.write(configfile)


def update_params(file_path="pyba/config/params.conf"):
    """Update the values mandatory by the service on the params.conf
    The values updated by this function will be specified at some point
    in the service or in another file, initialized on the __init__.py
    found on the same moudle as the __main__.py file. The user don't
    have any reason to change this, except if it's modifying the
    service, in that case it's easy to find where to change this data.

    :param file_path: Main configuration file of the service, defaults
                      to "pyba/config/params.conf"
    :type file_path: str, optional
    """

    logging.debug("Reading config file %s", file_path)
    CONFIG.read(file_path)

    logging.debug("Replacing non customizable camps")
    CONFIG["serviceInfo"]["apiVersion"] = API_VERSION
    CONFIG["serviceInfo"]["version"] = APP_VERSION

    logging.debug("Opening %s on write mode", file_path)
    with open(file_path, 'w') as configfile:
        logging.debug("Writing all readed config file with applied "
                      "changes")
        CONFIG.write(configfile)



if __name__ == "__main__":
    pass
else:
    logging.debug("Current: %s", __name__)
