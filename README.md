# flask-rest-starter

[![CircleCI](https://circleci.com/gh/miguelgarcia/flask-rest-starter.svg?style=svg)](https://circleci.com/gh/miguelgarcia/flask-rest-starter)

Base project to build REST APIs using Flask + Flask-RESTful + marshmallow. 

This project contains the components needed to develop, test and deploy as docker image REST APIs with Flask. An example API, a countries CRUD, is included.

# Local development environment

    python3 -m venv venv
    . ./venv/bin/activate
    pip install -r requirements.txt
    
## Run

    python manage.py runserver
    
## Run tests

    python manage.py test
    
# Build Docker image and run

    docker -t myimage .
    docker run 5000:80 myimage
    
After that, go and check http://localhost:5000/restexample/countries
    
# Examples in /app/restexample

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

 * `@qsargs`: validates query string parameters using a marshmallow schema.
 * `@inputbody`: validates the request body using a marshmallow schema.
 * `@output`: transforms the method output using a marshmallow schema.
