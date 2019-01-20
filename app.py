import argparse
import datetime
import os

import pytz
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler


parser = argparse.ArgumentParser(description='Launch')
parser.add_argument('--key', action='store', dest='key',
                    help='Current stage name: DEV, TEST or PROD. Default: DEV',required=True)
# to allow introducing arguments in advance
cfg, unknown = parser.parse_known_args()


local_tz = pytz.timezone('Asia/Yekaterinburg')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


updater = Updater(cfg.key)
dispatcher = updater.dispatcher


context = None

import json

def append_index(local, text):
    ensure_context_dir()
    file = get_context()+'/index.json'
    with open(file, mode='a+', encoding='utf-8') as js:
        json.dump({'text': text, 'time': local.isoformat()}, js, ensure_ascii=False)
        js.write('\n')




def photo_handler(bot, update):
    ensure_context_dir()
    m: Message = update.message
    local: datetime.datetime = utc_to_local(update.message.date)
    largest_photo_id = update.message.photo[-1].file_id
    file = bot.getFile(largest_photo_id)

    name = get_context() + '/' + local.strftime('%Y-%m-%d') + ".jpg"


    file.download(name)
    reply(bot, update, 'saved')

def get_context():
    if context:
        return context
    return 'inbox'

def set_context(ctx):
    global context
    context = ctx




def ensure_context_dir():
    context = get_context()
    if not os.path.exists(context):
        os.makedirs(context)


contexts = ['maya', 'erik', 'robot']

def echo(bot, update: Update):


    m : Message = update.message

    local : datetime.datetime = utc_to_local(update.message.date)

    text = update.message.text

    lower = text.lower()

    for ctx in contexts:
        tag = '#'+ctx
        if tag in lower:
            set_context(tag)
            return


    append_index(local, text)
    reply(bot, update, "ok")


def reply(bot, update, status):
    context = get_context()
    text = '{0}> {1}'.format(context, status)
    bot.send_message(chat_id=update.message.chat_id, text=text)


from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


photo_handler = MessageHandler(Filters.photo, photo_handler)
dispatcher.add_handler(photo_handler)


updater.start_polling()
updater.idle()
