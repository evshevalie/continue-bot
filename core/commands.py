# -*- coding: utf-8 -*-
import re
import pytz

from datetime import datetime, timedelta
from vk import VK
from vk_api.exceptions import ApiError
from database import Database
from functools import wraps

timezone = pytz.timezone('Europe/Moscow')

class Command:
    def __init__(self, vk, db, chat_id, messages, log):
        self.messages = messages
        self.chat_id = chat_id
        self.log = log
        self.vk = vk
        self.db = db

    def __only_admins(func):
        @wraps(func)
        def wrapper(self, params, user_id):
            if self.db.is_admin(user_id):
                func(self, params, user_id)
            else:
                self.__self_kick(user_id)
        return wrapper

    def __only_creators(func):
        @wraps(func)
        def wrapper(self, params, user_id):
            if self.db.is_creator(user_id):
                func(self, params, user_id)
            else:
                if self.db.is_admin(user_id):
                    self.vk.send_message(
                        self.chat_id,
                        "Данная команда не доступна вашему уровню привилегий"
                    )
                else:
                    self.__self_kick(user_id)
        return wrapper

    def __with_params(func):
        @wraps(func)
        def wrapper(self, params, user_id):
            if params:
                func(self, params, user_id)
            else:
                self.vk.send_message(
                    self.chat_id,
                    "Вы не ввели ни одного параметра"
                )
        return wrapper

    def __kick(self, user_id):
        self.vk.kick_user(self.chat_id, user_id)
        self.vk.add_user(user_id, self.messages['ban_user'])

    def __self_kick(self, user_id, time=1):
        if not self.db.is_kicked(user_id):
            time = datetime.now() + timedelta(minutes=time)
            return_time = time - datetime.now()

            self.vk.send_message(self.chat_id, self.messages['kick_yourself'])
            self.__kick(user_id)
            self.db.set_kicked(user_id, time)

    @__only_admins
    @__with_params
    def user_kick(self, params, user_id):
        if re.match(r"^\[id\d*\|.*\]$", params[0]):
            user_id = params[0].split("|")[0].replace("[id","")
            time = datetime.now()
            if len(params) == 1:
                time += timedelta(minutes=10)
            elif re.match(r"^\d*[dmh]$", params[1]):
                time_count = int(params[1][:-1])
                time_type = params[1][-1]

                if time_type == 'd':
                    time += timedelta(days=time_count)
                elif time_type == 'h':
                    time += timedelta(hours=time_count)
                elif time_type == 'm':
                    time += timedelta(minutes=time_count)
            else:
                self.vk.send_message(self.chat_id, "Введите корректно время. К примеру 10m - 10 минут")
                return

            return_time = time.replace(tzinfo=timezone).strftime("%Y-%m-%d %H:%M:%S")
            self.__kick(user_id)
            self.vk.send_message(self.chat_id, self.messages['kick'])
            self.db.set_kicked(user_id, time.strftime("%Y-%m-%d %H:%M:%S"))
            try:
                self.vk.send_message_user(user_id, self.messages['return_time'] + return_time)
            except ApiError:
                return
        else:
            self.vk.send_message(self.chat_id, "Введите корректно @упоминание")

    @__only_admins
    @__with_params
    def user_ban(self, params, user_id):
        if re.match(r"^\[id\d*\|.*\]$",params[0]):
            user_id = params[0].split("|")[0].replace("[id","")
            if not self.db.is_admin(user_id):
                self.__kick(user_id)
                self.vk.send_message(self.chat_id, self.messages['ban'])
                self.db.set_ban(user_id)
            else:
                self.vk.send_message(self.chat_id, "Нельзя забанить администратора!")
        else:
            self.vk.send_message(self.chat_id, "Это не похоже на упоминание...")


    @__only_admins
    @__with_params
    def user_unban(self, params, user_id):
        try:
            user_name = params[0]
            user_id = self.vk.get_uid_by_nick(user_name)

            self.db.unset_ban(user_id)
            try:
                self.vk.invite_user(self.chat_id, user_id)
            except ApiError:
                self.vk.send_message(self.chat_id, self.messages['return'])
        except TypeError:
            self.vk.send_message(self.chat_id, "Такого я не нахожу")

    @__only_admins
    @__with_params
    def user_unkick(self, params, user_id):
        try:
            user_name = params[0]
            user_id = self.vk.get_uid_by_nick(user_name)

            self.db.unset_kick(user_id)
            try:
                self.vk.invite_user(self.chat_id, user_id)
                self.vk.add_user(user_id, self.messages['ban_user'])
                self.vk.send_message(self.chat_id, self.messages['return_user'])
            except ApiError:
                self.vk.send_message(self.chat_id, self.messages['return'])
        except TypeError:
            self.vk.send_message(self.chat_id, "Такого я не нахожу")


    @__only_creators
    def user_admin(self, params, user_id):
        if not params:
            self.vk.send_message(
                self.chat_id,
                self.messages['help_admin'][1]
            )
        else:
            if params[1] is not None and re.match(r"^\[id\d*\|.*\]$", params[1]):
                user_id = params[1].split("|")[0].replace("[id","")
            else:
                self.vk.send_message(
                    self.chat_id,
                    "Введите @упоминание третьим параметром".format(user_id)
                )
                return

            if params[0] == "добавить":
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

    def print_hello(self):
        self.vk.send_message(self.chat_id, self.messages['hello'])

    def print_help(self, user_id):
        if self.db.is_admin(user_id):
            self.vk.send_message(self.chat_id, self.messages['help_admin'][0])
        else:
            self.vk.send_message(self.chat_id, self.messages['help_user'])

    def unknown(self):
        self.vk.send_message(self.chat_id, self.messages['unknown'])
