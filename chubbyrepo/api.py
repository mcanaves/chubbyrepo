from flask import Blueprint, jsonify, request

from chubbyrepo.core.interactors import ChubbiestRepositoriesInteractor, OrganizationStatsInteractor
from chubbyrepo.core.requests import ChubbiestRepositoriesRequest, OrganizationStatsRequest
from chubbyrepo.core.responses import ResponseFailure, ResponseSuccess
from chubbyrepo.gateways import RepositoryGateway, StatsGateway

api_blueprint = Blueprint('api', __name__)

STATUS_CODES = {
    ResponseSuccess.SUCCESS: 200,
    ResponseFailure.RESOURCE_ERROR: 404,
    ResponseFailure.PARAMETERS_ERROR: 400,
    ResponseFailure.SYSTEM_ERROR: 500
}


@api_blueprint.route('/organizations/<org_name>/stats', methods=['GET'])
def organization_stats(org_name):
    """Get organization repositories stats. Number of repositories and
    the biggest one.
    """
    request_object = OrganizationStatsRequest.from_dict({'organization_name': org_name})
    interactor = OrganizationStatsInteractor(StatsGateway())
    response = interactor.execute(request_object)
    return jsonify(response.value), STATUS_CODES[response.type]


@api_blueprint.route('/chubbiest_repositories', methods=['GET'])
def chubbiest_repositories():
    """List n-th most starred repositories. By default n is 10 and can be
     set with `limit` query param.
     """
    limit = request.args.get('limit', 10)
    request_object = ChubbiestRepositoriesRequest.from_dict({'limit': limit})
    interactor = ChubbiestRepositoriesInteractor(RepositoryGateway())
    response = interactor.execute(request_object)
    return jsonify(response.value), STATUS_CODES[response.type]
