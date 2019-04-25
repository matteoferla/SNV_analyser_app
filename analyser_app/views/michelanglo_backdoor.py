import requests as rq
from pyramid.view import view_config
import os

import logging
log = logging.getLogger(__name__)

@view_config(route_name='xpost', renderer="string")
def talk_to_michelanglo(request):
    """
    This is an experimental option. What if there was a single user db?
    The problem is that the cookie on one App is different from the other.
    Two layers of security. A shared environment variable and REMOTE_ADDR 127.0.0.1
    Do note that the apps are in different venvs.
    """
    if request.user: #this feature is not open to unregistered users.
        data = {'username': request.user.name,
                'code': os.environ['SECRETCODE'],
                'description': request.params['description'],
                'title': request.params['title'],
                'protein': request.params['protein']
        }
        log.info(f'{request.user.name} generated a report')
        return rq.post(os.environ['MICHELANGLO_URL']+'/venus', data=data).content.decode('utf-8')
    else:
        log.warn(f'Unregisted user tried to generate a report')
        request.response.status = 403
        return {'status':'Please register'}
