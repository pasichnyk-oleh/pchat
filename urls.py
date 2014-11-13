# coding: utf-8 -*-

__author__ = 'o.pasichnyk'

import tornado

import settings
from handlers import main, chat

urls = [
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings.STATIC_ROOT}),
    (r'/', main.MainHandler),
    (r'/registration', main.RegistrationHandler),
    (r'/error', main.ErrorHandler),
    (r'/chat', chat.MainHandler),
    (r'/chat/(\d+)', chat.ChatHandler),
    (r'/chat/join/(\d+)', chat.JoinHandler),
    (r'/chat/add', chat.ChatAddHandler),
    (r'/chat/search', chat.ChatSearchHandler),
    (settings.SOCKET_URL, chat.MessagesSocketHandler),
]
