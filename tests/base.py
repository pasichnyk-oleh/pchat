# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['BaseAsyncTestCase', ]

from requests import Request
from tornado.testing import AsyncTestCase
from tornado.testing import AsyncHTTPClient

import settings
from models.users import User
from models.chat import ChatUser, Chat
from db_connect import db
from utils.random_data import random_string


class BaseAsyncTestCase(AsyncTestCase):
    def setUp(self):
        super(BaseAsyncTestCase, self).setUp()

        self.client = AsyncHTTPClient(self.io_loop)
        self.server_url = 'http://{0}:{1}'.format(settings.TESTING_SITE_URL, str(settings.TESTING_PORT))

        #setup test data
        self.user = self.init_base_user()
        self.chats = self.add_some_chats()

    def tearDown(self):
        super(BaseAsyncTestCase, self).tearDown()

        #delete test data
        self.delete_objects(self.user)
        self.delete_objects(*self.chats)

    def delete_objects(self, *args):
        '''
        Delete object or objects

        :param args: object/objects to delete
        :return: None
        '''
        for obj in args:
            db.delete(obj)

        db.commit()

    def do_request(self, uri, data=None, method="POST", timeout=20, body_ckeck=True, **kwargs):
        '''
        Do http request

        :param uri: do request to this uri (server_url + uri)
        :param data: request key/value data
        :param method: do request by this method
        :param timeout: sleep to some seconds if need
        :param body_ckeck: check response body by assertTrue of not
        :param kwargs: some addition params that will be send with request
        :return: body response
        '''
        request_data = data if data else {}

        request_params = dict(
            method=method,
            url=self.server_url + uri,
            data=request_data
        )

        #add additional params
        request_params.update(kwargs)

        rq = Request(**request_params).prepare()

        self.client.fetch(
            rq.url,
            callback=self.stop,
            method=rq.method,
            body=rq.body,
            headers=rq.headers
        )

        data = self.wait(timeout=timeout)

        self.assertTrue(data)

        if body_ckeck:
            self.assertTrue(data.body)

        return data.body

    def request_get(self, *args, **kwargs):
        '''
        Do http GET request (get wrapper for do_request)

        :param args:
        :param kwargs:
        :return: response body
        '''
        kwargs['method'] = 'GET'
        return self.do_request(*args, **kwargs)

    def request_post(self, *args, **kwargs):
        '''
        Do http POST request (post wrapper for do_request)

        :param args:
        :param kwargs:
        :return: response body
        '''
        kwargs['method'] = 'POST'
        return self.do_request(*args, **kwargs)

    def add_user(self, **user_data):
        '''
        Add some user to DB

        :param user_data: some user data
        :return: new added user
        '''
        user = User(**user_data)

        db.add(user)
        db.commit()

        return user

    def init_base_user(self):
        '''
        Prepopulate some user, that can be accessed by self.user

        :return: new added user
        '''
        return self.add_user(name='base_user_test', password='123456')

    def add_user_to_chat(self, chat_id, user_id):
        chat_user = ChatUser(chat_id=chat_id, user_id=user_id)

        db.add(chat_user)
        db.commit()

        return chat_user

    def add_chat(self, name, user_id):
        '''
        Wrapper for adding chat

        :param name: name of chat
        :param user_id: user id of user that add chat
        :return: new added chat
        '''
        chat = Chat(name=name, user_id=user_id)

        db.add(chat)
        db.commit()

        return chat

    def add_some_chats(self, num=5):
        '''
        Prepopulate some chats

        :param num: how much chats will be generated, default=5
        :return: list of generated chats
        '''
        chats = []

        for _ in range(num):
            name = random_string(5)

            chats.append(self.add_chat(name, self.user.id))

        return chats
