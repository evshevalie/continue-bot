# -*- coding: utf-8 -*-
import logging
import os

from vk import VK
from database import Database
from commands import Command

class Bot:
    def __init__(self, config, creds, messages, logging):
        self.lm = os.path.join(os.getcwd(), "config/last_message_id.txt")
        db_path = os.path.join(os.getcwd(), "database/continue-bot.db")

        self.log = logging
        self.vk = VK(creds['login'], creds['password'])
        self.database = Database(db_path, logging)
        self.command = Command(self.vk, self.database, config['chat_id'], messages, self.log)
        self.config = config

        if os.stat(self.lm).st_size != 0:
            with open(self.lm, 'r') as l:
                self.config['messages']['last_message_id'] = l.read()
                self.log.info("Readed last message id")

    def last_message(self, msg_id):
        message_conf = self.config['messages']

        if not 'last_message_id' in message_conf:
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
        elif command_type == "бан":
            self.command.user_ban(command_params)
        elif command_type == "разбан":
            self.command.user_unban(command_params)
        else:
            self.command.unknown()
