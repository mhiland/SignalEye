import pytest
import sys
import os
from flask import Flask
os.environ['UNIT_TESTING'] = 'True'
test_file_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.abspath(os.path.join(test_file_dir, '../frontend'))
sys.path.insert(0, module_path)
from app import app, networks_data, DATA_FILE

@pytest.fixture
def client():
    """Fixture for setting up the Flask test client."""
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route of the application."""
    response = client.get('/')

    assert response.status_code == 200
    assert len(response.data) > 0
    assert b'<!DOCTYPE html>' in response.data

def test_download_route(client):
    """Test the download route of the application."""
    response = client.get('/download')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Content-Disposition'] == 'attachment; filename=persistent_networks.json'
