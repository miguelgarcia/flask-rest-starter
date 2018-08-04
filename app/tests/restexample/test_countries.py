from ..fixtures import client
from flask import json

def test_1_list(client):
    """ Test countries listing """
    with client:
        response = client.get('/restexample/countries/',
                                    content_type='application/json')
        assert response.status_code == 200
        expect = [dict(code='AR', name='Argentina'), dict(code='BR', name='Brazil')]
        assert expect == json.loads(response.data.decode())


def test_2_list_limit_offset(client):
    """ Test countries listing with limit and offset params """
    with client:
        response = client.get('/restexample/countries/?offset=1&limit=3',
                                    content_type='application/json')
        assert response.status_code == 200
        expect = [dict(code='BR', name='Brazil')]
        assert expect == json.loads(response.data.decode())

def test_3_create(client):
    """ Test create country """
    data = """ {
        "code": "%s",
        "name": "%s" }
    """ % ('UY', 'Uruguay')
    with client:
        response = client.post('/restexample/countries/',
                                    data=data,
                                    content_type='application/json')
        assert response.status_code == 201


def test_4_get_one(client):
    """ Test get one existing country """
    with client:
        response = client.get('/restexample/countries/AR')
        assert response.status_code == 200
        expect = dict(code='AR', name='Argentina')
        assert expect == json.loads(response.data.decode())

def test_5_get_one_404(client):
    """ Test get one non existing country """
    with client:
        response = client.get('/restexample/countries/XXX')
        assert response.status_code == 404
        expect = dict(message="Not found", status=404)
        assert expect == json.loads(response.data.decode())

def test_6_update_one(client):
    """ Test update existing country """
    data = """ {
        "code": "XXX",
        "name": "NAME"
        }
    """
    with client:
        response = client.put('/restexample/countries/BR',
                                    data=data,
                                    content_type='application/json')
        assert response.status_code == 204
        response = client.get('/restexample/countries/XXX')
        assert response.status_code == 200
        assert json.loads(data) == json.loads(response.data.decode())

def test_7_update_one_404(client):
    """ Test update non existing country """
    data = """ {
        "code": "XXX",
        "name": "NAME"
        }
    """
    with client:
        response = client.put('/restexample/countries/ZZZ',
                                    data=data,
                                    content_type='application/json')
        assert response.status_code == 404
        expect = dict(message="Not found", status=404)
        assert expect == json.loads(response.data.decode())

def test_8_delete_one(client):
    """ Test delete one country """
    with client:
        response = client.get('/restexample/countries/AR')
        assert response.status_code == 200
        response = client.delete('/restexample/countries/AR')
        assert response.status_code == 204
        response = client.get('/restexample/countries/AR')
        assert response.status_code == 404
        expect = dict(message="Not found", status=404)
        assert expect == json.loads(response.data.decode())

def test_9_delete_404(client):
    """ Test delete non existing country """
    with client:
        response = client.delete('/restexample/countries/ZZZ')
        assert response.status_code == 404
        expect = dict(message="Not found", status=404)
        assert expect == json.loads(response.data.decode())