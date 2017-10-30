import pytest

from chubbyrepo.core.requests import InvalidRequest
from chubbyrepo.core.responses import ResponseFailure, ResponseSuccess


class TestResponseSuccess:
    @pytest.fixture
    def response_value(self):
        return {'key': ['value1', 'value2']}

    def test_is_true(self, response_value):
        assert bool(ResponseSuccess(response_value)) is True

    def test_contains_value(self, response_value):
        response = ResponseSuccess(response_value)
        assert response.value == response_value


class TestResponseFailure:
    @pytest.fixture
    def response_type(self):
        return 'ResponseError'

    @pytest.fixture
    def response_message(self):
        return 'This is a response error'

    def test_is_false(self, response_type, response_message):
        assert bool(ResponseFailure(response_type, response_message)) is False

    def test_has_type_and_message(self, response_type, response_message):
        response = ResponseFailure(response_type, response_message)
        assert response.type == response_type
        assert response.message == response_message

    def test_contains_value(self, response_type, response_message):
        response = ResponseFailure(response_type, response_message)
        assert response.value == {'type': response_type, 'message': response_message}

    def test_initialization_with_exception(self, response_type):
        response = ResponseFailure(response_type, Exception('Just an error message'))
        assert bool(response) is False
        assert response.type == response_type
        assert response.message == "Exception: Just an error message"

    def test_from_invalid_request_object(self):
        response = ResponseFailure.build_from_invalid_request(InvalidRequest())
        assert bool(response) is False

    def test_from_invalid_request_object_with_errors(self):
        request_object = InvalidRequest()
        request_object.add_error('path', 'Is mandatory')
        request_object.add_error('path', "can't be blank")
        response = ResponseFailure.build_from_invalid_request(request_object)
        assert bool(response) is False
        assert response.type == ResponseFailure.PARAMETERS_ERROR
        assert response.message == "path: Is mandatory\npath: can't be blank"

    def test_build_resource_error(self):
        response = ResponseFailure.build_resource_error("test message")
        assert bool(response) is False
        assert response.type == ResponseFailure.RESOURCE_ERROR
        assert response.message == "test message"

    def test_build_parameters_error(self):
        response = ResponseFailure.build_parameters_error("test message")
        assert bool(response) is False
        assert response.type == ResponseFailure.PARAMETERS_ERROR
        assert response.message == "test message"

    def test_build_system_error(self):
        response = ResponseFailure.build_system_error("test message")
        assert bool(response) is False
        assert response.type == ResponseFailure.SYSTEM_ERROR
        assert response.message == "test message"
