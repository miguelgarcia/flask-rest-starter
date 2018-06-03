from flask import Blueprint
from flask_restful import Api

from .endpoints.countries import CountriesList

blueprint = Blueprint('restexample', __name__)

rest = Api(blueprint)

rest.add_resource(CountriesList, '/countries/')