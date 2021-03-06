# coding: utf-8 -*-

import urllib2
import hashlib
import re
import __builtin__
from abc import ABCMeta, abstractmethod

from utils.random_data import random_string

__author__ = 'o.pasichnyk'
__all__ = ['model_field_proccesing', 'Md5Handler', 'ImageFindHandler', ]


def model_field_proccesing(*handlers):
    '''
    Decorator to handle some field in model

    :param handlers: list - list of handlers that implement BaseHandler and will do something with field value
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

        :param value: str - value to handle
        :return: str - processed value
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

        :param string: str - value to decode
        :return: str - hashed value
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

        :param text: str - text into which will be added img tag
        :param img_path: str - path to img
        :return: str - message with added img tag
        '''
        #todo: rewrite
        return "{0}<br /><img src='{1}' />".format(text, img_path)

    def _get_and_save_content(self, url, mime):
        '''
        Get and save content to file

        :param url: str - url to get content
        :param mime: str - mime type of file
        :return: str -path of saved file
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

        :param mime: str - mime to check
        :return: bool - True if is allowed and False if not
        '''
        if not dict(self._allowed_images_type).get(mime, None):
            return False

        return True

    def _get_url_mime(self, url):
        '''
        Get mime type of url content

        :param url: str - url to get header
        :return: str - mime type or F
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

        :param text: str - where to search
        :return: str -url if finded or False if not
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
    For example: sum of 1 2 3
    '''
    _allowed_cmd_patterns = [(re.compile("(sum of (\d+\s?)+)"), "sum"),
                             (re.compile("(min of (\d+\s?)+)"), "min"),
                             (re.compile("(max of (\d+\s?)+)"), "max"),
                             (re.compile("(sort (\d+\s?)+)"), "sorted")]

    _elements_pattern = re.compile("\d+")

    def process(self, value):
        '''Implemented method'''

        cmd, func = self._find_cmd(value)

        if not cmd:
            return value

        elements = self._get_int_elements(cmd)

        func_result = self._run_func(func, elements)

        value = self._concat_to_text(func_result, cmd, value)

        return value

    def _concat_to_text(self, result, cmd, original):
        '''
        Add some text to initial text

        :param result: str - what will be added
        :param cmd: str -  command  that was founded
        :param original: str - initial text
        :return: str - result of concatenating
        '''
        return "{0}<blockquote>result of {1} is: {2}</blockquote>".format(original, cmd, result)

    def _run_func(self, func, elements):
        '''
        Do some operation by function with some elements

        :param func: str - func to process
        :param elements: list - data what to handle
        :return: result of function work
        '''
        return getattr(__builtin__, func)(elements)

    def _get_int_elements(self, cmd):
        '''
        Get numbers from string

        :param cmd: str - where to search numbers
        :return: list - list of numbers
        '''
        result = re.findall(self._elements_pattern, cmd)

        return map(int, result)

    def _find_cmd(self, string):
        '''
        Search comand in string

        :param string: str - where to search
        :return: tuple - if found will be return tuple with comand and function, otherwise None, None
        '''
        for pattern, func in self._allowed_cmd_patterns:
            try:
                cmd = re.search(pattern, string).group()
            except AttributeError:
                continue
            else:
                return cmd, func

        return None, None
