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
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('configs.db.get_db_connection', return_value=mock_conn)
    mock_cursor.fetchall.return_value = [
        ('2016-01-01', 882, 3),  
        ('2016-01-02', 882, 3)   
    ]


    response = client.get('/rates?date_from=2016-01-01&date_to=2016-01-02&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 200
    data = response.json

    assert len(data) == 2
    assert data[0]['day'] == '2016-01-01'
    assert data[0]['average_price'] == 882  
    assert data[1]['day'] == '2016-01-02'
    assert data[1]['average_price'] == 882  


def test_missing_parameters(client):
    response = client.get('/rates?date_from=2016-01-01&date_to=2016-01-02')
    assert response.status_code == 400
    assert 'error' in response.json

def test_invalid_date_format(client):
    response = client.get('/rates?date_from=01-01-2016&date_to=2016-01-02&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 400
    assert 'error' in response.json

def test_no_data_available(client, mocker):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('configs.db.get_db_connection', return_value=mock_conn)
    mock_cursor.fetchall.return_value = []

    response = client.get('/rates?date_from=2017-01-01&date_to=2017-01-02&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 0

def test_less_than_three_prices(client, mocker):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mocker.patch('configs.db.get_db_connection', return_value=mock_conn)
    
    mock_cursor.fetchall.return_value = [
        ('2016-01-02', 882, 3)  
    ]
    response = client.get('/rates?date_from=2016-01-02&date_to=2016-01-02&origin=CNSGH&destination=NLRTM')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]['day'] == '2016-01-02'
    assert data[0]['average_price'] == 882  

def test_invalid_date_range_returns_null(client):
    # Perform the request with an invalid date range (to_date < from_date)
    response = client.get('/rates?date_from=2016-01-02&date_to=2016-01-01&origin=CNSGH&destination=NLRTM')
    
    assert response.status_code == 200
    data = response.json
    assert len(data) == 0  
