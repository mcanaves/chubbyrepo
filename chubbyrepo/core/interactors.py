"""Functions that encapsulate business logic for the app.

Interactor are the place where we implement classes that query the repository,
apply business rules, logic, and whatever transformation we need for our data,
and return the results
"""
from typing import Union

from chubbyrepo.core.gateways import DoesNotExist, RepositoryGateway, StatsGateway
from chubbyrepo.core.requests import (
    ChubbiestRepositoriesRequest, InvalidRequest, OrganizationStatsRequest, ValidRequest
)
from chubbyrepo.core.responses import ResponseFailure, ResponseSuccess


class Interactor:
    """Base class for all ChubbyRepo interactors."""

    def execute(self, request_object: Union[ValidRequest, InvalidRequest]) -> Union[ResponseSuccess, ResponseFailure]:
        if not request_object:
            return ResponseFailure.build_from_invalid_request(request_object)
        try:
            return self._process_request(request_object)
        except DoesNotExist as exc:
            return ResponseFailure.build_resource_error("{}".format(exc))
        except Exception as exc:
            return ResponseFailure.build_system_error("{}: {}".format(exc.__class__.__name__, "{}".format(exc)))

    def _process_request(self, request_object: ValidRequest) -> ResponseSuccess:
        raise NotImplementedError("process_request() not implemented by Interactor class")


class OrganizationStatsInteractor(Interactor):
    """Return organization stats given a organization name."""

    def __init__(self, gateway: StatsGateway):
        self.gateway = gateway

    def _process_request(self, request_object: OrganizationStatsRequest):
        repository_stats = self.gateway.organization_stats(request_object.organization_name)
        return ResponseSuccess(repository_stats.asdict())


class ChubbiestRepositoriesInteractor(Interactor):
    """Get most starred repositories."""

    def __init__(self, gateway: RepositoryGateway):
        self.gateway = gateway

    def _process_request(self, request_object: ChubbiestRepositoriesRequest):
        chubbiest_repositories = self.gateway.chubbiest_repositories(request_object.limit)
        return ResponseSuccess([r.asdict() for r in chubbiest_repositories])
