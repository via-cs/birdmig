import pytest
from app.base import api as flask_app
from flask import json, session
from unittest.mock import patch, MagicMock
from shapely.geometry import LineString
import pandas as pd

class TestConfig:
    TESTING = True
    DEBUG = False

# Mock data for testing purposes
DEMO_bird_data = {
    "Blackpoll Warbler": {
        "info": "Migration details about Blackpoll Warbler",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}]
    },
    "Bald Eagle": {
        "info": "Migration details about Bald Eagle",
        "sdmData": [{"x": 1, "y": 100}, {"x": 2, "y": 200}, {"x": 3, "y": 500}]
    }
}

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_temperature_data(client):
    """Test fetching temperature data."""
    response = client.get('/temperature/2020')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Checks if the response is a list

def test_precipitation_data(client):
    """Test fetching precipitation data."""
    response = client.get('/precipitation/2020')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Checks if the response is a list

def test_bird_data(client):
    """Test fetching bird data."""
    response = client.get('/bird-data/Blackpoll Warbler')
    assert response.status_code == 200
    assert response.json['info'] == "Migration details about Blackpoll Warbler"

def test_valid_bird_data(client):
    # A known bird name in your DEMO_bird_data
    response = client.get('/bird-data/Blackpoll Warbler')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'info' in data
    assert data['info'] == "Migration details about Blackpoll Warbler"
    assert 'sdmData' in data
    assert isinstance(data['sdmData'], list)

def test_get_heatmap_data_success(client):
    # Sample data to return
    sample_data = pd.DataFrame([
        {"LATITUDE": 34.0522, "LONGITUDE": -118.2437},
        {"LATITUDE": 36.7783, "LONGITUDE": -119.4179}
    ])
    
    # Mock pd.read_csv to return a DataFrame
    with patch('pandas.read_csv', return_value=sample_data):
        response = client.get('/get_heatmap_data?bird=ValidBird')
        assert response.status_code == 200
        data = json.loads(response.data)
        expected_data = sample_data[['LATITUDE', 'LONGITUDE']].values.tolist()
        assert data == expected_data

def test_get_heatmap_data_failure(client):
    # Mock pd.read_csv to raise FileNotFoundError
    with patch('pandas.read_csv', side_effect=FileNotFoundError("File not found")):
        
        response = client.get('/get_heatmap_data?bird=InvalidBird')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'File not found'

