"""Query endpoint
"""

from flask import request
from flask import Blueprint

from ..model.query_model import QueryModel

QUERY = Blueprint('query', __name__)

@QUERY.route('/query', methods=["GET", "POST"])
def query():
    """Query to the beacon
    Accept GET and POST methods, they will do the same.

    :return: JSON object and HTTP code.
    :rtype: dict(), int()
    """
    params = {
        "referenceName"           : request.args.get('referenceName'),
        "start"                   : request.args.get('start'),
        "startMin"                : request.args.get('startMin'),
        "startMax"                : request.args.get('startMax'),
        "end"                     : request.args.get('end'),
        "endMin"                  : request.args.get('endMin'),
        "endMax"                  : request.args.get('endMax'),
        "referenceBases"          : request.args.get('referenceBases'),
        "alternateBases"          : request.args.get('alternateBases'),
        "variantType"             : request.args.get('variantType'),
        "assemblyId"              : request.args.get('assemblyId'),
        "mateName"                : request.args.get('mateName'),
        "datasetIds"              : request.args.get('datasetIds'),
        "includeDatasetResponses" : request.args.get('includeDatasetResponses')
    }
    query_object = QueryModel(params)

    return query_object.response, query_object.http_code
