from typing import List

import requests
from flask import current_app

from chubbyrepo.core.entities import OrganizationStats, Repository
from chubbyrepo.core.gateways import RepositoryGateway as BaseRepositoryGateway
from chubbyrepo.core.gateways import StatsGateway as BaseStatsGateway
from chubbyrepo.core.gateways import DoesNotExist


class GithubGraphQLGateway:
    """Base class for all Github based gateways."""
    url = 'https://api.github.com/graphql'

    @classmethod
    def execute(cls, document, *args, **kwargs):
        errors, data = cls._get_result(document, *args, **kwargs)
        if errors:
            if errors[0].get('type') == 'NOT_FOUND':
                raise DoesNotExist(str(errors[0].get('message')))
            raise Exception(str(errors[0].get('message')))
        return data

    @classmethod
    def _get_result(cls, document, variable_values=None):
        payload = {
            'query': document,
            'variables': variable_values or {}
        }
        request = requests.post(cls.url, json=payload, auth=('token', current_app.config['GITHUB_API_KEY']))
        request.raise_for_status()
        result = request.json()
        assert 'errors' in result or 'data' in result, 'Received non-compatible response "{}"'.format(result)
        return result.get('errors'), result.get('data')


class StatsGateway(GithubGraphQLGateway, BaseStatsGateway):
    @classmethod
    def organization_stats(cls, name: str) -> OrganizationStats:
        document = 'query($org_name:String!) { organization(login: $org_name) { repositories(first: 1, orderBy: {' \
                   'field: STARGAZERS, direction: DESC}) { nodes { name stargazers { totalCount}} totalCount}}}'
        result = cls.execute(document, {"org_name": name})['organization']['repositories']
        chubby_repo = Repository(result['nodes'][0]['name'], result['nodes'][0]['stargazers']['totalCount'])
        return OrganizationStats(result['totalCount'], chubby_repo)


class RepositoryGateway(GithubGraphQLGateway, BaseRepositoryGateway):
    @classmethod
    def chubbiest_repositories(cls, limit: int) -> List[Repository]:
        document = 'query($limit: Int!) { search(type: REPOSITORY, query: "stars:>1", first: $limit) { edges { node ' \
                   '{ ... on Repository { name stargazers { totalCount}}}}}}'
        result = cls.execute(document, {"limit": limit})
        return [Repository(r['node']['name'], r['node']['stargazers']['totalCount']) for r in result['search']['edges']]
