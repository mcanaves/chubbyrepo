from unittest import mock

import pytest

from chubbyrepo.core.entities import OrganizationStats, Repository
from chubbyrepo.core.gateways import DoesNotExist
from chubbyrepo.core.interactors import ChubbiestRepositoriesInteractor, Interactor, OrganizationStatsInteractor
from chubbyrepo.core.requests import ChubbiestRepositoriesRequest, InvalidRequest, OrganizationStatsRequest
from chubbyrepo.core.responses import ResponseFailure


class TestInteractor:
    def test_cannot_process_valid_requests(self):
        valid_request = mock.MagicMock()
        valid_request.__bool__.return_value = True
        interactor = Interactor()
        response = interactor.execute(valid_request)
        assert not response
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'NotImplementedError: process_request() not implemented by Interactor class'

    def test_can_process_invalid_requests_and_returns_response_failure(self):
        invalid_request = InvalidRequest()
        invalid_request.add_error('someparam', 'somemessage')
        interactor = Interactor()
        response = interactor.execute(invalid_request)
        assert not response
        assert response.type == ResponseFailure.PARAMETERS_ERROR
        assert response.message == 'someparam: somemessage'

    def test_can_manage_generic_exception_from_process_request(self):
        class TestException(Exception):
            pass

        interactor = Interactor()
        interactor._process_request = mock.Mock()
        interactor._process_request.side_effect = TestException('somemessage')
        response = interactor.execute(mock.Mock)
        assert not response
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == 'TestException: somemessage'

    def test_can_manage_not_found_exception_from_process_request(self):
        interactor = Interactor()
        interactor._process_request = mock.Mock()
        interactor._process_request.side_effect = DoesNotExist('somemessage')
        response = interactor.execute(mock.Mock)
        assert not response
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == 'somemessage'


class TestOrganizationStatsInteractor:
    @pytest.fixture
    def organization_stats_entity(self):
        return OrganizationStats(repositories_count=10, chubby_repository=Repository(name='Test', stars=10))

    def test_execute(self, organization_stats_entity):
        gateway = mock.Mock()
        gateway.organization_stats.return_value = organization_stats_entity
        interactor = OrganizationStatsInteractor(gateway)
        request = OrganizationStatsRequest.from_dict({'organization_name': 'Sirius Cybernetics Corp.'})
        response = interactor.execute(request)
        assert bool(response) is True
        gateway.organization_stats.assert_called_with('Sirius Cybernetics Corp.')
        assert response.value == organization_stats_entity.asdict()


class TestChubbiestRepositoriesInteractor:
    @pytest.fixture
    def chubbiest_repositories_entities(self):
        repo_1 = Repository(name='Test 1', stars=30)
        repo_2 = Repository(name='Test 2', stars=10)
        repo_3 = Repository(name='Test 3', stars=2)
        return [repo_1, repo_2, repo_3]

    def test_execute(self, chubbiest_repositories_entities):
        gateway = mock.Mock()
        gateway.chubbiest_repositories.return_value = chubbiest_repositories_entities
        interactor = ChubbiestRepositoriesInteractor(gateway)
        request = ChubbiestRepositoriesRequest.from_dict({'limit': 3})
        response = interactor.execute(request)
        assert bool(response) is True
        gateway.chubbiest_repositories.assert_called_with(3)
        assert response.value == [r.asdict() for r in chubbiest_repositories_entities]
