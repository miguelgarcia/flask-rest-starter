# flask-rest-starter

[![CircleCI](https://circleci.com/gh/miguelgarcia/flask-rest-starter.svg?style=svg)](https://circleci.com/gh/miguelgarcia/flask-rest-starter)

Base project to build REST APIs using Flask + Flask-RESTful + marshmallow

# Install deps

    pip install -r requirements.txt
    
# Run

    python manage.py runserver
    
# Examples at /app/restexample

 * `schemas.py` defines input and output schemas used on the API
 * `endpoints/*.py` shows how to implement different REST API endpoints
 * `__init__.py` maps endpoints to url paths
 
 This project groups endpoints into blueprints. If you create a new blueprint, register it in `app/__init__.py`

## Example schema

    class ListArgsSchema(Schema):
        limit = fields.Integer(required=False, validate=[
                               validate.Range(1, 100)], missing=100)
        offset = fields.Integer(required=False, validate=[
                                validate.Range(0)], missing=0)


    class CountrySchema(Schema):
        code = fields.String(required=True, validate=[validate.Length(max=255)])
        name = fields.String(required=True, validate=[validate.Length(max=255)])



## Example endpoints

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
            
Note the decorators `@output`, `@qsargs` and `@inputbody`:

 * `@qsargs`: validate query string parameters using a marshmallow Schema.
 * `@inputbody`: validate the request body using a marshmallow Schema.
 * `@output`: transforms the method output a marshmallow Schema.
