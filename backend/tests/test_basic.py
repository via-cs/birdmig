import pytest
from app.base import api as flask_app

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_bird_info(client):
    # Testing for a bird that exists
    response = client.get('/bird-info/Bird 1')
    assert response.status_code == 200
    assert 'Blackpoll Warbler' in response.get_data(as_text=True)

    # Testing for a bird that does not exist
    response = client.get('/bird-info/Unknown Bird')
    assert response.status_code == 404
    assert 'Bird not found' in response.get_data(as_text=True)

def test_get_bird_sdm_data(client):
    response = client.get('/bird-sdm-data/Bird 1')
    assert response.status_code == 200
    data = response.get_json()  # This parses the JSON response into a Python dictionary
    assert data['name'] == 'Bird 1'
    assert data['sdmData'][0] == {'x': 1, 'y': 300}  # Check the first element in the SDM data list


def test_migration_images(client):
    response = client.get('/migration_images/blackpoll_warbler_kde_heatmap.html')
    assert response.status_code == 200
    assert 'heat_map_e833d4f994813e3678911f266cf06ab3.addTo(map_c41f81891829e14e1ba664e26fe1a80d);' in response.get_data(as_text=True)


# Optional: Test invalid, empty, and special characters for robustness
def test_get_bird_info_special_characters(client):
    response = client.get('/bird-info/@#!$')
    assert response.status_code == 404  # Assuming special characters are not valid
