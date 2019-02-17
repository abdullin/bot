import argparse
import datetime
import json
import os
from os import path

import pytz
import telegram
from telegram import Update, Bot, PhotoSize
from telegram.ext import Updater

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

import db


parser = argparse.ArgumentParser(description='Launch')
parser.add_argument('--key', action='store', dest='key', required=True)
parser.add_argument('--store', action='store', dest='root', required=True)

# to allow introducing arguments in advance
cfg, unknown = parser.parse_known_args()



with open(os.path.join(cfg.root, "telegram.json")) as f:
    tg_cfg = json.load(f)


reply_chat_id = tg_cfg['reply_chat_id']


local_tz = pytz.timezone('Asia/Yekaterinburg')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # .normalize might be unnecessary



#bot = telegram.Bot(token=cfg.key)

updater = Updater(token=cfg.key)
dispatcher = updater.dispatcher
bot = updater.bot


def handle_message(bot: Bot, update: Update):

    chat_id = str(update.message.chat_id)

    if not chat_id in tg_cfg['chats']:
        reply(bot, "Chat {0} not registered".format(chat_id), update.message.chat_id)
        return

    chat =  tg_cfg['chats'][chat_id]
    folder = chat['folder']

    local = get_message_date_local(update)
    db.append_item(path.join(cfg.root,folder), {
        'time': local.isoformat(),
        'raw': update.to_dict(),
    })

    reply(bot, 'ok')

def get_message_date_local(update: Update):
    date = update.message.date
    if update.message.forward_date:
        date = update.message.forward_date
    local: datetime.datetime = utc_to_local(date)
    return local


def reply(bot, status, chat_id = None):
    bot.send_message(chat_id=chat_id or reply_chat_id, text=status)


from telegram.ext import MessageHandler, Filters

dispatcher.add_handler(MessageHandler(Filters.all, handle_message, allow_edited=True))

updater.start_polling()
updater.idle()
