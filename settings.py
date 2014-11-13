# coding: utf-8 -*-

__author__ = 'o.pasichnyk'

import os


PROJECT_DIR = os.path.join(os.path.dirname(__file__))

DEBUG = True
PORT = 8888

DATABASE = {
    'name': 'test',
    'host': 'localhost',
    'user': 'postgres',
    'password': '123456',
    'port': 5433
}

TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIR, "templates/"),
]

# static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(PROJECT_DIR, "static/")
STATIC_URL = '/static/'

#url for socket requests
SOCKET_URL = r"/chat/socket"

# settings for testing
TESTING_PORT = 8888 #port for unit test
TESTING_SITE_URL = '0.0.0.0' #url for tests requests
