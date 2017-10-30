from unittest import mock

from flask import url_for


@mock.patch('requests.post')
def test_org_stats(mock_post, client):
    mock_post.return_value.json.return_value = {
        'data': {
            'organization': {
                'repositories': {
                    'nodes': [{'name': 'dj-txmoney', 'stargazers': {'totalCount': 4}}],
                    'totalCount': 4
                }
            }
        }
    }
    http_response = client.get(url_for('api.organization_stats', org_name='Txerpa'))
    assert http_response.json == {
        'chubby_repository': {
            'name': 'dj-txmoney',
            'stars': 4
        },
        'repositories_count': 4
    }
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('requests.post')
def test_org_stats_not_found(mock_post, client):
    mock_post.return_value.json.return_value = {
        "data": {"organization": None},
        "errors": [{
            "message": "Could not resolve to an Organization with the login of '3434'.",
            "type": "NOT_FOUND",
            "path": ["organization"],
            "locations": [{
                "line": 2,
                "column": 3
            }]
        }]
    }
    http_response = client.get(url_for('api.organization_stats', org_name='3434'))
    assert http_response.json == {
        'message': "Could not resolve to an Organization with the login of '3434'.",
        'type': 'RESOURCE_ERROR'
    }
    assert http_response.status_code == 404
    assert http_response.mimetype == 'application/json'
