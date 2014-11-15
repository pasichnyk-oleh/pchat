# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['form_validator', 'BaseHandler', ]

import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

import settings


def form_validator(form_cls, raise_http_error=True):
    '''
    Decorator for semi-auto form validation in handlers.
    Data for validation get from "Handler.request.arguments"

    :param form_cls: class of Form validator
    :param raise_http_error: if True will be raised tornado.web.HTTPError(400)
    '''
    def method_wrapper(method):
        def wrapper(*args, **kwargs):
            self = args[0]
            form = form_cls(self.request.arguments)
            form.validate()

            if form.errors and raise_http_error:
                raise tornado.web.HTTPError(400)
            else:
                kwargs['form'] = form
                return method(*args, **kwargs)

        return wrapper

    return method_wrapper


class BaseHandler(tornado.web.RequestHandler):
    '''Base class for handlers. Can return user id, user name, render templates'''
    def _get_auth_data(self, key):
        '''
        Get data from Auth in headers by specific key

        :param key: what to get
        :return: "value" if key exist, otherwise None
        '''
        try:
            auth_data = self.request.headers.get('Auth')

            result = auth_data[key]
        except (TypeError, KeyError):
            return None
        else:
            return result

    def _get_user_id(self):
        '''
        Get "user id" from headers

        :return: int that correspond "user_id" or None if user is not authorized
        '''
        return self._get_auth_data('user_id')

    user_id = property(_get_user_id)

    def _get_user_name(self):
        '''
        Get user name from headers

        :return: "string" that correspond "user name" or None if user is not authorized
        '''
        name = self._get_auth_data('user_name')
        return unicode(name, 'utf8') if name else None

    user_name = property(_get_user_name)

    def _render_template(self, template_name, **kwargs):
        '''
        Render specific template

        :param template_name:  template to render
        :param kwargs: some data to pass into template
        :raise TemplateNotFound: will be raised if template can not be found
        :return string: rendered data
        '''
        env = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIRS))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)

        content = template.render(kwargs)

        return content

    def render_to_response(self, template_name, return_data=False, **kwargs):
        '''
        Render temlate to browser or return it

        :param template_name:  template to render
        :param return_data: True if you want to return data not render to browser
        :param kwargs: some data to pass into template
        :return: if return_data=True return rendered template
        '''
        root_params = {
            'STATIC_URL': settings.STATIC_URL,
            'SOCKET_URL': settings.SOCKET_URL,
            'user_id': self.user_id,
            'user_name': self.user_name
        }

        kwargs.update(root_params)

        content = self._render_template(template_name, **kwargs)

        if return_data:
            return content
        else:
            self.write(content)
