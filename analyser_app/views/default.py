from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

@view_config(route_name='admin', renderer='../templates/admin.mako')
@view_config(route_name='home', renderer='../templates/main.mako')
def my_view(request):
    return {'project': 'Venus',
            'needs_tour': True,
            'needs_feat': True,
            'needs_ngl': True,
            'user': request.user}


@view_config(route_name='status', renderer='json')
def status_view(request):
    return {'status': 'OK'}
