# coding: utf-8 -*-

from tornado.testing import AsyncHTTPTestCase, gen_test

__author__ = 'o.pasichnyk'
__all__ = ['TestSocket', ]


class TestSocket(AsyncHTTPTestCase):
    def get_app(self):
        return None

    @gen_test
    def test_on_message(self):
        #todo
        pass
