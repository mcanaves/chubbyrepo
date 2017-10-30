from typing import List

from chubbyrepo.core.entities import OrganizationStats, Repository


class DoesNotExist(Exception):
    """Exception to be raised when an entity is not found in gateway."""
    pass


class StatsGateway:
    def organization_stats(self, name: str) -> OrganizationStats:
        raise NotImplementedError


class RepositoryGateway:
    def chubbiest_repositories(self, limit: int) -> List[Repository]:
        raise NotImplementedError
