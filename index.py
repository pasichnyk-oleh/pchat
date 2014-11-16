# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web

import settings
from urls import urls

__author__ = 'o.pasichnyk'


tornado_settings = {'static_path': settings.STATIC_ROOT}
application = tornado.web.Application(urls, tornado_settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()
