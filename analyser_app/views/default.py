from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models

import logging
log = logging.getLogger(__name__)

@view_config(route_name='admin', renderer='../templates/admin.mako')
@view_config(route_name='home', renderer='../templates/main.mako')
def my_view(request):
    if request.user:
        log.info(f'{request.matched_route} for {request.user.name}')
    else:
        log.info(f'{request.matched_route} for unregistered user')
    return {'project': 'Venus',
            'needs_tour': True,
            'needs_feat': True,
            'needs_ngl': True,
            'user': request.user}

@view_config(route_name='status', renderer='json')
def status_view(request):
    log.warn(f'Status ping request')
    return {'status': 'OK'}
