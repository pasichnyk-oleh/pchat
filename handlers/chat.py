# coding: utf-8 -*-

import tornado.ioloop
import tornado.websocket
import tornado.escape
import tornado.web

from handlers.base import BaseHandler, form_validator
from utils.auth import http_auth
from forms.chat import ChatAddForm, ChatSearchForm, MessageForm
from db_connect import db
from models.chat import Chat, ChatUser, Message
from models.users import User

__author__ = 'o.pasichnyk'
__all__ = ['MainHandler', 'JoinHandler', 'ChatSearchHandler', 'ChatAddHandler', 'ChatHandler', 'MessagesSocketHandler',]


@http_auth
class MainHandler(BaseHandler):
    '''Handler to process chat main page'''
    def get(self):
        user_in_chats = ChatUser.get_user_chats(self.user_id)
        chats = db.query(Chat).all()

        self.render_to_response("chat/index.html", chat_add_form=ChatAddForm(),
                                chat_search_form=ChatSearchForm(), chats=chats, user_in_chats=user_in_chats)


@http_auth
class JoinHandler(BaseHandler):
    '''Handler to process joining/un-joining user to chat'''
    def get(self, chat_id):
        ChatUser.join_switcher(self.user_id, chat_id)

        user_in_chats = ChatUser.get_user_chats(self.user_id)
        chats = db.query(Chat).all()
        self.render_to_response("chat/chats_list.html", chats=chats, user_in_chats=user_in_chats)


@http_auth
class ChatSearchHandler(BaseHandler):
    '''Handler to process search query to search chats'''
    @form_validator(ChatSearchForm)
    def post(self, form):

        search_value = u'%{0}%'.format(self.get_argument("name"))
        chats = db.query(Chat).filter(Chat.name.like(search_value)).all()

        user_in_chats = ChatUser.get_user_chats(self.user_id)

        self.render_to_response("chat/chats_list.html", chats=chats, user_in_chats=user_in_chats)


@http_auth
class ChatAddHandler(BaseHandler):
    '''Handler to process adding new chat'''
    @form_validator(ChatAddForm)
    def post(self, form):
        '''Create new Chat object, populate it, save and render new chats list'''
        chat = Chat()
        form.populate_obj(chat)
        chat.user_id = self.user_id
        db.add(chat)
        db.commit()

        #re-render block with chats
        user_in_chats = ChatUser.get_user_chats(self.user_id)
        chats = db.query(Chat).all()
        self.render_to_response("chat/chats_list.html", chats=chats, user_in_chats=user_in_chats)


@http_auth
class ChatHandler(BaseHandler):
    '''Handler to process some specific chat page'''
    def get(self, chat_id):
        #if user is not joined to chat - redirct to chat main page
        if not ChatUser.has_access(self.user_id, chat_id):
            self.redirect("/chat")

        chat = db.query(Chat).filter(Chat.id == chat_id).one()
        messages = db.query(Message, User).join(User).filter(
            Message.chat_id == chat_id).order_by(Message.id.desc()).limit(50).all()

        self.render_to_response("chat/chat.html", chat=chat, messages=messages, form=MessageForm(chat_id=chat_id))


@http_auth
class MessagesSocketHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    '''Handler to process socket work'''

    connections = set() #only unique socket connections

    def _format_data_to_form(self, data):
        '''
        Must reformat data that come from socket to work fine with WTForms

        :param data: form data from socket
        :return: reformated dict, for example {'message': ['text'], 'chat_id': ['1']}
        '''
        result = {}

        for key, val in data.items():
           result[str(key)] = [val]

        return result

    def open(self):
        '''
        Add new user to list of connectors

        :return: None
        '''
        self.__class__.connections.add(self)

    def on_close(self):
        '''
        If socket close - remove user from list of connectors

        :return: None
        '''
        self.__class__.connections.remove(self)

    @classmethod
    def send_updates(cls, message):
        '''
        Send message to all from connectors list

        :param message: what to send
        :return: None
        '''
        for waiter in cls.connections:
            waiter.write_message(message)

    def on_message(self, data_json):
        '''
        Runs when socket send some message.
        Validating the data, save data and render new message html template

        :param data_json: form from socket in json
        :raise HTTPError: if user is not joined to chat or form data is not valid
        :return: None
        '''
        data = tornado.escape.json_decode(data_json)

        #if not in chat - raise HTTPError
        if not ChatUser.has_access(self.user_id, data['chat_id']):
            raise tornado.web.HTTPError(400)

        form = MessageForm(self._format_data_to_form(data))

        #if bad data - raise HTTPError
        if not form.validate():
            raise tornado.web.HTTPError(400)

        #adding message to DB
        message = Message()
        form.populate_obj(message)
        message.user_id = self.user_id
        db.add(message)
        db.commit()

        current_user = User(name=self.user_name, id=self.user_id)

        data_to_response = {'id': message.id,
                            'message': self.render_to_response("chat/message.html", return_data=True,
                                                   message=message, user=current_user)}

        self.__class__.send_updates(data_to_response)
