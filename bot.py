#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import logging
import praw
import telegram
from telegram.ext import CommandHandler, MessageHandler, Updater

from config import *
from messages import *

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)
reddit = praw.Reddit(user_agent=RD_USERAGENT)

class RedditRobot:
    def __init__(self):
        updater = Updater(token=TG_TOKEN)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', self.welcome))
        dp.add_handler(CommandHandler('suggest', self.suggest))
        dp.add_handler(CommandHandler('feedback', self.feedback))
        dp.add_handler(MessageHandler(self.fetch))
        dp.add_handler(MessageHandler(self.error))
        updater.start_polling()
        logger.info("RedditRobot started polling")
        self.message = ''
        self.chat_id = None
        self.user_id = None
        self.subreddit = None
        self.submission = None
        #updater.idle()

    def welcome(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=MSG_WELCOME)

    def suggest(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=MSG_SUGGEST)

    def feedback(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=MSG_RATE+TG_BOTNAME,
                        disable_web_page_preview=True)

    def fetch(self, bot, update):

        logger.info("Received message")

        self.set_message(update)
        self.set_chat_id(update)
        self.set_user_id(update)
        self.set_subreddit(bot)

    def error(self, update, error):
        logger.warning('Update "%s" caused error "%s"' % (update, error))

    def set_message(self, update):
        self.message = update.message.text

    def set_chat_id(self, update):
        self.chat_id = update.message.chat_id

    def set_user_id(self, update):
        self.user_id = update.message.from_user.id        

    def set_subreddit(self, bot, name=None):

        if 'random' in self.message.lower().split():
            name = str(reddit.random_subreddit())
            bot.sendMessage(chat_id=self.chat_id, text=MSG_CHECKOUT+name)

        elif name is None:
            # clean up user message
            name = self.message.encode('ascii', 'ignore')
            name = name.lower()
            name = name.replace('moar ', '') # kb press sends this
            name = name.replace('/r/', '')
            name = ''.join(name.split())

        try:
            self.subreddit = reddit.subreddit(name)

        except:  # to-do: specify exceptions
            bot.sendMessage(chat_id=self.chat_id, text=MSG_INV_SUB)
            logger.warning("Invalid /r/%s" % name)
            self.subreddit = None

if __name__ == "__main__": RedditRobot