#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import time

from classes.bot import Bot

logging.basicConfig(
    format='[%(levelname)s][%(asctime)s] %(message)s',
    level=logging.INFO
)

if __name__ == "__main__":
    log = logging.getLogger(__name__)
    with open('config/config.json', 'r') as conf:
        config = json.loads(conf.read())
        log.info("Loaded file with configurations")
    with open('config/credentials.json', 'r') as creds:
        credentials = json.loads(creds.read())
        log.info("Loaded file with credentials")
    with open('config/messages.json', 'r') as msg:
        messages = json.loads(msg.read())
        log.info("Loaded file with messages")
    bot = Bot(config, credentials, messages, log)
    log.info("Bot initialized")

    while True:
        try:
            bot.check_messages()
            time.sleep(1)
        except KeyboardInterrupt:
            log.error("Shutdown...")
            raise
