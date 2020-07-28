"""__main__ file for start services.
Module __main__ that will start when the full package is called. Just
calling the package from Python will start this script.
"""

from __future__ import absolute_import

import logging

import pyba.library as lib
from pyba import api
# REMEMBER TO UPDATE THE VERSION ON EACH COMMIT!!!



def main():
    """Main function for starting
    This function will execute when the package is called by Python, it
    will take the arguments specified if theres one, apply them and
    start Flask service.
    """
    options = lib.main.parse_args()

    #Initialize all the loggings with the options specified.
    lib.main.logs_initialization(options)
    logging.debug("Logs are now enabled and working")

    #Update the main config file with the app information.
    logging.debug("Updating parameters on config files")
    lib.config.update_params()

    # Finally, when all the initialization schedule is completed, Flask
    # will start.
    logging.debug("Calling Flask initializator function")
    api.start(options["debug"])



if __name__ == "__main__":
    main()
