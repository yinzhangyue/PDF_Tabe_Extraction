from flask import jsonify
from flask import Blueprint
from controllers.auth import *


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route('/hello')
def hello():
    return 'Hello World!'


@auth_bp.route('/login', methods=['GET'])
def login():
    return jsonify({
        'contribution': 123,
        'total_count': 123456
    })


@auth_bp.route('/register', methods=['GET'])
def register():
    return jsonify({
        'contribution': 123,
        'total_count': 123456
    })