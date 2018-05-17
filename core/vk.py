# -*- coding: utf-8 -*-
import json
import time

from vk_api.vk_api import VkApi

class VK:
    def __init__(self, username, password, log):
        self.vk = VkApi(login=username, password=password)
        self.vk.auth()
        self.log = log

    def send_message(self, chat_id, message):
        return self.vk.method(
            'messages.send',
            {'chat_id': chat_id, 'message': message}
        )

    def send_repost(self, chat_id, attachment):
        return self.vk.method(
            'messages.send',
            {'chat_id': chat_id, 'attachment': attachment }
        )

    def send_message_user(self, user_id, message):
        return self.vk.method(
            'messages.send',
            {'user_id': user_id, 'message': message}
        )

    def get_messages(self, value):
        return self.vk.method(
            'messages.get',
            value
        )

    def add_user(self, user_id, text):
        return self.vk.method(
            'friends.add',
            {'user_id': user_id, 'text': text}
        )

    def kick_user(self, chat_id, user_id):
        return self.vk.method(
            'messages.removeChatUser',
            {'chat_id': chat_id, 'user_id': user_id}
        )

    def invite_user(self, chat_id, user_id):
        return self.vk.method(
            'messages.addChatUser',
            {'chat_id': chat_id, 'user_id': user_id}
        )

    def get_uid_by_nick(self, nick):
        return self.vk.method(
            'utils.resolveScreenName',
            {'screen_name': nick}
        )['object_id']

    def get_users(self, chat_id):
        return self.vk.method(
            'messages.getChat',
            {'chat_id': chat_id}
        )['users']

    def request_list(self):
        return self.vk.method('friends.getRequests')['items']

    def get_last_news(self, group_id):
        return self.vk.method('wall.get',
            { "owner_id": "-{0}".format(group_id), "offset": 1, "count": 1 })['items'][0]['id']