def test_get_bird_info_success(client):
    # Testing with a valid bird name
    bird_name = "Blackpoll Warbler"
    response = client.get(f'/bird-info/{bird_name}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {"name": bird_name, "info": DEMO_bird_data[bird_name]['info']}

def test_get_bird_info_failure(client):
    # Testing with an invalid bird name
    bird_name = "Unknown Bird"
    response = client.get(f'/bird-info/{bird_name}')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {"error": "Invalid bird"}

def test_get_bird_sdm_data_success(client):
    # Testing with a valid bird name
    bird_name = "Blackpoll Warbler"
    response = client.get(f'/bird-sdm-data/{bird_name}')
    assert response.status_code == 200
    data = json.loads(response.data)
    expected_data = {
        "name": bird_name,
        "sdmData": DEMO_bird_data[bird_name]['sdmData']
    }
    assert data == expected_data

def test_get_bird_sdm_data_failure(client):
    # Testing with an invalid bird name
    bird_name = "Unknown Bird"
    response = client.get(f'/bird-sdm-data/{bird_name}')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data == {'error': 'Bird not found'}

def test_get_bird_ids_success(client):
    selected_bird = 'sparrow'
    bird_ids = ['id1', 'id2', 'id3']
    mock_df = pd.DataFrame({
        'ID': ['id1', 'id1', 'id2', 'id2', 'id3']
    })

    # Mock pandas.read_csv to return a DataFrame
    with patch('pandas.read_csv', return_value=mock_df) as mock_read_csv:
        response = client.get(f'/get_bird_ids?bird={selected_bird}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == bird_ids  # Check if the data returned is as expected
        mock_read_csv.assert_called_once_with(f'./data/{selected_bird}.csv')

def test_get_trajectory_data_success(client):
    selected_bird = 'sparrow'
    bird_id = '123'
    mock_df = pd.DataFrame({
        'ID': ['123', '123', '124'],
        'LATITUDE': [34.0522, 34.0522, 35.0522],
        'LONGITUDE': [-118.2437, -118.2437, -117.2437],
        'TIMESTAMP': ['2021-07-01', '2021-07-02', '2021-07-01']
    })

    # Mock pandas.read_csv to return a DataFrame
    with patch('pandas.read_csv', return_value=mock_df) as mock_read_csv:
        response = client.get(f'/get_trajectory_data?bird={selected_bird}&birdID={bird_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        expected_data = mock_df[mock_df['ID'].str.contains(bird_id)][['LATITUDE', 'LONGITUDE', 'TIMESTAMP']].to_dict(orient='records')
        assert data == expected_data


def simplify_line_mock(coordinates):
    # Simplify the mocking by returning the input or slightly modified
    return coordinates[:1] + coordinates[-1:]

@pytest.fixture
def bird_data():
    return pd.DataFrame({
        'ID': ['1', '1', '2', '2'],
        'LATITUDE': [34.0522, 34.0523, 35.0522, 35.0523],
        'LONGITUDE': [-118.2437, -118.2436, -117.2437, -117.2436],
        'TIMESTAMP': ['2021-07-01 00:00:00', '2021-07-02 00:00:00', '2021-07-01 00:00:00', '2021-07-02 00:00:00']
    })

def test_get_general_migration_success(client, bird_data):
    selected_bird = 'sparrow'
    
    # Mock pandas.read_csv and our simplify_line function
    with patch('pandas.read_csv', return_value=bird_data), \
         patch('app.base.simplify_line', side_effect=simplify_line_mock) as mock_simplify:
        
        response = client.get(f'/get_general_migration?bird={selected_bird}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'segmented_polylines' in data
        mock_simplify.assert_called()


def test_simplify_line():
    from shapely.geometry import LineString

    def simplify_line(coordinates, tolerance=0.1):
        line = LineString(coordinates)
        simplified_line = line.simplify(tolerance, preserve_topology=False)
        return list(zip(*simplified_line.xy))

    # Coordinates that form a rough line
    coordinates = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    # Use a tolerance that should realistically simplify the line to just the endpoints
    expected_simplified = [(0, 0), (5, 5)]
    simplified = simplify_line(coordinates, tolerance=0.01)  # Adjust tolerance as needed
    assert simplified == expected_simplified, f"Expected {expected_simplified}, got {simplified}"

    # Test with a more complex line and a realistic tolerance
    coordinates = [(0, 0), (1, 2), (2, 1), (4, 4), (5, 5)]
    expected_simplified = [(0, 0), (5, 5)]  # Assuming tolerance simplifies to just the start and end points
    simplified = simplify_line(coordinates, tolerance=1.0)  # Increase tolerance to force more simplification
    assert simplified == expected_simplified, f"Expected {expected_simplified}, got {simplified}"

def test_get_heatmap_data_success(client):
    selected_bird = 'sparrow'
    mock_data = pd.DataFrame({
        'LATITUDE': [10.0, 20.0],
        'LONGITUDE': [10.0, 20.0]
    })

    # Mock pd.read_csv to return a DataFrame
    with patch('pandas.read_csv', return_value=mock_data):
        response = client.get(f'/get_heatmap_data?bird={selected_bird}')
        assert response.status_code == 200
        data = json.loads(response.data)
        expected_data = [[10.0, 10.0], [20.0, 20.0]]
        assert data == expected_data, f"Expected {expected_data}, got {data}"

def test_get_heatmap_data_file_error(client):
    selected_bird = 'unknown_bird'

    # Mock pd.read_csv to raise a general exception
    with patch('pandas.read_csv', side_effect=Exception("File read error")):
        response = client.get(f'/get_heatmap_data?bird={selected_bird}')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data == {'error': 'File read error'}, f"Expected error message 'File read error', got '{data['error']}'"

def test_bird_data_empty_input(client):
    """Test fetching bird data with an empty input which is not valid."""
    response = client.get('/bird-data/')
    assert response.status_code == 404  # No bird name provided

def test_get_heatmap_data_no_data(client):
    """Test fetching heatmap data for a valid bird with no actual data."""
    mock_data = pd.DataFrame(columns=['LATITUDE', 'LONGITUDE'])  # No data
    with patch('pandas.read_csv', return_value=mock_data):
        response = client.get('/get_heatmap_data?bird=EmptyDataBird')
        assert response.status_code == 200
        assert json.loads(response.data) == [], "Expected empty list for no data"