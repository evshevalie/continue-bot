# -*- coding: utf-8 -*-
import logging
import os

from vk import VK
from database import Database
from commands import Command
from datetime import datetime


class Bot:
    def __init__(self, config, creds, messages, home, logging):
        self.cache_lm = os.path.join(home, "cache/last_message_id")
        self.cache_ln = os.path.join(home, "cache/last_post_id")
        db_path = os.path.join(home, "database/continue-bot.db")

        self.vk = VK(creds['login'], creds['password'], logging)
        self.database = Database(db_path, logging)
        self.command = Command(
            self.vk,
            self.database,
            config['chat_id'],
            messages,
            logging
        )
        self.log = logging
        self.config = config
        self.messages = messages

        if os.path.exists(self.cache_lm):
            with open(self.cache_lm, 'r') as l:
                self.config['messages']['last_message_id'] = l.read()
                self.log.info("Readed last message id")

    def check_messages(self):
        messages = self.vk.get_messages(self.config['messages'])

        if messages['items']:
            last_message = messages['items'][0]['id']
            self.__last_message(last_message)
            self.config['messages']['last_message_id'] = last_message

            for m in messages['items']:
                if 'chat_id' in m:
                    if m['chat_id'] == self.config['chat_id']:
                        command = m['body'].encode('utf-8')
                        command = command.split()
                        if command and command[0][0] == "/":
                            self.__spawn_command(command, m['user_id'])

    def check_unkicked(self):
        kicked = self.database.get_unkicked()

        if kicked:
            self.log.info("Next users will unckicked: {0}".format(kicked))
            for k in kicked:
                self.log.info("Unkicking user with id {0}".format(k))
                self.command.user_unkick(["id{0}".format(k)], "0")

    def check_intruders(self):
        kicked = self.database.get_all_kicked()
        banned = self.database.get_all_banned()

        intruders = set(kicked + banned)
        users = set(self.vk.get_users(self.config['chat_id']))
        intruders = list(intruders & users)

        if intruders:
            self.log.info("Starting kick some intruders...")
            for i in intruders:
                self.vk.kick_user(self.config['chat_id'], i)
                self.log.info("Kicked intruder with id {0}".format(i))

    def check_friends(self):
        users = self.vk.request_list()

        if users:
            for u in users:
                self.log.info("Adding user with id {0}".format(u))
                self.vk.add_user(u, self.messages['frendly'])

    def check_news(self):
        seconds = datetime.now().second

        if seconds > 55 and seconds < 59:
            with open(self.cache_ln, "r") as r:
                last_id = r.read()

            last_news = self.vk.get_last_news(self.config['group_id'])
            if int(last_id) != int(last_news):
                self.vk.send_repost(
                    self.config['chat_id'],
                    "wall-{0}_{1}".format(self.config['group_id'], last_news)
                )
                with open(self.cache_ln, "w+") as f:
                    f.write(str(last_news))

    def __last_message(self, msg_id):
        message_conf = self.config['messages']

        if 'last_message_id' not in message_conf:
            with open(self.cache_lm, 'w+') as l:
                l.write(str(msg_id))
        elif message_conf['last_message_id'] != msg_id:
            with open(self.cache_lm, 'w+') as l:
                l.write(str(msg_id))

    def __spawn_command(self, command, user_id):
        command_type = command[0][1:]
        command_params = [] + command[1:]

        self.log.info("Read command \"{0}\"".format(command_type))
        if command_type == "помощь" or command_type == "help":
            self.command.print_help(user_id)
        elif command_type == "привет" or command_type == "hello":
            self.command.print_hello()
        elif command_type == "правила" or command_type == "rules":
            self.command.print_rules()
        elif command_type == "кик" or command_type == "kick":
            self.command.user_kick(command_params, user_id)
        elif command_type == "вернуть" or command_type == "return":
            self.command.user_unban(command_params, user_id)
        elif command_type == "бан" or command_type == "ban":
            self.command.user_ban(command_params, user_id)
        elif command_type == "админ" or command_type == "admin":
            self.command.user_admin(command_params, user_id)
        elif command_type == "предупреждение" or command_type == "warning":
            self.command.user_warning(command_params, user_id)
        else:
            self.command.unknown()
