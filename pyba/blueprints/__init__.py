"""
Module container of all the Flask RestPLUS endpoints.
This module is a container for all the blueprints that Flask will use
to load every available endpoint.

If you want to add a new blueprint and it's on this module (blueprints),
import it and add it in the __all__ variable. After that, you just have
to add a line on the api.py file.
"""

from pyba.blueprints import info_root as i,\
                            networks as n,\
                            parser as p,\
                            registered_beacons as rb,\
                            registries as r,\
                            service_info as si,\
                            service_types as st,\
                            services as s

__all__ = ["i", "n", "p", "rb", "r", "si", "st", "s"]
