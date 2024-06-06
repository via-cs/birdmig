import pytest

from fastapi.responses import Response
from fastapi.testclient import TestClient

import json
import os

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
    
def test_get_temp_data(client):
    
    response = client.get(f'/temperature/{2021}')
    assert response.status_code == 200
    
def test_get_precip_data(client):
  
  response = client.get(f'/precipitation/{2021}')
  assert response.status_code == 200
    
def test_valid_predictions(client):
    
    test_directory = os.getcwd()
    os.chdir('./app')
    
    valid_birds = [
        "warbler",
        "eagle",
        "anser",
        "curlew",
        "whimbrel"
    ]
    try:
      for bird in valid_birds:
        payload = {
                        "bird": bird,
                        "year": 2025,
                        "emissions": 'ssp245',
                    }
                    
        response = client.put('/prediction', json= payload)    
        assert response.status_code == 200
    
    finally:
      os.chdir(test_directory)
        

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

def test_get_sdm_data(client):
    
    valid_birds = [
        "Blackpoll Warbler",
        "Bald Eagle",
        "White Fronted Goose",
        "Long Billed Curlew",
        "Whimbrel"
    ]
    
    for bird in valid_birds:
        response = client.get(f'/bird-info/{bird}')
        
        assert response.status_code == 200
    
    assert client.get(f'/bird-info/bad_get').status_code == 404
    

def test_read_json(client):
  test_directory = os.getcwd()
  os.chdir('./app')
  
  try:
    json_request_response = client.get(f'./json/tavg.json')
    assert json_request_response.status_code == 200
  finally:
    os.chdir(test_directory)


def test_get_bird_ids(client):
    
    # Test if the backend can retreive bird ids for all valid birds.
    valid_birds = [
        "warbler",
        "eagle",
        "anser",
        "curlew",
        "whimbrel"
    ]
    
    test_directory = os.getcwd()
    os.chdir('./app')
    
    try:
      for bird in valid_birds:
          
          ids_response = client.get(f'/get_bird_ids?bird={bird}')
          assert ids_response.status_code == 200
          
          ids_content = read_response_body(ids_response)
          traj_resp = client.get(f'/get_trajectory_data?bird={bird}&birdID={ids_content[0]}')
              
          assert traj_resp.status_code == 200
              
          # Assert that for each bird, a bad response is handled properly.
          assert client.get(f'/get_trajectory_data?bird={bird}&birdID=BAD_ID').status_code == 404
      
      # Ensure that bad 'get' requests are handled properly.
      response = client.get(f'/get_bird_ids?bird=bad_ID')
      assert response.status_code == 404
      
      assert client.get(f'/get_trajectory_data?bird=BAD_ID&birdID=BAD_ID').status_code == 404

    finally:
      os.chdir(test_directory)
    
    
def test_get_heatmap(client):
    valid_birds = [
        "warbler",
        "eagle",
        "anser",
        "curlew",
        "whimbrel"
    ]
    
    test_directory = os.getcwd()
    os.chdir('./app')
    
    try:
      for bird in valid_birds:
          
          response = client.get(f'/get_heatmap_data?bird={bird}')
          assert response.status_code == 200
      
      assert client.get(f'/get_heatmap_data?bird=BAD_ID').status_code == 400
    finally:
      os.chdir(test_directory)