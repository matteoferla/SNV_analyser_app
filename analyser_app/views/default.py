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
        log.info(f'{request.matched_route.name} for {request.user.name}')
    else:
        log.info(f'{request.matched_route.name} for unregistered user')
    page = request.matched_route.name
    reply = {'project': 'Venus',
            'needs_tour': True,
            'needs_feat': True,
            'needs_ngl': True,
            'user': request.user}
    if page == 'admin':
        #reply['users'] = request.dbsession.query(User).all()
        pass
    return reply

@view_config(route_name='status', renderer='json')
def status_view(request):
    log.warn(f'Status ping request')
    return {'status': 'OK'}
