import argparse
import datetime
import os

import pytz
from telegram import Update, Message, Bot
from telegram.ext import Updater, CommandHandler


parser = argparse.ArgumentParser(description='Launch')
parser.add_argument('--key', action='store', dest='key',
                    help='Current stage name: DEV, TEST or PROD. Default: DEV',required=True)

parser.add_argument('--www', action='store', dest='www')
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



def load_index():
    file = get_context_dir() + '/index.json'

    items = []
    with open(file, mode='r', encoding='utf-8') as js:

        for line in js:
            if line:
                items.append(json.loads(line))
    return items


def render_index():
    items = load_index()

    output = cfg.www + '/' + get_context() + '/index.html'

    with open(output, mode='w', encoding='utf-8') as w:
        w.write('<html><body>')
        for i in items:
            if i['kind'] == 'text':
                lines = i['text'].split('\n')
                for l in lines:
                    w.write('<p>' + l + '</p>')

        w.write('</body></html>')



def append_index(item):
    ensure_context_dir()
    file = get_context_dir()+'/index.json'
    with open(file, mode='a+', encoding='utf-8') as js:
        json.dump(item, js, ensure_ascii=False)
        js.write('\n')
    render_index()


def photo_handler(bot: Bot, update: Update):
    ensure_context_dir()
    m: Message = update.message
    local = get_message_date_local(update)
    largest_photo_id = update.message.photo[-1].file_id
    file = bot.getFile(largest_photo_id)

    jpg_ = local.strftime('%Y-%m-%d_%H%M%S') + ".jpg"
    name = get_context_dir() + '/' + jpg_

    file.download(name)

    append_index({
        'kind': 'photo',
        'file': jpg_,
        'time': local.isoformat()
    })

    reply(bot, update, 'saved')

def get_context():
    if context:
        return context
    return 'inbox'

def set_context(ctx):
    global context
    context = ctx


def get_context_dir():
    return 'data/' + get_context()

def ensure_context_dir():
    dir = get_context_dir()
    if not os.path.exists(dir):
        os.makedirs(dir)


contexts = {
    'maya':[ 'майя', 'maya'],
    'erik':['эрик', 'erik'],
    'robot':['robot'],
}

def echo(bot, update: Update):
    local = get_message_date_local(update)

    text = update.message.text

    lower = text.lower()

    for ctx, tags in contexts.items():
        for t in tags:
            tag = '#'+t
            if tag in lower:
                set_context(ctx)

    append_index({
        'kind': 'text',
        'text': text,
        'time': local.isoformat()
    })

    reply(bot, update, "ok")


def get_message_date_local(update: Update):
    date = update.message.date
    if update.message.forward_date:
        date = update.message.forward_date
    local: datetime.datetime = utc_to_local(date)
    return local


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
