import attr
import pytest

from chubbyrepo.core.entities import Entity


@pytest.fixture()
def some_entity():
    @attr.s()
    class SomeEntity(Entity):
        title = attr.ib()
        body = attr.ib(default='what')

    return SomeEntity(title='nah')


def test_asdict(some_entity):
    entity_dict = some_entity.asdict()
    assert entity_dict == attr.asdict(some_entity)
