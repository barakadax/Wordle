import pytest
from game import Game
from typing import Optional

def test_no_arguments_should_throw():
    with pytest.raises(ValueError):
        Game()

def test_wrong_type_input_should_throw():
    with pytest.raises(ValueError):
        Game(retries='1', target=1, has_won='a')

def test_missing_value_should_throw():
    with pytest.raises(ValueError):
        Game(retries=1, target='a')

def test_all_values_should_be_expected():
    res = Game(retries=1, target='a', has_won=None)
    assert isinstance(res, Game)
    assert isinstance(res.retries, int)
    assert res.retries == 1
    assert isinstance(res.target, str)
    assert res.target == 'a'
    assert isinstance(res.has_won, type(None))
    assert res.has_won == None
    res.has_won = True
    assert isinstance(res.has_won, bool)
    assert res.has_won == True
