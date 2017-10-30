"""Structures that transport results data.

Requests contain the results of the interactors calls, but shall also be able
to represent error cases and to deliver rich information on what happened.
"""
from typing import Any, Dict, Optional, Union

from chubbyrepo.core.requests import InvalidRequest


class ResponseSuccess:
    """Contain interactor response data."""

    SUCCESS = 'SUCCESS'

    def __init__(self, value: Optional[Any]):
        self.type = self.SUCCESS
        self.value = value


class ResponseFailure:
    """Contain errors that happen when running the interactor. Type errors:
        * RESOURCE_ERROR: errors related to the resources contained in the repository.
        * PARAMETERS_ERROR: errors that occur when the request parameters are wrong or missing.
        * SYSTEM_ERROR: errors that happen in the underlying system at operating system level.
    """

    RESOURCE_ERROR = 'RESOURCE_ERROR'
    PARAMETERS_ERROR = 'PARAMETERS_ERROR'
    SYSTEM_ERROR = 'SYSTEM_ERROR'

    def __init__(self, error_type: str, message: Union[str, Exception]):
        self.type = error_type
        self.message = self._format_message(message)

    @property
    def value(self) -> Dict[str, str]:
        return {'type': self.type, 'message': self.message}

    def __bool__(self):
        return False

    @staticmethod
    def _format_message(message: [str, Exception]) -> str:
        if isinstance(message, Exception):
            return "{}: {}".format(message.__class__.__name__, "{}".format(message))
        return message

    @classmethod
    def build_resource_error(cls, message: Optional[Union[str, Exception]]) -> 'ResponseFailure':
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message: Optional[Union[str, Exception]]) -> 'ResponseFailure':
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message: Optional[Union[str, Exception]]) -> 'ResponseFailure':
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_from_invalid_request(cls, invalid_request: InvalidRequest) -> 'ResponseFailure':
        message = "\n".join(["{}: {}".format(err['parameter'], err['message']) for err in invalid_request.errors])
        return cls.build_parameters_error(message)
