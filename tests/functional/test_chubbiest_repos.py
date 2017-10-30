from unittest import mock

import pytest
from flask import url_for


@mock.patch('requests.post')
def test_get_chubbiest_repositories(mock_post, client):
    mock_post.return_value.json.return_value = {
        'data': {
            'search': {
                'edges': [
                    {'node': {'name': 'react', 'stargazers': {'totalCount': 79799}}},
                    {'node': {'name': 'd3', 'stargazers': {'totalCount': 69548}}},
                    {'node': {'name': 'awesome', 'stargazers': {'totalCount': 68386}}},
                    {'node': {'name': 'oh-my-zsh', 'stargazers': {'totalCount': 61047}}},
                    {'node': {'name': 'angular.js', 'stargazers': {'totalCount': 57403}}},
                    {'node': {'name': 'gitignore', 'stargazers': {'totalCount': 56731}}},
                    {'node': {'name': 'electron', 'stargazers': {'totalCount': 52146}}},
                    {'node': {'name': 'linux', 'stargazers': {'totalCount': 51312}}},
                    {'node': {'name': 'coding-interview-university', 'stargazers': {'totalCount': 48909}}},
                    {'node': {'name': 'jquery', 'stargazers': {'totalCount': 46881}}}
                ]
            }
        }
    }
    http_response = client.get(url_for('api.chubbiest_repositories'))
    assert http_response.json == [
        {'name': 'react', 'stars': 79799},
        {'name': 'd3', 'stars': 69548},
        {'name': 'awesome', 'stars': 68386},
        {'name': 'oh-my-zsh', 'stars': 61047},
        {'name': 'angular.js', 'stars': 57403},
        {'name': 'gitignore', 'stars': 56731},
        {'name': 'electron', 'stars': 52146},
        {'name': 'linux', 'stars': 51312},
        {'name': 'coding-interview-university', 'stars': 48909},
        {'name': 'jquery', 'stars': 46881},
    ]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('requests.post')
def test_get_chubbiest_repositories_with_limit(mock_post, client):
    mock_post.return_value.json.return_value = {
        'data': {
            'search': {
                'edges': [
                    {'node': {'name': 'react', 'stargazers': {'totalCount': 79799}}},
                ]
            }
        }
    }
    http_response = client.get(url_for('api.chubbiest_repositories'), query_string={'limit': 1})
    assert http_response.json == [{'name': 'react', 'stars': 79799}]
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@pytest.mark.parametrize('limit,expected_json', [
    ('asdf', {'message': 'limit: Is not integer', 'type': 'PARAMETERS_ERROR'}),
    (0, {'message': 'limit: Must be between 1 and 100, both included', 'type': 'PARAMETERS_ERROR'}),
    ('101', {'message': 'limit: Must be between 1 and 100, both included', 'type': 'PARAMETERS_ERROR'}),
])
def test_get_chubbiest_repositories_invalid_limit(client, limit, expected_json):
    http_response = client.get(url_for('api.chubbiest_repositories'), query_string={'limit': limit})
    assert http_response.json == expected_json
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'
