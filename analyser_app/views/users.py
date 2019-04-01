from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from ..models import User

from pyramid.security import (
    remember,
    forget,
    )

@view_config(route_name='login', renderer="json")
def login_view(request):
    action   = request.params['action']
    username = request.params['username']
    password = request.params['password']
    print('login_view', action)
    user = request.dbsession.query(User).filter_by(name=username).first()
    if action == 'login':
        if user is not None and user.check_password(password):
            headers = remember(request, user.id)
            request.response.headerlist.extend(headers)
            return {'status': 'logged in', 'name': user.name, 'rank': user.role}
        elif user:
            request.response.status = 400
            return {'status': 'wrong password'}
        else:
            request.response.status = 400
            return {'status': 'wrong username'}
    elif action == 'register':
        if not user:
            if username == 'admin':
                new_user = User(name=username, role='admin')
            else:
                new_user = User(name=username, role='basic')
            new_user.set_password(password)
            request.dbsession.add(new_user)
            return {'status': 'registered', 'name': new_user.name, 'rank': new_user.role}
        else:
            request.response.status = 400
            return {'status': 'existing username'}
    elif action == 'logout':
        headers = forget(request)
        request.response.headerlist.extend(headers)
        return {'status': 'logged out'}
    elif action == 'promote':
        if request.user and request.user.role == 'admin': ##only admins can make admins
            target=request.dbsession.query(User).filter_by(name=username).one()
            target.role = 'admin'
            request.dbsession.add(target)
            return {'status': 'promoted'}
    else:
        request.response.status = 400
        return {'status': 'unknown request'}
