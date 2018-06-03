import unittest
from app.tests.base import BaseTestCase
from flask import json

class TestCountries(BaseTestCase):
    def test_1_list(self):
        """ Test currencies listing """
        with self.client:
            response = self.client.get('/restexample/countries/',
                                       content_type='application/json')
            self.assert200(response)
            expect = [dict(code='AR', name='Argentina'), dict(code='BR', name='Brazil')]
            self.assertListEqual(expect, json.loads(response.data.decode()))

    def test_2_list_limit_offset(self):
        """ Test countries listing with limit and offset params """
        with self.client:
            response = self.client.get('/restexample/countries/?offset=1&limit=3',
                                       content_type='application/json')
            self.assert200(response)
            expect = [dict(code='BR', name='Brazil')]
            self.assertListEqual(expect, json.loads(response.data.decode()))

    def test_3_create(self):
        """ Test create country """
        data = """ {
          "code": "%s",
          "name": "%s" }
        """ % ('UY', 'Uruguay')
        with self.client:
            response = self.client.post('/restexample/countries/',
                                        data=data,
                                        content_type='application/json')
            self.assertStatus(response, 201)