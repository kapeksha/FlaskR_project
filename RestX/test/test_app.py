import pytest
from app import app, DAO

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: Clear DAO and add initial todos
    DAO.todos = []
    DAO.counter = 0
    DAO.create({'task': 'Build an API'})
    DAO.create({'task': '?????'})
    DAO.create({'task': 'profit!'})
    yield
    # Teardown: Clear DAO after tests if needed
    DAO.todos = []
    DAO.counter = 0

def test_get_todos(client):
    """Test fetching all todos"""
    rv = client.get('/todos/')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 3
    assert json_data[0]['task'] == 'Build an API'
    assert json_data[1]['task'] == '?????'
    assert json_data[2]['task'] == 'profit!'

def test_get_todo_by_id(client):
    """Test fetching a single todo by id"""
    rv = client.get('/todos/1')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['task'] == 'Build an API'

    rv = client.get('/todos/999')
    assert rv.status_code == 404

def test_create_todo(client):
    """Test creating a new todo"""
    rv = client.post('/todos/', json={'task': 'New Task'})
    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data['task'] == 'New Task'
    assert 'id' in json_data

def test_create_todo_invalid(client):
    """Test creating a new todo with invalid data"""
    rv = client.post('/todos/', json={})
    assert rv.status_code == 400

def test_update_todo(client):
    """Test updating an existing todo"""
    rv = client.put('/todos/1', json={'task': 'Updated Task'})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['task'] == 'Updated Task'

    rv = client.put('/todos/999', json={'task': 'Nonexistent Task'})
    assert rv.status_code == 404

def test_update_todo_invalid(client):
    """Test updating a todo with invalid data"""
    rv = client.put('/todos/1', json={})
    assert rv.status_code == 400

def test_delete_todo(client):
    """Test deleting a todo"""
    rv = client.delete('/todos/1')
    assert rv.status_code == 204

    rv = client.get('/todos/1')
    assert rv.status_code == 404

    rv = client.delete('/todos/999')
    assert rv.status_code == 404
