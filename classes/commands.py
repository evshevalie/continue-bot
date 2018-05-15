# -*- coding: utf-8 -*-
from vk import VK

class Command:
    def __init__(self, vk, chat_id, messages):
        self.messages = messages
        self.chat_id = chat_id
        self.vk = vk

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
        return

    def unknown(self):
        self.vk.send_message(self.chat_id, self.messages['unknown'])
