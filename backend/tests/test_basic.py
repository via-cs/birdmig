import pytest

from fastapi.responses import Response
from fastapi.testclient import TestClient

import json

from app.base import app as fast_app


'''
Helper function for tests
'''

def read_response_body(response):
    return json.loads(response.content.decode())

'''
Test functions
'''

@pytest.fixture
def app():
    
    yield fast_app

@pytest.fixture
def client(app):
    
    yield TestClient(app)
    
    
def test_get_bird_info(client):
    
    valid_birds = {
        "Blackpoll Warbler" : "Migration details about Blackpoll Warbler",
        "Bald Eagle" : "Migration details about Bald Eagle",
        "White Fronted Goose" : "Migration details about White Fronted Goose",
        "Long Billed Curlew" : "Migration details about Long Billed Curlew",
        "Whimbrel" : "Migration details about Whimbrel"
    }
        
    # Test for each bird that exists    
    for bird in valid_birds:
        
        response = client.get(f'/bird-info/{bird}')
        
        assert response.status_code == 200
        
        # Decode the response body.
        response_body = read_response_body(response)
        assert response_body['name'] == bird
        assert response_body['info'] == valid_birds[bird]
        
    # Test an invalid entry
    response = client.get(f'/bird-info/Invalid_Bird')
    
    assert response.status_code == 404
    
def test_get_temp_data(client):
    
    response = client.get(f'/temperature/{2021}')
    
    assert response.status_code == 200
    # TODO: continue coverage for climate data
    # response_body = read_response_body(response)
    
@pytest.mark.skip(reason= "This test takes a very long time. Uncomment when doing other tests.")
def test_valid_predictions(client):
    
    valid_birds = [
        "warbler",
        "eagle",
        "anser",
        "curlew",
        "whimbrel"
    ]
    
    for bird in valid_birds:
        
        # Test all possible valid emission types.
        ssps = [
            'ssp126',
            'ssp245',
            'ssp370',
            'ssp585'
        ]
        
        for ssp in ssps:
            
            # Test all possible valid years.
            for year in range(2021, 2100):
                payload = {
                    "bird": bird,
                    "year": year,
                    "emissions": ssp,
                }
                
                response = client.put('/prediction', json= payload)
                response_body = read_response_body(response)
                
                assert response.status_code == 200
                assert response_body['resFormat'] == "PNG"

def test_invalid_predictions(client):
        
    # Test invalid inputs
    invalid_entries = [
        ("bad_bird", 2050, 'ssp126'),
        ("eagle", 2101, 'ssp126'),
        ("anser", 2050, 'invalid')
    ]
    
    for invalid_entry in invalid_entries:
        
        # Test bad inputs.
        try:
            bad_payload = {
                "bird": invalid_entry[0],
                "year": invalid_entry[1],
                "emissions": invalid_entry[2]
            }
            
            client.put('/prediction', json= bad_payload)
        except Exception as e:
            
            if invalid_entry[0] == 'bad_bird':
                # This should throw a key error.
                assert isinstance(e, KeyError)
            else:
                # This should throw a file not found error.
                assert isinstance(e, FileNotFoundError)

def test_get_bird_ids(client):
    
    # Test the 
    valid_birds = [
        "warbler",
        "eagle",
        "anser",
        "curlew",
        "whimbrel"
    ]
    
    for bird in valid_birds:
        client.get('/get_bird_ids', )