import logging as log
from .. import APP
from .blueprint.index import INDEX
from .blueprint.query import QUERY

def start():
    log.debug("Adding blueprints.")
    APP.register_blueprint(INDEX)
    APP.register_blueprint(QUERY)

    log.debug("Starting API.")
    APP.run(debug=True, port=5000, host='0.0.0.0')
