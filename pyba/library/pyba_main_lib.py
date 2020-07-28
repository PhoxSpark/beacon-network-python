"""General functions module
This module contains all the general pourpose functions, but mostly,
the initialization and main functions.
"""

from __future__ import absolute_import

import os
import logging
import argparse
import shutil

from pyba import APP
from pyba import HANDLER
from pyba import LOGGROOT
from pyba import LOGGLIB
from pyba import LOGGFLASK
from pyba import EXECUTION_TIME



def parse_args():
    """Take the arguments on the console.
    Function to establish the options selecteable by the user on the
    console. As argparse have a lot of pre configured goodies, the
    function is quite simple.

    :return: Return a dictionary with the flag name (the same as the
             option without hyphen) and the value inputed (if it's
             necessary as boolean flags will not require input).
    :rtype: dictionarty
    """

    parser = argparse.ArgumentParser(description='Arguments to start '
                                                 'the service.')

    #Debug flag:
    parser.add_argument('--debug',
                        '-d',
                        action='store_true',
                        help='Choose if the debug mode will be enabled '
                             'or disabled. This will add some more '
                             'loggs on the service console, error '
                             'tracing and app refresh when the code is '
                             'changed.')

    #Flask output flag:
    parser.add_argument('--enable-flask-output',
                        '-f',
                        action='store_true',
                        default=False,
                        help="Flask output is disabled by default. "
                             "To see urllib and flask console "
                             "messages, use this flag. Requires debug "
                             "mode! Without it, the loggs will not "
                             "show because those loggs are low "
                             "severity.")

    #External logs flag:
    parser.add_argument('--external-logs',
                        '-e',
                        action='store_true',
                        help='Save all the logs on a .log file.')

    #Clean logs flag:
    parser.add_argument('--clean-logs',
                        '-C',
                        action='store_true',
                        help='Clean all the logs on the logs folder if '
                             'exists before creating the new one.')

    return vars(parser.parse_args())


def logs_initialization(options):
    """Initialize the Logging configurations with the options obtained
    The options will be obtained from the arguments parsed, depending
    on these options will configure loggs in one way or another. This
    function can't have too many logs for obvious reasons! Until the
    logging module isn't configured, there's no logs.

    :param options: obtained from the parsed arguments
    :type options: dictionary
    """

    ## Initialization of loggs format depending on specified flags
    # Set the format of HANDLER depending on the specified flags

    # If debug mode is specified, the loggs will show more information.
    if options["debug"]:
        HANDLER.setFormatter(logging.Formatter('[%(levelname)s] '
                                               '%(filename)s.'
                                               '%(funcName)s(), '
                                               'line: %(lineno)s\n'
                                               '%(message)s\n'))
    else:
        HANDLER.setFormatter(logging.Formatter('[%(levelname)s]: '
                                               '%(message)s'))

    # If external logs were specified, it's mandatory to have a logs
    # folder. Note: Because of the way Flask Debug Mode is maded, when
    # specified to externalize logs it will execute two times creating
    # two log files with miliseconds of difference. This is normal and
    # can be ignored.
    if options["clean_logs"]:
        try:
            shutil.rmtree("./pyba/logs")
        except OSError:
            logging.error("Exception handled! Failed to remove "
                          "./pyba/logs directory, OSError")

    if options["external_logs"]:
        error = False
        if not os.path.exists("./pyba/logs"):
            #This will try to create the folder for the logs.
            try:
                os.mkdir("./pyba/logs")
            except OSError:
                error = True
                logging.error("Exception handled! Failed to make "
                              "./pyba/logs directory, OSError")
        if not error:
            #Adding handlers for external logs.
            exthand = logging.FileHandler("./pyba/logs/%s.log"
                                          % EXECUTION_TIME)
            exthand.format = HANDLER.format
            LOGGROOT.addHandler(exthand)

    #Setting logg levels depending on flags
    if options["debug"]:
        if not options["enable_flask_output"]:
            LOGGROOT.setLevel(logging.DEBUG)
            LOGGLIB.setLevel(logging.ERROR)
            LOGGFLASK.setLevel(logging.ERROR)
            APP.logger.disabled = True
        else:
            LOGGROOT.setLevel(logging.DEBUG)
            LOGGLIB.setLevel(logging.ERROR)
            LOGGFLASK.setLevel(logging.DEBUG)
            APP.logger.disabled = False
    else:
        LOGGROOT.setLevel(logging.INFO)
        LOGGLIB.setLevel(logging.ERROR)
        LOGGFLASK.setLevel(logging.ERROR)
        APP.logger.disabled = True
        logging.info("Logging messages started")



if __name__ == "__main__":
    pass
else:
    logging.debug("Current: %s", __name__)
