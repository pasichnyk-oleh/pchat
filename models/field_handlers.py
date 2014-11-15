# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['model_field_proccesing', 'Md5Handler', 'ImageFindHandler', ]

import urllib2
import hashlib
import re
from abc import ABCMeta, abstractmethod

from utils.random_data import random_string


def model_field_proccesing(*handlers):
    '''
    Decorator to handle some field in model

    :param handlers: list of handlers that implement BaseHandler and will do something with field value
    '''
    def proccessing(method):
        def wrapper(self, key, value):
            for handler in handlers:
                value = handler.process(value)
            return method(self, key, value)

        return wrapper
    return proccessing


class BaseHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, value):
        '''
        Method that will handle the value from model field

        :param value: value to handle
        :return: processed value
        '''
        pass


class Md5Handler(BaseHandler):
    '''Class that process string into md5 hash'''

    _salt = 'abc' #string that will be added to hash

    def __init__(self, salt='abc'):
        self._salt = salt

    def _decode_string(self, string):
        '''
        Decode string to md5 hash + some salt

        :param string: string to decode
        :return: hashed string
        '''
        new_string = '{salt}{string}{salt}'.format(salt=self._salt, string=string)

        return hashlib.md5(new_string).hexdigest()

    def process(self, value):
        '''Implemented method'''
        return self._decode_string(value)


class _HeadRequest(urllib2.Request):
    '''Derive from Request class and override get_method to allow a HEAD request.'''
    def get_method(self):
        '''Overriden'''
        return "HEAD"


class ImageFindHandler(BaseHandler):
    '''Class that find url in text, if it is image save it to local storage and add img tag to text'''
    _link_regex = re.compile("(?P<url>https?://[^\s]+)")
    _allowed_images_type = [('image/jpeg', 'jpeg'), ('image/pjpeg', 'jpg'), ('image/png', 'png')]

    def __init__(self, save_path='.'):
        self._save_path = save_path

    def process(self, value):
        '''Implemented method'''
        return self._process_text(value)

    def _process_text(self, text):
        '''facade of class'''
        url = self._find_url(text)

        if not url:
            return text

        mime_type = self._get_url_mime(url)

        if not self._is_mime_allowed(mime_type):
            return text

        file_path = self._get_and_save_content(url, mime_type)

        if not file_path:
            return text

        return self._append_img_tag(text, file_path)

    def _append_img_tag(self, text, img_path):
        '''
        Add img tag to text

        :param text: text into which will be added img tag
        :param img_path: path to img
        :return: message with added img tag
        '''
        #todo: rewrite
        return "{0}<br /><img src='{1}' />".format(text, img_path)

    def _get_and_save_content(self, url, mime):
        '''
        Get and save content to file

        :param url: url to get content
        :param mime: mime type of file
        :return: path of saved file
        '''
        try:
            content = urllib2.urlopen(url)
        except (urllib2.HTTPError, urllib2.URLError):
            return False

        file_ext = dict(self._allowed_images_type).get(mime)
        file_path = '%s%s.%s' % (self._save_path, random_string(15), file_ext)

        newFile = open (".%s" % file_path, "wb+")
        newFile.write(content.read())
        newFile.close()

        return file_path

    def _is_mime_allowed(self, mime):
        '''
        Check is mime allowed

        :param mime: mime to check
        :return: True if is allowed and False if not
        '''
        if not dict(self._allowed_images_type).get(mime, None):
            return False

        return True

    def _get_url_mime(self, url):
        '''
        Get mime type of url content

        :param url: url to get header
        :return: mime type or F
        '''
        try:
            response = urllib2.urlopen(_HeadRequest(url))
            response_headers = response.info()

            mime_type = response_headers['content-type']
        except urllib2.HTTPError:
            return False
        else:
            return mime_type

    def _find_url(self, text):
        '''
        Search url in text

        :param text: where to search
        :return: url if finded or False if not
        '''
        try:
            url = re.search(self._link_regex, text).group("url")
        except AttributeError:
            return False
        else:
            return url

class BotCmdHandler(BaseHandler):
    '''
    Bot that search some comand in text end execute it.
    For example sum of 1 2 3
    '''
    def process(self, value):
        '''Implemented method'''
        # todo
        return value
