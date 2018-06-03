from flask import Blueprint
from flask_restful import Api

from .endpoints.countries import CountriesList, CountryEntity

blueprint = Blueprint('restexample', __name__)

rest = Api(blueprint)

rest.add_resource(CountriesList, '/countries/')
rest.add_resource(CountryEntity, '/countries/<string:code>')