# -*- coding: utf-8 -*-

"""
This file contains all messages and message-related methods
"""

import time

MSG_WELCOME = 'Hi! Just type a subreddit name to start. Example: funny'
MSG_SUGGEST = 'Here you can find popular subreddit suggestions http://redditlist.com/'
MSG_INV_SUB = 'Invalid Subreddit'
MSG_RATE = '‎Use this link to rate and review:\nhttps://telegram.me/storebot?start='

MSG_CHECKOUT = 'Let\'s checkout /r/'
MSG_MOAR = ':thumbsup: MOAR /r/'
MSG_RANDOM = ':see_no_evil: Random Subreddit'

def getTimeAgo(timestamp):
    timespan = time.time() - timestamp

    if timespan > 3600*24:
        return '%d days ago' % int(timespan/(3600*24))
    elif timespan > 3600:
        return '%d hours ago' % int(timespan/3600)
    else:
        return '%d minutes ago' % int(timespan/60)