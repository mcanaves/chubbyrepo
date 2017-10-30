from unittest import mock

from flask import url_for

from chubbyrepo.core.responses import ResponseSuccess


@mock.patch('chubbyrepo.core.interactors.OrganizationStatsInteractor.execute')
def test_get_organization_stats(mock_interactor, client):
    organization_stats_data = {'name': 'Acme Corp.', 'stars': 200}
    mock_interactor.return_value = ResponseSuccess(organization_stats_data)
    http_response = client.get(url_for('api.organization_stats', org_name='acme_corp'))
    assert http_response.json == organization_stats_data
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('chubbyrepo.core.interactors.ChubbiestRepositoriesInteractor.execute')
def test_get_chubbiest_repositories(mock_interactor, client):
    chubbiest_repos = [{'name': 'Acme Corp.', 'stars': 200}]
    mock_interactor.return_value = ResponseSuccess(chubbiest_repos)
    http_response = client.get(url_for('api.chubbiest_repositories'))
    assert http_response.json == chubbiest_repos
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('chubbyrepo.core.interactors.ChubbiestRepositoriesInteractor.execute')
def test_get_chubbiest_repositories_with_limit(mock_interactor, client):
    chubbiest_repos = [{'name': 'Acme Corp.', 'stars': 200}]
    mock_interactor.return_value = ResponseSuccess(chubbiest_repos)
    http_response = client.get(url_for('api.chubbiest_repositories'), query_string={'limit': 1})
    assert http_response.json == chubbiest_repos
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
