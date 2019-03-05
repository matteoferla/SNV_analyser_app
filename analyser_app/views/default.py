from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(route_name='home', renderer='../templates/default.mako')
def my_view(request):
    return {'project': 'analyser_app', 'needs_tour': True, 'needs_feat': True, 'needs_ngl': True}
