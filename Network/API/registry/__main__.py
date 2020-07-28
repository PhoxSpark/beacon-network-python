"""__main__ module, gateway of the service.
"""
import logging as log
from .src import start_api

def init():
    """"Gateway" of the app
    It will call the necessary function to start the service.
    """
    log.debug("Initializing API...")
    start_api.start()

if __name__ == "__main__":
    init()
