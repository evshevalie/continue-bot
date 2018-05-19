#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import logging
import time

from daemonize import Daemonize
from datetime import datetime
from core.bot import Bot

logging.basicConfig(
    format='[%(levelname)s][%(asctime)s] %(message)s',
    level=logging.INFO
)
log = logging.getLogger(__name__)

def main():
    bot_home = os.path.dirname(os.path.abspath( __file__ ))

    with open(os.path.join(bot_home, 'config/config.json'), 'r') as conf:
        config = json.loads(conf.read())
        log.info("Loaded file with configurations")
    with open(os.path.join(bot_home, 'config/credentials.json'), 'r') as creds:
        credentials = json.loads(creds.read())
        log.info("Loaded file with credentials")
    with open(os.path.join(bot_home, 'config/messages.json'), 'r') as msg:
        messages = json.loads(msg.read())
        log.info("Loaded file with messages")

    bot = Bot(config, credentials, messages, bot_home, log)
    log.info("Bot initialized")

    while True:
        try:
            bot.check_messages()
            bot.check_unkicked()
            bot.check_intruders()
            bot.check_friends()
            bot.check_news()
            time.sleep(1)

        except KeyboardInterrupt:
            log.error("Shutdown...")
            raise

if __name__ == "__main__":
    main()
