# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['http_auth', ]

import base64

from models.users import User

user_checker = User.isset_user


def http_auth(handler_class):
    ''' Handle Tornado HTTP Basic Auth '''
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):
            auth_header = handler.request.headers.get('Authorization')

            if auth_header is None or not auth_header.startswith('Basic '):
                handler.set_status(401)
                handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
                handler._transforms = []
                handler.finish()

                return False

            auth_decoded = base64.decodestring(auth_header[6:])
            login, password = auth_decoded.split(':', 2)
            auth_found = user_checker(login, password)

            if auth_found is None:
                handler.set_status(401)
                handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
                handler._transforms = []
                handler.finish()

                return False
            else:
                handler.request.headers.add('auth', auth_found)

            return True

        def _execute(self, transforms, *args, **kwargs):
            if not require_auth(self, kwargs):
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class
