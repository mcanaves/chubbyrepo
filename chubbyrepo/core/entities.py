"""Domain objects used by ChubbyRepo app."""
from typing import Dict

import attr


class Entity:
    """Base class for all ChubbyRepo entities.

    Attaches attrs helper methods for convenience, and so that our business
    logic doesn't need to rely on attrs directly.

    We use the attrs package to reduce boilerplate for all ChubbyRepo entities:
    "All attrs does is take your declaration, write dunder methods based on
    that information, and attach them to your class."
    """

    def asdict(self) -> Dict:
        """Return class attributes in a dictionary."""
        return attr.asdict(self)


@attr.s
class Repository(Entity):
    """Repository stores metadata for a set of files or directory structure."""

    name = attr.ib(validator=attr.validators.instance_of(str))
    stars = attr.ib(validator=attr.validators.instance_of(int))


@attr.s
class OrganizationStats(Entity):
    """Organization statistics such as number of repositories and biggest one"""

    repositories_count = attr.ib(validator=attr.validators.instance_of(int))
    chubby_repository = attr.ib(validator=attr.validators.instance_of(Repository))
