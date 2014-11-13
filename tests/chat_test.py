# coding: utf-8 -*-

__author__ = 'o.pasichnyk'
__all__ = ['TestChat', ]

from sqlalchemy.orm.exc import NoResultFound

from db_connect import db
from tests.base import BaseAsyncTestCase
from tests.tests_utils.fixtureman import FixtureManager
from models.chat import ChatUser

chat_fixture = FixtureManager()
chat_fixture.load(fixture_file='fixtures/chat', current_file=__file__)


class TestChat(BaseAsyncTestCase):

    def test_get_user_chats(self):
        chat_user = []
        chat_user_obj = []

        for chat in self.chats:
            chat_user_obj.append(self.add_user_to_chat(chat.id, self.user.id))
            chat_user.append(chat.id)

        new_chat_user = ChatUser.get_user_chats(self.user.id)

        self.assertEqual(chat_user.sort(), new_chat_user.sort())
        self.delete_objects(*chat_user_obj)

    def test_user_has_access(self):
        chat_user_obj = []

        for chat in self.chats:
            chat_user_obj.append(self.add_user_to_chat(chat.id, self.user.id))

            self.assertTrue(ChatUser.has_access(self.user.id, chat.id))

        self.delete_objects(*chat_user_obj)

    def test_user_not_has_access(self):
        for chat in self.chats:
            self.assertFalse(ChatUser.has_access(self.user.id, chat.id))

    def test_user_join(self):
        chat = self.chats[0]

        ChatUser.join_switcher(self.user.id, chat.id)

        get_row = db.query(ChatUser).filter(ChatUser.user_id==self.user.id, ChatUser.chat_id==chat.id).one()

        self.assertTrue(get_row)
        self.delete_objects(get_row)


    def test_user_unjoin(self):
        chat = self.chats[0]
        self.add_user_to_chat(chat.id, self.user.id)

        ChatUser.join_switcher(self.user.id, chat.id)

        with self.assertRaises(NoResultFound):
            db.query(ChatUser).filter(ChatUser.user_id==self.user.id, ChatUser.chat_id==chat.id).one()
