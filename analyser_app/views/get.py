############ THIS IS COPY PASTE FROM MICHELANGLO. PLEASE EDIT THAT TOO.
### EXCEPT FOR get_pages METHOD


from pyramid.view import view_config
from pyramid.renderers import render_to_response
import traceback
from ..models.pages import Page
from ..models.user import User

import logging
log = logging.getLogger(__name__)
from ._common_methods import get_username

@view_config(route_name='get')
def get_ajax(request):
    def log_it():
        log.warn(f'{get_username(request)} was refused {request.params["item"]}, code: {request.response.status}')

    user = request.user
    modals = {'register': "../templates/login/register_modalcont.mako",
            'login': "../templates/login/login_modalcont.mako",
            'forgot': "../templates/login/forgot_modalcont.mako",
            'logout': "../templates/login/logout_modalcont.mako",
            'password': "../templates/login/password_modalcont.mako"}
    ###### get the user page list.
    if request.params['item'] == 'pages':
        if not user:
            request.response.status = 401
            log_it()
            return render_to_response("../templates/part_error.mako", {'error': '401'}, request)
        elif user.role == 'admin':
            target = request.dbsession.query(User).filter_by(name=request.POST['username']).one()
            return render_to_response("../templates/login/pages.mako", {'user': target}, request)
        elif request.POST['username'] == user.name:
            return render_to_response("../templates/login/pages.mako", {'user': request.user}, request)
        else:
            request.response.status = 403
            log_it()
            return render_to_response("../templates/part_error.mako", {'error': '403'}, request)
    ####### get the modals
    elif request.params['item'] in  modals.keys():
        return render_to_response(modals[request.params['item']], { 'user': request.user}, request)
    ####### get the implementation code.
    elif request.params['item'] == 'implement':
        ## should non editors be able to see this??
        page = Page(request.params['page'])
        if 'key' in request.params:
            page = Page(request.params['page'], request.params['key'])
        else:
            page = Page(request.params['page'])
        settings = page.load()
        return render_to_response("../templates/results/implement.mako", settings, request)
    else:
        request.response.status = 404
        log_it()
        return render_to_response("../templates/part_error.mako", {'error': '404'}, request)