from flask import Blueprint
from flask import render_template

INDEX = Blueprint('index', __name__, template_folder='../../static')

@INDEX.route('/', methods=["GET"])
@INDEX.route('/index', methods=["GET"])
def index():
    result = None
    result = render_template("index.html")
    return result
