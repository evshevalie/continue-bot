# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

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

    def user_kick(self, params, user_id):
        if self.db.is_admin(user_id):
            user_id = params[0].split("|")[0].replace("[id","")
            time_count = int(params[1][:-1])
            time_type = params[1][-1]

            if time_type == 'd':
                time = datetime.now() + timedelta(days=time_count)
            elif time_type == 'h':
                time = datetime.now() + timedelta(hours=time_count)
            elif time_type == 'm':
                time = datetime.now() + timedelta(minutes=time_count)

            time = time.strftime("%Y-%m-%d %H:%M:%S")
            self.vk.send_message(self.chat_id, self.messages['kick'])
            self.vk.kick_user(self.chat_id, user_id)
            self.db.set_kicked(user_id, time)
            self.vk.add_user(user_id, self.messages['kick_user'])
        else:
            time = datetime.now() + timedelta(minutes=10)
            time = time.strftime("%Y-%m-%d %H:%M:%S")

            self.vk.send_message(self.chat_id, self.messages['kick_yourself'])
            self.vk.kick_user(self.chat_id, user_id)
            self.db.set_kicked(user_id, time)

    def user_ban(self, params, user_id):
        if self.db.is_admin(user_id):
            user_id = params[0].split("|")[0].replace("[id","")

            self.vk.send_message(self.chat_id, self.messages['ban'])
            self.vk.kick_user(self.chat_id, user_id)
            self.db.set_ban(user_id)
            self.vk.add_user(user_id, self.messages['ban_user'])
        else:
            time = datetime.now() + timedelta(minutes=10)
            time = time.strftime("%Y-%m-%d %H:%M:%S")

            self.vk.send_message(self.chat_id, self.messages['kick_yourself'])
            self.vk.kick_user(self.chat_id, user_id)
            self.db.set_kicked(user_id, time)

    def user_unban(self, params, user_id):
        if self.db.is_admin(user_id):
            nick = params[0]
            user_id = self.vk.get_uid_by_nick(nick)

            self.db.unset_ban(user_id)
            try:
                self.vk.invite_user(self.chat_id, user_id)
            except ApiError:
                self.log.error("This user are not in friend list")
                self.vk.send_message(self.chat_id, self.messages['return'])
        else:
            self.vk.send_message(self.chat_id, self.messages['kick_yourself'])

    def user_unkick(self, params, user_id):
        if self.db.is_admin(user_id):
            nick = params[0]
            user_id = self.vk.get_uid_by_nick(nick)

            self.db.unset_kick(user_id)
            try:
                self.vk.invite_user(self.chat_id, user_id)
                self.vk.add_user(user_id, self.messages['ban_user'])
                self.vk.send_message(self.chat_id, self.messages['return_user'])
            except ApiError:
                self.log.error("This user are not in friend list")
                self.vk.send_message(self.chat_id, self.messages['return'])
        else:
            self.vk.send_message(self.chat_id, self.messages['kick_yourself'])

    def user_admin(self, params, user_id):
        if self.db.is_admin(user_id):
            if params:
                user_id = params[1].split("|")[0].replace("[id","")
            if not params:
                self.vk.send_message(
                    self.chat_id,
                    self.messages['help_admin'][1]
                )
            elif params[0] == "добавить":
                self.db.set_admin(user_id)
                self.vk.send_message(
                    self.chat_id,
                    "[id{0}|Администратор] успешно добавлен!".format(user_id)
                )
            elif params[0] == "удалить":
                self.db.remove_admin(user_id)
                self.vk.send_message(
                    self.chat_id,
                    "[id{0}|Администратор] успешно удален!".format(user_id)
                )
            elif params[0] == "повысить":
                self.db.set_creator(user_id)
                self.vk.send_message(
                    self.chat_id,
                    "[id{0}|Администратор] успешно повышен!".format(user_id)
                )
            else:
                self.unknown()
        else:
            self.vk.send_message(self.chat_id, self.messages['kick_yourself'])

    def print_hello(self):
        self.vk.send_message(self.chat_id, self.messages['hello'])

    def print_help(self, user_id):
        if self.db.is_admin(user_id):
            self.vk.send_message(self.chat_id, self.messages['help_admin'][0])
        else:
            self.vk.send_message(self.chat_id, self.messages['help_user'])

    def unknown(self):
        self.vk.send_message(self.chat_id, self.messages['unknown'])
