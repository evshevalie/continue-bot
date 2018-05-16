# -*- coding: utf-8 -*-
import logging
import os

from vk import VK
from database import Database
from commands import Command
from datetime import datetime


class Bot:
    def __init__(self, config, creds, messages, logging):
        self.lm = os.path.join(os.getcwd(), "cache/last_message_id")
        db_path = os.path.join(os.getcwd(), "database/continue-bot.db")

        self.log = logging
        self.vk = VK(creds['login'], creds['password'])
        self.database = Database(db_path, logging)
        self.command = Command(
            self.vk,
            self.database,
            config['chat_id'],
            messages,
            logging
        )
        self.config = config

        if os.path.exists(self.lm):
            with open(self.lm, 'r') as l:
                self.config['messages']['last_message_id'] = l.read()
                self.log.info("Readed last message id")

    def last_message(self, msg_id):
        message_conf = self.config['messages']

        if 'last_message_id' not in message_conf:
            with open(self.lm, 'w+') as l:
                l.write(str(msg_id))
        elif message_conf['last_message_id'] != msg_id:
            with open(self.lm, 'w+') as l:
                l.write(str(msg_id))

    def check_messages(self):
        messages = self.vk.get_messages(self.config['messages'])

        if messages['items']:
            last_message = messages['items'][0]['id']
            self.last_message(last_message)
            self.config['messages']['last_message_id'] = last_message

            for m in messages['items']:
                if 'chat_id' in m:
                    if m['chat_id'] == self.config['chat_id']:
                        m = m['body'].encode('utf-8')
                        text = m.split()
                        if text and text[0][0] == "/":
                            self.spawn_command(text)

    def check_unkicked(self):
        kicked = self.database.get_unkicked()
        if kicked:
            self.log.info("Next users will unckicked: {0}".format(kicked))
            for k in kicked:
                self.log.info("Unkicking user with id {0}".format(k[0]))
                self.command.user_unkick(["id{0}".format(k[0])])

    def check_intruders(self):
        kicked = [k[0] for k in self.database.get_all_kicked()]
        banned = [b[0] for b in self.database.get_all_banned()]

        intruders = set(kicked + banned)
        users = set(self.vk.get_users(config['chat_id']))
        intruders = list(intruders & users)

        if intruders:
            self.log.info("Starting kick some intruders...")
            for i in intruders:
                vk.self.kick_user(config['chat_id'], i)
                self.log.info("Kicked intruder with id {0}".format(i))

    def spawn_command(self, command):
        command_type = command[0][1:]
        command_params = command[1:]

        self.log.info("Read command \"{0}\"".format(command_type))
        if command_type == "помощь":
            self.command.print_help()
        elif command_type == "привет":
            self.command.print_hello()
        elif command_type == "кик":
            self.command.user_kick(command_params)
        elif command_type == "вернуть":
            self.command.user_unkick(command_params)
        elif command_type == "бан":
            self.command.user_ban(command_params)
        elif command_type == "разбан":
            self.command.user_unban(command_params)
        else:
            self.command.unknown()
