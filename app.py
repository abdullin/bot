import argparse
import datetime
import json
import os
import traceback
from os import path
import subprocess

import pytz
from telegram import Update, Bot
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


# bot = telegram.Bot(token=cfg.key)

updater = Updater(token=cfg.key)
dispatcher = updater.dispatcher
bot = updater.bot


def handle_message(bot: Bot, update: Update):
    context = ""
    try:

        message = update.effective_message
        chat_id = str(message.chat_id)

        if not chat_id in tg_cfg['chats']:
            reply(bot, "Chat {0} not registered".format(chat_id), message.chat_id)
            return

        chat = tg_cfg['chats'][chat_id]
        folder = chat['folder']

        context = folder

        local = get_message_date_local(update)

        dict = update.to_dict()
        em = dict.pop("_effective_message", None)

        # cleanup empty arrays
        for k in list(em):
            if not em[k]:
                em.pop(k)

        em.pop("chat", None)

        em["_time"] = local.isoformat()
        em["update_id"] = update.update_id

        db.append_item(path.join(cfg.root, folder), em)

        exec = chat.get('exec', None)

        if not exec:
            reply(bot, "{0}> saved {1}".format(context, update.update_id))
            return

        result = subprocess.run(exec, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        if len(output) > 1000:
            output = output[-1000:]
        reply(bot, "{0}> exec {1}: {2}".format(context, result.args, output))

    except:
        reply(bot, "{0}> err {1}".format(context, traceback.format_exc()))
        return




def get_message_date_local(update: Update):
    message = update.effective_message
    date = message.date
    if message.forward_date:
        date = message.forward_date
    local: datetime.datetime = utc_to_local(date)
    return local


def reply(bot, status, chat_id=None):
    bot.send_message(chat_id=chat_id or reply_chat_id, text=status)


from telegram.ext import MessageHandler, Filters

dispatcher.add_handler(MessageHandler(
    Filters.all,
    handle_message,
    allow_edited=True,
    message_updates=True))

updater.start_polling()
updater.idle()
