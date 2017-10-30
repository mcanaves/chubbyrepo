"""Structures that transport call parameters and input data.

Requests are objects created from incoming calls, thus they shall deal with
things like incorrect values, missing parameters, wrong formats, etc. and
transport data from outside the application into the interactors layer.
"""
from typing import Dict, Optional, Union


class InvalidRequest:
    """"Contains requests validation errors and other errors from inner layers."""

    def __init__(self):
        self.errors = []

    def add_error(self, parameter: str, message: str):
        self.errors.append({'parameter': parameter, 'message': message})

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __bool__(self):
        return False


class ValidRequest:
    """"Contains interactor call parameters and input data."""

    @classmethod
    def from_dict(cls, adict: Dict) -> Union['ValidRequest', InvalidRequest]:
        raise NotImplementedError

    def __bool__(self):
        return True


class OrganizationStatsRequest(ValidRequest):
    """RepositoriesStats interactor request."""

    def __init__(self, organization_name: str):
        self.organization_name = organization_name

    @classmethod
    def from_dict(cls, adict):
        invalid_request = InvalidRequest()

        if 'organization_name' not in adict:
            invalid_request.add_error('organization_name', 'Is required')

        if 'organization_name' in adict and not isinstance(adict['organization_name'], str):
            invalid_request.add_error('organization_name', 'Is not string')

        if invalid_request.has_errors():
            return invalid_request

        return OrganizationStatsRequest(organization_name=adict['organization_name'])


class ChubbiestRepositoriesRequest(ValidRequest):
    """ChubbiestRepositories interactor request."""

    def __init__(self, limit: Optional[int]=None):
        self.limit = limit or 10

    @classmethod
    def from_dict(cls, adict):
        invalid_request = InvalidRequest()

        try:
            adict['limit'] = int(adict.get('limit', 10))
        except ValueError:
            invalid_request.add_error('limit', 'Is not integer')
        else:
            if not (1 <= adict['limit'] <= 100):
                invalid_request.add_error('limit', 'Must be between 1 and 100, both included')

        if invalid_request.has_errors():
            return invalid_request

        return ChubbiestRepositoriesRequest(limit=adict['limit'])
