"""Functional tests for the microservice (http tests) against the APIs"""
#import pytest
from flask import json
from service import app


def test_user_save():
    """Test user saving"""
    response = app.test_client().put(
        '/reservations',
        data=json.dumps({'seat_num': "12C", 'flight_id': "QWE123", "customer_id": "anon"}),
        content_type='application/json',
    )

    # data = json.loads(response.get_data(as_text=True))

    valid_response = (response.status_code == 200 or response.status_code == 403)
    assert valid_response
    #assert data['completion']['user_id'] == '12345'



def test_getter():
    """test greeter endpoint"""
    response = app.test_client().get(
        '/reservations?flight_id=QWE123'
    )

    # data = response.get_data(as_text=True)

    assert response.status_code == 200
    # assert data == "Hello nina!"
