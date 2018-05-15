from vk import VK

class Command:
    def __init__(self, vk, chat_id):
        self.chat_id = chat_id
        self.vk = vk

    def print_hello(self):
        self.vk.send_message(self.chat_id, self.messages['hello'])

    def print_help(self):
        self.vk.send_message(self.chat_id, self.messages['help'])

    def user_kick(self, parameters):
        user_id = parameters[0].split("|")[0].replace("[id","")
        self.vk.send_message(self.chat_id, "КИКАЛИТИ 😏")
        self.vk.kick_user(self.chat_id, user_id)

    def unknown(self):
        self.vk.send_message(self.config['chat_id'], "Мне такая команда неизвестна :C")
