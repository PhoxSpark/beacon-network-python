from flask import Blueprint
from flask import render_template
from flask import request
import requests

QUERY = Blueprint('query', __name__, template_folder='../../static')

@QUERY.route('/query', methods=["GET"])
def index():
    result = str()
    req = requests.get("ba1.bn.com:5004" + request.full_path)
    print(req.json())
    return result
