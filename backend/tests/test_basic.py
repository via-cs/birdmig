import pytest
from app.base import api as flask_app

class TestConfig:
    TESTING = True
    DEBUG = False


@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_bird_data(client):
    # Testing for a bird that exists
    response = client.get('/bird-data/Bird 1')
    assert response.status_code == 200
    assert 'Generic info for unique bird 1' in response.get_data(as_text=True)

    # Testing for a bird that does not exist
    response = client.get('/bird-data/Unknown Bird')
    assert response.status_code == 404
    assert 'Invalid bird' in response.get_data(as_text=True)
