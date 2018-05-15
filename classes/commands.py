# -*- coding: utf-8 -*-

from vk import VK
from vk_api.exceptions import ApiError
from database import Database

class Command:
    def __init__(self, vk, db, chat_id, messages, log):
        self.messages = messages
        self.chat_id = chat_id
        self.log = log
        self.vk = vk
        self.db = db

    def print_hello(self):
        self.vk.send_message(self.chat_id, self.messages['hello'])

    def print_help(self):
        self.vk.send_message(self.chat_id, self.messages['help'])

    def user_kick(self, params):
        user_id = params[0].split("|")[0].replace("[id","")

        self.vk.send_message(self.chat_id, self.messages['kick'])
        self.vk.kick_user(self.chat_id, user_id)

    def user_ban(self, params):
        user_id = params[0].split("|")[0].replace("[id","")

        self.vk.send_message(self.chat_id, self.messages['ban'])
        self.vk.kick_user(self.chat_id, user_id)
        self.db.set_ban(user_id)
        self.vk.add_user(user_id, self.messages['ban_user'])

    def user_unban(self, params):
        nick = params[0]
        user_id = self.vk.get_uid_by_nick(nick)

        self.db.unset_ban(user_id)
        try:
            self.vk.invite_user(self.chat_id, user_id)
        except ApiError:
            self.log.error("This user are not in friend list")
            self.vk.send_message(self.chat_id, self.messages['return'])

    def unknown(self):
        self.vk.send_message(self.chat_id, self.messages['unknown'])
