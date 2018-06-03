import os

from flask import Flask, jsonify
from flask_cors import CORS
from .utils.validateschema import SchemaViolationException

import logging

logger = logging.getLogger(__name__)

# Inititalize APP
app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)

app.config.from_object(app_settings)

# Load blueprints


def register_blueprints(app):
    from app.restexample import blueprint as restexample_api
    app.register_blueprint(restexample_api, url_prefix='/restexample')


register_blueprints(app)


@app.errorhandler(SchemaViolationException)
def schema_exception_error_handler(error):
    logger.error(error)
    return jsonify(dict(
        status_code=error.status_code,
        error=error.error
    )), error.status_code


@app.route('/api/help', methods=['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)