import sys
import os

# Adjust the Python path to ensure the imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from configs.db import get_db_connection  
import pytest
from app import app
from unittest.mock import MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_valid_request(client, mocker):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('db.get_db_connection', return_value=mock_conn)
    
    # Mock the data returned by the cursor
    mock_cursor.fetchall.return_value = [
        ('2016-01-01', 1150, 3),
        ('2016-01-02', 1300, 2)
    ]

    # Perform the request to the /rates endpoint
    response = client.get('/rates?date_from=2016-01-01&date_to=2016-01-02&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 200
    data = response.json

    # Check the returned JSON structure and content
    assert len(data) == 2
    assert data[0]['day'] == '2016-01-01'
    assert data[0]['average_price'] == 1150
    assert data[1]['day'] == '2016-01-02'
    assert data[1]['average_price'] is None  # Less than 3 prices

def test_missing_parameters(client):
    # Perform the request with missing parameters
    response = client.get('/rates?date_from=2016-01-01&date_to=2016-01-02')
    assert response.status_code == 400
    assert 'error' in response.json

def test_invalid_date_format(client):
    # Perform the request with an invalid date format
    response = client.get('/rates?date_from=01-01-2016&date_to=2016-01-02&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 400
    assert 'error' in response.json

def test_no_data_available(client, mocker):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('db.get_db_connection', return_value=mock_conn)
    
    # Mock the data returned by the cursor
    mock_cursor.fetchall.return_value = []

    # Perform the request to the /rates endpoint with no data available
    response = client.get('/rates?date_from=2017-01-01&date_to=2017-01-02&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 200
    data = response.json

    # Check the returned JSON structure and content
    assert len(data) == 0

def test_less_than_three_prices(client, mocker):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('db.get_db_connection', return_value=mock_conn)
    
    # Mock the data returned by the cursor
    mock_cursor.fetchall.return_value = [
        ('2016-01-02', 1300, 2)
    ]

    # Perform the request to the /rates endpoint
    response = client.get('/rates?date_from=2016-01-02&date_to=2016-01-02&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 200
    data = response.json

    # Check the returned JSON structure and content
    assert len(data) == 1
    assert data[0]['day'] == '2016-01-02'
    assert data[0]['average_price'] is None  # Less than 3 prices
