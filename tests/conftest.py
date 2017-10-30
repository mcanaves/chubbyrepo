import pytest

from chubbyrepo import create_app


@pytest.yield_fixture(scope='function')
def app():
    return create_app('testing')
