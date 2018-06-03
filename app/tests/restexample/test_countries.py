import unittest
from app.tests.base import BaseTestCase
from flask import json

class TestCountries(BaseTestCase):
    def test_1_list(self):
        """ Test countries listing """
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


    def test_4_get_one(self):
        """ Test get one existing country """
        with self.client:
            response = self.client.get('/restexample/countries/AR')
            self.assert200(response)
            expect = dict(code='AR', name='Argentina')
            self.assertDictEqual(expect, json.loads(response.data.decode()))

    def test_5_get_one_404(self):
        """ Test get one non existing country """
        with self.client:
            response = self.client.get('/restexample/countries/XXX')
            self.assert404(response)
            expect = dict(message="Not found",
                          code="NOT_FOUND")
            self.assertDictEqual(expect, json.loads(response.data.decode()))

    def test_6_update_one(self):
        """ Test update existing country """
        data = """ {
          "code": "XXX",
          "name": "NAME"
          }
        """
        with self.client:
            response = self.client.put('/restexample/countries/BR',
                                       data=data,
                                       content_type='application/json')
            self.assertStatus(response, 204)
            response = self.client.get('/restexample/countries/XXX')
            self.assert200(response)
            self.assertDictEqual(json.loads(data), json.loads(response.data.decode()))

    def test_7_update_one_404(self):
        """ Test update non existing country """
        data = """ {
          "code": "XXX",
          "name": "NAME"
          }
        """
        with self.client:
            response = self.client.put('/restexample/countries/ZZZ',
                                       data=data,
                                       content_type='application/json')
            self.assert404(response)
            expect = dict(message="Not found",
                          code="NOT_FOUND")
            self.assertDictEqual(expect, json.loads(response.data.decode()))

    def test_8_delete_one(self):
        """ Test delete one country """
        with self.client:
            response = self.client.get('/restexample/countries/AR')
            self.assert200(response)
            response = self.client.delete('/restexample/countries/AR')
            self.assertStatus(response, 204)
            response = self.client.get('/restexample/countries/AR')
            self.assert404(response)
            expect = dict(message="Not found",
                          code="NOT_FOUND")
            self.assertDictEqual(expect, json.loads(response.data.decode()))

    def test_9_delete_404(self):
        """ Test delete non existing country """
        with self.client:
            response = self.client.delete('/restexample/countries/ZZZ')
            self.assert404(response)
            expect = dict(message="Not found",
                          code="NOT_FOUND")
            self.assertDictEqual(expect, json.loads(response.data.decode()))