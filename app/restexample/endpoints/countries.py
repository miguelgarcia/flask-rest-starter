from flask import request
from flask_restful import Resource

from app.utils.validateschema import (qsargs, output,
                                      inputbody)
from app.errors import NotFoundException

from ..schemas import CountrySchema, ListArgsSchema


class Country:
    def __init__(self, code='', name=''):
        self.code = code
        self.name = name


countries_list = [Country('AR', 'Argentina'), Country('BR', 'Brazil')]


class CountriesList(Resource):
    @output(CountrySchema, many=True)
    @qsargs(ListArgsSchema)
    def get(self, args_cleaned):
        limit = args_cleaned.get('limit')
        offset = args_cleaned.get('offset')

        countries = countries_list[offset:offset+limit]

        return countries, 200, {'x-next': request.base_url + "?offset=%d&limit=%d" % (offset+limit, limit)}

    @inputbody(CountrySchema)
    def post(self, data):
        country = Country()
        CountrySchema.toObject(data, country)
        countries_list.append(country)
        return None, 201


class CountryEntity(Resource):
    @output(CountrySchema)
    def get(self, code):
        match = list(filter(lambda c: c.code == code, countries_list))
        if len(match) == 0:
            raise NotFoundException()
        return match[0], 200

    @inputbody(CountrySchema)
    def put(self, code, data):
        match = list(filter(lambda c: c.code == code, countries_list))
        if len(match) == 0:
            raise NotFoundException()
        CountrySchema.toObject(data, match[0])
        return None, 204

    def delete(self, code):
        match = list(filter(lambda c: c.code == code, countries_list))
        if len(match) == 0:
            raise NotFoundException()
        #countries_list.remove(match[0])
        return None, 204
