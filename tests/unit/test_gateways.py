from unittest import mock

import pytest

from chubbyrepo.core.entities import OrganizationStats, Repository
from chubbyrepo.core.gateways import DoesNotExist
from chubbyrepo.gateways import GithubGraphQLGateway, RepositoryGateway, StatsGateway


class TestGithubGraphQLGateway:
    @mock.patch('chubbyrepo.gateways.GithubGraphQLGateway._get_result')
    def test_execute(self, mock_get_result):
        mock_get_result.return_value = None, {'data': 'test'}
        assert GithubGraphQLGateway.execute('document') == {'data': 'test'}
        mock_get_result.assert_called_once_with('document')

    @mock.patch('chubbyrepo.gateways.GithubGraphQLGateway._get_result')
    def test_execute_with_errors(self, mock_get_result):
        mock_get_result.return_value = [{
            'message': 'Variable org_name of type String! was provided invalid value',
            'locations': [{'line': 1, 'column': 8}]
        }], None
        with pytest.raises(Exception) as e:
            GithubGraphQLGateway.execute('document')
        assert str(e.value) == 'Variable org_name of type String! was provided invalid value'

    @mock.patch('chubbyrepo.gateways.GithubGraphQLGateway._get_result')
    def test_execute_with_not_found_errors(self, mock_get_result):
        mock_get_result.return_value = [{
            'message': "Could not resolve to an Organization with the login of '3434'.", 'type': 'NOT_FOUND'}], None
        with pytest.raises(DoesNotExist) as e:
            GithubGraphQLGateway.execute('document')
        assert str(e.value) == 'Could not resolve to an Organization with the login of \'3434\'.'

    @mock.patch('requests.post')
    def test_get_result(self, mock_request, config):
        mock_request.return_value.json.return_value = {'data': 'data', 'errors': 'errors'}
        assert GithubGraphQLGateway._get_result('document') == ('errors', 'data')
        mock_request.assert_called_once_with(
            GithubGraphQLGateway.url, json={'query': 'document', 'variables': {}},
            auth=('token', config['GITHUB_API_KEY']))

    @mock.patch('requests.post')
    @mock.patch('chubbyrepo.gateways.current_app')
    def test_get_incompatible_result(self, mock_current_app, mock_request):
        mock_request.return_value.json.return_value = {'incompatible': 'response'}
        with pytest.raises(AssertionError) as e:
            assert GithubGraphQLGateway._get_result('document')
        assert str(e.value) == 'Received non-compatible response "{\'incompatible\': \'response\'}"'


class TestStatsGateway:
    @mock.patch('chubbyrepo.gateways.GithubGraphQLGateway.execute')
    def test_organization_stats(self, mock_execute):
        mock_execute.return_value = {
            'organization': {
                'repositories': {
                    'nodes': [{'name': 'repo-test', 'stargazers': {'totalCount': 10}}],
                    'totalCount': 4
                }
            }
        }
        assert StatsGateway.organization_stats('test') == OrganizationStats(4, Repository('repo-test', 10))
        mock_execute.assert_called_once_with(
            'query($org_name:String!) { organization(login: $org_name) { repositories(first: 1, orderBy: {'
            'field: STARGAZERS, direction: DESC}) { nodes { name stargazers { totalCount}} totalCount}}}',
            {"org_name": 'test'})


class TestRepositoryGateway:
    @mock.patch('chubbyrepo.gateways.GithubGraphQLGateway.execute')
    def test_chubbiest_repositories(self, mock_execute):
        mock_execute.return_value = {
            'search': {
                'edges': [
                    {'node': {'name': 'freeCodeCamp', 'stargazers': {'totalCount': 291350}}},
                    {'node': {'name': 'bootstrap', 'stargazers': {'totalCount': 117311}}},
                    {'node': {'name': 'free-programming-books', 'stargazers': {'totalCount': 96563}}}
                ]
            }
        }
        assert RepositoryGateway.chubbiest_repositories(3) == [
            Repository('freeCodeCamp', 291350),
            Repository('bootstrap', 117311),
            Repository('free-programming-books', 96563)
        ]
        mock_execute.assert_called_once_with(
            'query($limit: Int!) { search(type: REPOSITORY, query: "stars:>1", first: $limit) { edges { node '
            '{ ... on Repository { name stargazers { totalCount}}}}}}', {"limit": 3})
