import pytest
from flask import current_app

from chubbyrepo import create_app


@pytest.mark.parametrize("environ, expected_config", [
    ("development", {'SECRET_KEY': 'SUPER SECRET KEY', 'DEBUG': True, 'TESTING': False}),
    ("testing", {'SECRET_KEY': 'SUPER SECRET KEY', 'DEBUG': True, 'TESTING': True}),
    ("production", {'SECRET_KEY': None, 'DEBUG': False, 'TESTING': False}),
])
def test_config(environ, expected_config):
    app = create_app(environ)
    assert app.config['SECRET_KEY'] == expected_config['SECRET_KEY']
    assert expected_config['DEBUG'] is app.config['DEBUG']
    assert expected_config['TESTING'] is app.config['TESTING']
    assert app.config['CACHE_TYPE'] == 'redis'
    assert app.config['CACHE_REDIS_HOST'] == 'chubby-cache'
    assert app.config['GITHUB_API_KEY'] is None
    assert current_app is not None
