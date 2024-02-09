import pytest
from config import config

def test_no_arguments_should_throw():
    with pytest.raises(ValueError):
        config()

def test_wrong_type_input_should_throw():
    with pytest.raises(ValueError):
        config(ttl='8', max_games='42', max_retries='1', ip=8, port='1', words_path='../valid-wordle-words.txt')

def test_missing_value_should_throw():
    with pytest.raises(ValueError):
        config(ttl=8, max_games=42, max_retries=1, ip='a', words_path='../valid-wordle-words.txt')

def test_all_values_should_be_expected():
    res = config(ttl=8, max_games=42, max_retries=1, ip='a', port=1, words_path='../valid-wordle-words.txt')
    assert isinstance(res, config)
    assert isinstance(res.ttl, int)
    assert res.ttl == 8
    assert isinstance(res.max_games, int)
    assert res.max_games == 42
    assert isinstance(res.max_retries, int)
    assert res.max_retries == 1
    assert isinstance(res.ip, str)
    assert res.ip == 'a'
    assert isinstance(res.port, int)
    assert res.port == 1
    assert isinstance(res.words_path, str)
    assert res.words_path == '../valid-wordle-words.txt'
