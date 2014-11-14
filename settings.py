# coding: utf-8 -*-

__author__ = 'o.pasichnyk'

import os
import importlib


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
UPLOAD_FILES_DIR = "/static/files/"

#url for socket requests
SOCKET_URL = r"/chat/socket"

# settings for testing
TESTING_PORT = 8889 #port for unit test
TESTING_SITE_URL = '0.0.0.0' #url for tests requests


#import env settings
env_name = os.environ.get('ENV_NAME', None)

def import_env_vars(env_settings):
    globals_var = globals()

    for item in dir(env_settings):
        if item.startswith("__"):
            continue

        if item in globals_var:
            globals_var[item] = getattr(env_settings, item)

try:
    env_settings = importlib.import_module('settings_%s' % env_name)
except ImportError:
    pass
else:
    import_env_vars(env_settings)
