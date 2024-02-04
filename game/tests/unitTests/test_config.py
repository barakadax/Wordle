import pytest
from config import config

def test_no_arguments_should_throw():
    with pytest.raises(ValueError):
        config()