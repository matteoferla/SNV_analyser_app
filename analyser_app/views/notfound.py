from pyramid.view import notfound_view_config
import logging

log = logging.getLogger(__name__)

@notfound_view_config(renderer='../templates/404.mako')
def notfound_view(request):
    request.response.status = 404
    if request.user:
        log.warn(f'{request.user.name} requested a non-existant page')
    else:
        ip = '/'.join([request.environ[x] for x in ("REMOTE_ADDR", "HTTP_X_FORWARDED_FOR", "HTTP_CLIENT_IP") if x in request.environ])
        log.warn(f'Unregistered user {ip} requested a non-existant page')
    return {}
