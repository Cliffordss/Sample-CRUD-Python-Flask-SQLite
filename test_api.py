import pytest
import json
import warnings
from main import app
from db import create_tables
import os

# Suppress the jsonschema.RefResolver deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning, module="jsonschema")

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE_NAME'] = 'test_games.db'
    
    # Create a test client
    with app.test_client() as client:
        # Create tables before each test
        with app.app_context():
            create_tables()
        yield client
        # Clean up after each test
        try:
            os.remove('test_games.db')
        except OSError:
            pass

def test_create_game(client):
    """Test creating a new game"""
    # Test successful creation
    response = client.post('/api/v1/games',
        json={'name': 'Test Game', 'price': 29.99, 'rate': 5},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Test Game'
    assert float(data['price']) == 29.99
    assert int(data['rate']) == 5
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data

    # Test invalid input
    response = client.post('/api/v1/games',
        json={'name': '', 'price': -1, 'rate': 6},
        headers={'Content-Type': 'application/json'}
    )
    data = json.loads(response.data)
    print(f"Invalid input response: {data}")  # Debug print
    assert response.status_code == 400
    assert 'error' in data

def test_get_games(client):
    """Test getting list of games"""
    # Create a test game first
    client.post('/api/v1/games',
        json={'name': 'Test Game', 'price': 29.99, 'rate': 5},
        headers={'Content-Type': 'application/json'}
    )

    # Test getting all games
    response = client.get('/api/v1/games')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0
    assert data[0]['name'] == 'Test Game'
    assert float(data[0]['price']) == 29.99
    assert int(data[0]['rate']) == 5

def test_get_game(client):
    """Test getting a single game"""
    # Create a test game first
    response = client.post('/api/v1/games',
        json={'name': 'Test Game', 'price': 29.99, 'rate': 5},
        headers={'Content-Type': 'application/json'}
    )
    data = json.loads(response.data)
    game_id = data['id']

    # Test getting existing game
    response = client.get(f'/api/v1/games/{game_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Game'
    assert float(data['price']) == 29.99
    assert int(data['rate']) == 5

    # Test getting non-existent game
    response = client.get('/api/v1/games/999')
    data = json.loads(response.data)
    print(f"Non-existent game response: {data}")  # Debug print
    assert response.status_code == 404
    assert 'error' in data

def test_update_game(client):
    """Test updating a game"""
    # Create a test game first
    response = client.post('/api/v1/games',
        json={'name': 'Test Game', 'price': 29.99, 'rate': 5},
        headers={'Content-Type': 'application/json'}
    )
    data = json.loads(response.data)
    game_id = data['id']

    # Test successful update
    response = client.put(f'/api/v1/games/{game_id}',
        json={'name': 'Updated Game', 'price': 39.99, 'rate': 4},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Game'
    assert float(data['price']) == 39.99
    assert int(data['rate']) == 4

    # Test invalid update
    response = client.put(f'/api/v1/games/{game_id}',
        json={'name': '', 'price': -1, 'rate': 6},
        headers={'Content-Type': 'application/json'}
    )
    data = json.loads(response.data)
    print(f"Invalid update response: {data}")  # Debug print
    assert response.status_code == 400
    assert 'error' in data

    # Test updating non-existent game
    response = client.put('/api/v1/games/999',
        json={'name': 'Updated Game', 'price': 39.99, 'rate': 4},
        headers={'Content-Type': 'application/json'}
    )
    data = json.loads(response.data)
    print(f"Update non-existent game response: {data}")  # Debug print
    assert response.status_code == 404
    assert 'error' in data
    assert data['error'] == 'Game not found'

def test_delete_game(client):
    """Test deleting a game"""
    # Create a test game first
    response = client.post('/api/v1/games',
        json={'name': 'Test Game', 'price': 29.99, 'rate': 5},
        headers={'Content-Type': 'application/json'}
    )
    data = json.loads(response.data)
    game_id = data['id']

    # Test successful deletion
    response = client.delete(f'/api/v1/games/{game_id}')
    assert response.status_code == 204

    # Verify game is deleted
    response = client.get(f'/api/v1/games/{game_id}')
    data = json.loads(response.data)
    print(f"Verify deletion response: {data}")  # Debug print
    assert response.status_code == 404
    assert 'error' in data

    # Test deleting non-existent game
    response = client.delete('/api/v1/games/999')
    data = json.loads(response.data)
    print(f"Delete non-existent game response: {data}")  # Debug print
    assert response.status_code == 404
    assert 'error' in data 