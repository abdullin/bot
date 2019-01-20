import argparse
import datetime
import os

import pytz
from telegram import Update, Bot
from telegram.ext import Updater

import db
import render
from context import get_active_context

parser = argparse.ArgumentParser(description='Launch')
parser.add_argument('--key', action='store', dest='key', required=True)
parser.add_argument('--www', action='store', dest='www', required=True)

# to allow introducing arguments in advance
cfg, unknown = parser.parse_known_args()


render.set_www_root(cfg.www)

local_tz = pytz.timezone('Asia/Yekaterinburg')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # .normalize might be unnecessary


import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(cfg.key)
dispatcher = updater.dispatcher


def handle_photo(bot: Bot, update: Update):
    context = get_active_context(update)

    if not context:
        reply(bot, update, context, "need context!")
        return

    local = get_message_date_local(update)
    largest_photo_id = update.message.photo[-1].file_id
    file = bot.getFile(largest_photo_id)

    jpg_ = local.strftime('%Y-%m-%d_%H%M%S') + ".jpg"

    name = os.path.join(db.get_dir(context), jpg_)

    file.download(name)

    db.append_item(context, {
        'kind': 'photo',
        'file': jpg_,
        'time': local.isoformat(),
        'raw': update.to_dict(),
    })

    render.render_context(context)

    reply(bot, update, context, 'saved')


def handle_text(bot: Bot, update: Update):
    context = get_active_context(update)

    if not context:
        reply(bot, update, context, "need context!")
        return

    local = get_message_date_local(update)

    text = update.message.text

    db.append_item(context, {
        'kind': 'text',
        'text': text,
        'time': local.isoformat(),
        'raw': update.to_dict(),
    })

    render.render_context(context)
    reply(bot, update, context, "ok")


def get_message_date_local(update: Update):
    date = update.message.date
    if update.message.forward_date:
        date = update.message.forward_date
    local: datetime.datetime = utc_to_local(date)
    return local


def reply(bot, update, context, status):
    text = '{0}> {1}'.format(context, status)
    bot.send_message(chat_id=update.message.chat_id, text=text)


from telegram.ext import MessageHandler, Filters

dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

updater.start_polling()
updater.idle()
