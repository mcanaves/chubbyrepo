import pytest

from chubbyrepo.core.requests import (
    ChubbiestRepositoriesRequest, InvalidRequest, OrganizationStatsRequest, ValidRequest
)


class TestInvalidRequest:
    def test_is_false(self):
        request = InvalidRequest()
        assert bool(request) is False

    def test_accepts_errors(self):
        request = InvalidRequest()
        request.add_error(parameter='aparam', message='wrong value')
        request.add_error(parameter='anotherparam', message='wrong type')
        assert request.has_errors() is True
        assert len(request.errors) == 2


class TestValidRequest:
    def test_is_true(self):
        request = ValidRequest()
        assert True is bool(request)


class TestOrganizationStatsRequest:
    def test_build(self):
        request = OrganizationStatsRequest(organization_name='Sirius Cybernetics Corp.')
        assert request.organization_name == 'Sirius Cybernetics Corp.'
        assert bool(request) is True

    def test_build_from_dict(self):
        request = OrganizationStatsRequest.from_dict({'organization_name': 'Sirius Cybernetics Corp.'})
        assert request.organization_name == 'Sirius Cybernetics Corp.'
        assert bool(request) is True

    @pytest.mark.parametrize('test_input', [({'organization_name': 1}), ({})])
    def test_build_from_dict_with_invalid_organization_name(self, test_input):
        request = OrganizationStatsRequest.from_dict(test_input)
        assert request.has_errors()
        assert request.errors[0]['parameter'] == 'organization_name'
        assert bool(request) is False


class TestChubbiestRepositoriesRequest:
    @pytest.mark.parametrize('test_input,expected', [(2, 2), (None, 10)])
    def test_build(self, test_input, expected):
        request = ChubbiestRepositoriesRequest(limit=test_input)
        assert request.limit == expected
        assert bool(request) is True

    @pytest.mark.parametrize('test_input,expected', [({'limit': 2}, 2), ({}, 10)])
    def test_build_from_dict(self, test_input, expected):
        request = ChubbiestRepositoriesRequest.from_dict(test_input)
        assert request.limit == expected
        assert bool(request) is True

    @pytest.mark.parametrize("test_input", [0, 101, 'asdfg'])
    def test_build_from_dict_with_invalid_limit(self, test_input):
        request = ChubbiestRepositoriesRequest.from_dict({'limit': test_input})
        assert request.has_errors()
        assert request.errors[0]['parameter'] == 'limit'
        assert bool(request) is False
