import pytest
from wordle import Wordle
from config import config
from fastapi.testclient import TestClient

@pytest.fixture
def app() -> Wordle:
    test_config = config(ttl=600,
                 max_games=100,
                 max_retries=5,
                 ip='127.0.0.1',
                 port=8000,
                 words_path='test-wordle-words.txt')
    return Wordle(test_config).app

@pytest.fixture
def client(app):
    return TestClient(app)

def test_all_options(client):
    headers={"Content-Type": "text/plain"}

    start_response = client.get('/start')
    assert start_response.status_code == 200
    assert 'session' in start_response.json()
    session_id = start_response.json()['session']

    game_response = client.post('/play/session/nonExistentSession', content='happy', headers=headers)
    assert game_response.status_code == 404
    assert 'response' in game_response.json()
    assert game_response.json()['response'] == 'this session doesn\'t exists'
    assert game_response.headers['statues'] == 'deleted'

    game_response = client.post(f'/play/session/{session_id}')
    assert game_response.status_code == 422

    game_response = client.post(url=f'/play/session/{session_id}', content='early', headers=headers)
    assert game_response.status_code == 403
    assert 'response' in game_response.json()
    assert game_response.json()['response'] == 'Not an acceptable word'

    game_response = client.post(f'/play/session/{session_id}', content='tooLong', headers=headers)
    assert game_response.status_code == 400
    assert 'response' in game_response.json()
    assert game_response.json()['response'] == 'Input must be 5 letters long'

    game_response = client.post(f'/play/session/{session_id}', content='tiny', headers=headers)
    assert game_response.status_code == 400
    assert 'response' in game_response.json()
    assert game_response.json()['response'] == 'Input must be 5 letters long'

    game_response = client.post(f'/play/session/{session_id}', content='happy', headers=headers)
    assert game_response.status_code == 200
    assert 'response' in game_response.json()
    assert game_response.json()['response'] == 'You win!!! the word was: happy'
    assert game_response.headers['statues'] == 'won'

    game_response = client.post(url=f'/play/session/{session_id}', content='happy', headers=headers)
    assert game_response.status_code == 208
    assert 'response' in game_response.json()
    assert game_response.json()['response'] == 'Game already finished the word was: happy and you have won'

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'roles' in response.json()

def test_endpoint_doesnt_exist(client):
    response = client.get('/aaa')
    assert response.status_code == 404
    assert 'details' in response.json()
    assert response.json()['details'] == 'None existing endpoint'
