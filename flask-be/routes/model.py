from flask import jsonify
from flask import Blueprint
from controllers.model import *

model_bp = Blueprint("model_bp", __name__, url_prefix="/model")


@model_bp.route('/hello')
def hello():
    return 'Hello World!'
