import argparse
import datetime

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

def append_file(file, local, text):
    with open(file, mode='a+', encoding='utf-8') as js:
        json.dump({'text': text, 'time': local.isoformat()}, js, ensure_ascii=False)
        js.write('\n')


def photo_handler(bot, update):
    m: Message = update.message
    local: datetime.datetime = utc_to_local(update.message.date)
    largest_photo_id = update.message.photo[-1].file_id
    file = bot.getFile(largest_photo_id)

    name = local.strftime('%Y-%m-%d') + ".jpg"
    if context:
        name = context + "/" + name
    file.download(name)
    bot.sendMessage(chat_id=update.message.chat_id, text="download succesfull")



def set_context(ctx):
    global context
    context = ctx

def echo(bot, update: Update):

    global context

    m : Message = update.message

    local : datetime.datetime = utc_to_local(update.message.date)

    text = update.message.text

    lower = text.lower()

    if '#maya' in lower:
        set_context('maya')
        append_file("maya.json", local, text)
        bot.send_message(chat_id=update.message.chat_id, text='#maya')
        return

    cmd = text.split(' ', 1)[0].lower()




    if cmd == 'tm':
        local = local + datetime.timedelta(days=1)
        file = local.strftime('%Y-%m-%d') + ".json"
        append_file(file, local, text)
        bot.send_message(chat_id=update.message.chat_id, text='+tomorrow')
        return
    if cmd == '#bonus':
        append_file("bonus.json", local, text)
        bot.send_message(chat_id=update.message.chat_id, text='+bonus')
        return



    file = local.strftime('%Y-%m-%d') + ".json"
    append_file(file, local, text)
    bot.send_message(chat_id=update.message.chat_id, text='+today')




from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


photo_handler = MessageHandler(Filters.photo, photo_handler)
dispatcher.add_handler(photo_handler)


updater.start_polling()
updater.idle()
